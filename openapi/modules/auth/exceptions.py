from fastapi import status

from openapi.core.exceptions import DefaultException


class InvalidApiKeyError(DefaultException):
    detail: str = "Invalid api_key."
    status_code: status = status.HTTP_401_UNAUTHORIZED


class NoApiKeySent(DefaultException):
    detail: str = "No api-key sent."
    status_code: status = status.HTTP_403_FORBIDDEN
