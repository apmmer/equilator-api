from fastapi import status

from openapi.core.exceptions import DefaultException


class InvalidApiKeyError(DefaultException):
    detail: str = "Invalid api_key."
    status_code: status = status.HTTP_401_UNAUTHORIZED
