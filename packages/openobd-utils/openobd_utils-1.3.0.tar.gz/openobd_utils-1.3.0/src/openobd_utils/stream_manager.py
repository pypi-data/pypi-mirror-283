import threading
import typing
from queue import Queue, Empty
from collections.abc import Callable, Iterator
from typing import Any
from grpc import Call, StatusCode
from openobd_protocol.Messages import Empty_pb2 as grpcEmpty
from .stream_manager_exceptions import StreamException, StreamStoppedException, StreamTimeoutException


class IteratorStopped(Exception):
    pass


def requires_active_iterator(func):
    def wrapper(*args, **kwargs):
        iterator = args[0]
        assert isinstance(iterator, MessageIterator), "Decorator 'requires_active_iterator' used outside of MessageIterator!"
        if iterator.stop_iteration:
            raise IteratorStopped("Unable to fulfill request, as the iterator has been stopped.")
        return func(*args, **kwargs)
    return wrapper


class MessageIterator:

    def __init__(self, message: Any = None):
        self.next_messages = Queue()
        self.lock = threading.RLock()
        self.next_iteration_condition = threading.Condition(self.lock)
        self.queue_empty_condition = threading.Condition(self.lock)
        if message is not None:
            self.send_message(message)
        self.stop_iteration = False

    def __iter__(self):
        return self

    def __next__(self):
        with self.lock:
            if self.stop_iteration:
                raise StopIteration
            if self.next_messages.qsize() == 0:
                self.queue_empty_condition.notify_all()
                self.next_iteration_condition.wait()
                if self.stop_iteration:
                    raise StopIteration
            value = self.next_messages.get()
        return value

    @requires_active_iterator
    def send_message(self, message: Any):
        with self.lock:
            self.next_messages.put(message)
            self.next_iteration_condition.notify_all()

    @requires_active_iterator
    def stop(self, send_remaining_messages=False):
        with self.lock:
            if send_remaining_messages:
                self.wait_until_messages_sent()
            self.stop_iteration = True
            self.next_iteration_condition.notify_all()

    @requires_active_iterator
    def wait_until_messages_sent(self, timeout=10):
        with self.lock:
            self.queue_empty_condition.wait(timeout)


def requires_active_stream(func):
    def wrapper(*args, **kwargs):
        stream_manager = args[0]
        assert isinstance(stream_manager, StreamManager), "Decorator 'requires_active_stream' used outside of a StreamManager class!"
        if stream_manager.received_exception:
            raise stream_manager.received_exception
        if stream_manager.stream_finished:
            raise StreamStoppedException("Unable to fulfill request, as there is no stream active.")
        return func(*args, **kwargs)
    return wrapper


class BidirectionalStreamManager:

    def __init__(self, stream_function: Callable[[Iterator], Iterator]):
        """
        Allows easier handling of a bidirectional gRPC stream by providing methods to send and receive messages.

        :param stream_function: a reference to the function which should be used to send and receive messages.
        """
        self.incoming_messages = Queue()
        self.iterator = MessageIterator()
        self.response_iterator = stream_function(self.iterator)
        self.stream_thread = threading.Thread(target=self._stream, args=[stream_function], daemon=True)
        self.stream_thread.start()
        self.stream_finished = False

    @requires_active_stream
    def receive(self, block: bool = True, timeout: float | None = None) -> Any:
        """
        Retrieves the oldest pending message. If there are no pending messages, wait until a new message arrives.

        :param block: whether to wait for a new message if there are no pending messages.
        :param timeout: time in seconds to wait for a new message before raising a StreamTimeoutException. None will wait forever.
        :return: a message received by the gRPC stream.
        """
        try:
            return self.incoming_messages.get(block=block, timeout=timeout)
        except Empty:
            raise StreamTimeoutException

    @requires_active_stream
    def send(self, message: Any, clear_received_messages=False):
        """
        Sends a new message to this object's stream.

        :param message: the message to send to the stream.
        :param clear_received_messages: clears received messages that haven't been read yet. Can be helpful to find the response to this message.
        """
        if clear_received_messages:
            with self.incoming_messages.mutex:
                self.incoming_messages.queue.clear()
        self.iterator.send_message(message)

    @requires_active_stream
    def stop_stream(self):
        """
        Closes the stream. A new BidirectionalStreamManager object will have to be created to start another stream.
        """
        # Stops the outgoing stream
        if not self.iterator.stop_iteration:
            self.iterator.stop()
        # Stops the incoming stream
        if hasattr(self.response_iterator, "cancel"):
            self.response_iterator.cancel()
        else:
            raise StreamException("Unable to stop the stream, as the stream object does not have a `cancel` method.")

    def _stream(self, stream_function: Callable[[Iterator], Iterator]):
        """
        Starts a bidirectional stream. Places incoming messages in self.incoming_messages as they arrive.

        :param stream_function: a reference to the function which will be used to send and receive messages.
        """
        try:
            for response in self.response_iterator:
                self.incoming_messages.put(response)
        except Exception as e:
            if isinstance(e, Call) and e.code() == StatusCode.CANCELLED:
                # The stream has been cancelled, so there's no need to stop it again
                pass
            else:
                print(f"Encountered exception while handling the bidirectional gRPC stream: {e}")
                self.stop_stream()
        finally:
            self.stream_finished = True


