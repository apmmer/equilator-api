from fastapi import Depends

from openapi.core.settings import TestSettings
from openapi.modules.auth.dependencies import api_key_scheme
from openapi.modules.auth.exceptions import InvalidApiKeyError, NoApiKeySent


async def override_verify_api_key(
    api_key: str = Depends(api_key_scheme)
):
    if api_key == TestSettings.test_api_key:
        return True
    elif api_key is None:
        raise NoApiKeySent()
    raise InvalidApiKeyError()
