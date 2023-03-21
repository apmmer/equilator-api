from openapi.core.exceptions import DefaultException


class ConverterError(DefaultException):
    """
    This class is used for any exception in range_converter module.
    Detail should be provided 'on place'.
    """

    status_code: int = 400
