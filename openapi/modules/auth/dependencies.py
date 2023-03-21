from fastapi import Depends
from fastapi.security import APIKeyHeader
from loguru import logger

from openapi.modules.auth.exceptions import InvalidApiKeyError
from openapi.modules.auth.settings import AuthSettings

api_key_scheme = APIKeyHeader(name='api-key')


def verify_api_key(api_key: str = Depends(api_key_scheme)):
    logger.info(
        f'Auth using api-key. api_key = {api_key}'
    )
    if api_key == AuthSettings.api_key:
        return True
    raise InvalidApiKeyError()
