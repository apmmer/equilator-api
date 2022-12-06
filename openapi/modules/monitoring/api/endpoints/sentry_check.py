from fastapi import APIRouter, Depends
from loguru import logger

from openapi.modules.auth.api.dependencies import verify_api_key

router = APIRouter()


@router.get("/check", status_code=500, dependencies=[Depends(verify_api_key)])
async def trigger_error():
    logger.warning("Raised test sentry exception.")
    raise Exception("Sentry test error.")
