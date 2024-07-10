
class OpenOBDException(Exception):
    """
    Base class for all exceptions that can be raised when using the OpenOBD library.
    """
    pass


class OpenOBDInvalidArgumentsException(OpenOBDException):
    pass
