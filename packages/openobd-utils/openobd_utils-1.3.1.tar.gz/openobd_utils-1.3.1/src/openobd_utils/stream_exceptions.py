from openobd import OpenOBDException


class StreamException(OpenOBDException):
    """
    Base class for all exceptions that can be raised when using streams.
    """
    pass


class StreamStoppedException(StreamException):
    pass


class StreamTimeoutException(StreamException):
    pass
