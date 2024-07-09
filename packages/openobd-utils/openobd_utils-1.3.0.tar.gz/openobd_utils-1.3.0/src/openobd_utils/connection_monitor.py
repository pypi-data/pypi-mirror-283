from openobd import OpenOBDSession
from .stream_manager import StreamManager


class ConnectionMonitor(StreamManager):

    def __init__(self, openobd_session: OpenOBDSession, sample_size: int = 10):
        """
        Starts a stream which receives a ConnectionInformation message each second. Saves the most recently received
        ConnectionInformation messages, and allows them to be returned when requested.

        :param openobd_session: an active OpenOBDSession from which to receive connection information.
        :param sample_size: the maximum amount of ConnectionInformation messages that should be saved at a time.
        """
        super().__init__(openobd_session.open_connector_information_stream, outgoing_stream=False, incoming_stream=True)
        self.sample_size = sample_size
        self.connection_info_samples = []

    def get_connection_data(self) -> list:
        """
        Returns the latest ConnectionInformation messages. The amount of returned messages is dependent on this object's
        sample_size.

        :return: a list containing the latest ConnectionInformation messages, ordered from most recent to oldest.
        """
        # Add any new ConnectionInformation messages to the self.connection_info_samples list
        connection_sample = self.receive(block=False)
        while connection_sample is not None:
            self.connection_info_samples.append(connection_sample)
            connection_sample = self.receive(block=False)

        # Make sure the list does not exceed self.sample_size, by taking only the most recent messages
        self.connection_info_samples = self.connection_info_samples[-self.sample_size:]

        # Reverse the list, so the samples are ordered latest to oldest, and return it
        return self.connection_info_samples[::-1]