class ThreadSafeVariable:

    def __init__(self, value=None):
        self.value = value
        self.value_change_condition = threading.Condition()     # Acts as a lock

    def get_value_when_set(self, timeout=None):
        with self.value_change_condition:
            change_detected = self.value_change_condition.wait(timeout)
            if not change_detected:
                return None
            return self.value

    def get_latest_value(self):
        with self.value_change_condition:
            return self.value

    def set(self, value):
        with self.value_change_condition:
            self.value = value
            self.value_change_condition.notify_all()


class OutgoingStreamManager:

    def __init__(self, stream_function: Callable[[Iterator], Any]):
        """
        Allows easier handling of an outgoing gRPC stream by providing methods to send messages and receive the response.

        :param stream_function: a reference to the function which should be used to send messages.
        """
        self.response = ThreadSafeVariable()
        self.iterator = MessageIterator()
        self.stream_thread = threading.Thread(target=self._stream, args=[stream_function], daemon=True)
        self.stream_thread.start()
        self.stream_finished = False

    @requires_active_stream
    def send(self, message: Any):
        """
        Sends a new message to this object's stream.

        :param message: the message to send to the stream.
        """
        self.iterator.send_message(message)

    @requires_active_stream
    def finish(self) -> Any:
        """
        Closes the stream after having sent all messages, and returns the response. A new OutgoingStreamManager object
        will have to be created to start another stream.

        :return: the response received from the server. Returns None if no response is received within 10 seconds.
        """
        self.iterator.stop(send_remaining_messages=True)
        return self.response.get_value_when_set(timeout=10)

    def _stream(self, stream_function: Callable[[Iterator], Any]):
        """
        Starts an outgoing stream. Saves the response in the ThreadSafeVariable self.response.

        :param stream_function: a reference to the function which will be used to send messages.
        """
        try:
            response = stream_function(self.iterator)
            self.response.set(response)
        except Exception as e:
            print(f"Encountered exception while handling the outgoing gRPC stream: {e}")
            self.iterator.stop()
        finally:
            self.stream_finished = True


class IncomingStreamManager:

    def __init__(self, stream_function: Callable[[Any], Iterator], request: Any = None):
        """
        Allows easier handling of an incoming gRPC stream by providing methods to receive messages.

        :param stream_function: a reference to the function which should be used to receive messages.
        :param request: the message to send at the start of the stream. Leave it None to send an EmptyMessage.
        """
        self.incoming_messages = Queue()
        self.request = request if request is not None else grpcEmpty.EmptyMessage()
        self.response_iterator = stream_function(self.request)
        self.stream_thread = threading.Thread(target=self._stream, args=[stream_function], daemon=True)
        self.stream_thread.start()
        self.stream_finished = False

    @requires_active_stream
    def receive(self, block: bool = True, timeout: float | None = None) -> Any:
        """
        Retrieves the oldest pending message. If there are no pending messages, wait until a new message arrives.

        :param block: whether to wait for a new message if there are no pending messages.
        :param timeout: time in seconds to wait for a new message before raising a StreamTimeoutException. None will wait forever.
        :return: a message received by the gRPC stream.
        """
        try:
            return self.incoming_messages.get(block=block, timeout=timeout)
        except Empty:
            raise StreamTimeoutException

    @requires_active_stream
    def stop_stream(self):
        """
        Closes the stream. A new IncomingStreamManager object will have to be created to start another stream.
        """
        if hasattr(self.response_iterator, "cancel"):
            self.response_iterator.cancel()
        else:
            raise StreamException("Unable to stop the stream, as the stream object does not have a `cancel` method.")

    def _stream(self, stream_function: Callable[[Any], Iterator]):
        """
        Starts an incoming stream. Places incoming messages in self.incoming_messages as they arrive.

        :param stream_function: a reference to the function which will be used to receive messages.
        """
        try:
            for response in self.response_iterator:
                self.incoming_messages.put(response)
        except Exception as e:
            if isinstance(e, Call) and e.code() == StatusCode.CANCELLED:
                # The stream has been cancelled, so there's no need to stop it again
                pass
            else:
                print(f"Encountered exception while handling the incoming gRPC stream: {e}")
                self.stop_stream()
        finally:
            self.stream_finished = True


