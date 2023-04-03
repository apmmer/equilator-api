from fastapi import APIRouter, Depends
from loguru import logger

from openapi.core.exceptions import DefaultException
from openapi.core.settings import OpenapiSettings
from openapi.modules.auth.dependencies import verify_api_key

router = APIRouter()


@router.get(
    "/check",
    status_code=500,
    dependencies=[Depends(verify_api_key)]
)
async def trigger_error():
    """
    Raises an Exception to capture it in Sentry
    """

    if OpenapiSettings.monitoring_enabled is False:
        raise DefaultException(
            detail="Monitoring is not enabled in settings!"
        )
    logger.warning("Raised test sentry exception.")
    raise Exception("Sentry test error.")