class StreamManager:

    def __init__(self, stream_function: Callable[[Any], Any], request: Any = None, outgoing_stream: bool | None = None, incoming_stream: bool | None = None):
        """
        Allows easier handling of a gRPC stream by providing methods to send and receive messages.

        :param stream_function: a reference to the function which should be used to send and receive messages.
        :param request: the message to send when not using an outgoing stream. Leave it None to send an EmptyMessage.
        :param outgoing_stream: Whether the function requires a stream of messages as input. Leave None to determine it using the function's type hints.
        :param incoming_stream: Whether the function returns a stream of messages. Leave None to determine it using the function's type hints.
        """
        outgoing_stream = outgoing_stream if outgoing_stream is not None else self._has_outgoing_stream(stream_function)
        incoming_stream = incoming_stream if incoming_stream is not None else self._has_incoming_stream(stream_function)

        self.request_iterator = MessageIterator() if outgoing_stream else None

        if outgoing_stream:
            request = self.request_iterator
        else:
            request = request if request is not None else grpcEmpty.EmptyMessage()
        self.response_iterator = stream_function(request) if incoming_stream else None

        self.incoming_messages = Queue()
        self.stream_thread = threading.Thread(target=self._stream, args=[stream_function, request], daemon=True)
        self.stream_thread.start()
        self.stream_finished = False
        self.received_exception = None

    @staticmethod
    def _has_outgoing_stream(function: Callable[[Any], Any]) -> bool:
        type_hints = typing.get_type_hints(function)
        parameters = {k: v for k, v in type_hints.items() if k != "return"}
        parameter_type = next(iter(parameters.values()), None)
        return typing.get_origin(parameter_type) == Iterator

    @staticmethod
    def _has_incoming_stream(function: Callable[[Any], Any]) -> bool:
        type_hints = typing.get_type_hints(function)
        return_type = type_hints.get("return", Any)
        return typing.get_origin(return_type) == Iterator

    def receive(self, block: bool = True, timeout: float | None = None) -> Any:
        """
        Retrieves the oldest pending message. If there are no pending messages, wait until a new message arrives.

        :param block: whether to wait for a new message if there are no pending messages. If False, returns None when no messages are pending.
        :param timeout: time in seconds to wait for a new message before raising a StreamTimeoutException. None will wait forever.
        :return: a message received by the gRPC stream.
        """
        # If an exception occurred in this stream, raise it
        if self.received_exception:
            raise self.received_exception

        try:
            incoming_message = self.incoming_messages.get(block=block, timeout=timeout)
            # If an exception occurred while waiting, raise it
            if isinstance(incoming_message, Exception):
                raise incoming_message
            else:
                return incoming_message
        except Empty:
            if block:
                raise StreamTimeoutException
            else:
                return None

    @requires_active_stream
    def send(self, message: Any, clear_received_messages=False) -> None:
        """
        Sends a new message to this object's stream.

        :param message: the message to send to the stream.
        :param clear_received_messages: clears received messages that haven't been read yet. Can be helpful to find the response to this message.
        """
        if self.request_iterator is None:
            raise StreamException("It is not possible to send messages, as this object does not have an outgoing stream.")

        if clear_received_messages:
            with self.incoming_messages.mutex:
                self.incoming_messages.queue.clear()
        self.request_iterator.send_message(message)

    @requires_active_stream
    def stop_stream(self) -> None:
        """
        Closes the stream. A new StreamManager object will have to be created to start another stream.
        """
        if self.request_iterator is not None:
            # Stops the outgoing stream
            if not self.request_iterator.stop_iteration:
                if self.response_iterator is not None:
                    self.request_iterator.stop()
                else:
                    # When only using an outgoing stream, be sure to send all the messages before stopping
                    self.request_iterator.stop(send_remaining_messages=True)

        if self.response_iterator is not None:
            # Stops the incoming stream
            if hasattr(self.response_iterator, "cancel"):
                self.response_iterator.cancel()
            else:
                raise StreamException("Unable to stop the stream, as the stream object does not have a `cancel` method.")

    def _stream(self, stream_function: Callable[[Any], Any], request: Any) -> None:
        """
        Places any incoming messages in self.incoming_messages as they arrive.
        """
        try:
            if self.response_iterator is not None:
                # Handles the incoming stream
                for response in self.response_iterator:
                    self.incoming_messages.put(response)
            else:
                # There's no incoming stream, so send the request(s) and wait for the response
                response = stream_function(request)
                self.incoming_messages.put(response)
        except Exception as e:
            if isinstance(e, Call) and e.code() == StatusCode.CANCELLED:
                # The stream has been cancelled, so there's no need to stop it again
                pass
            else:
                self.stop_stream()
                self.received_exception = e
                # In case receive() is currently waiting for an incoming message, pass them the exception
                self.incoming_messages.put(e)
        finally:
            self.stream_finished = True
