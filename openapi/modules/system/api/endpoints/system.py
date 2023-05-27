from typing import Dict

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from openapi.core.schemas import HTTPExceptionModel
from openapi.modules.system.api.dependencies import get_system_repo
from openapi.modules.system.repositories.system import SystemRepo
from openapi.modules.auth.dependencies import verify_api_key
from openapi.core.db.db_session import db_session

router = APIRouter(
    dependencies=[Depends(verify_api_key)]
)


@router.get(
    "/healthcheck",
    responses={
        500: {"model": HTTPExceptionModel},
    },
    status_code=status.HTTP_200_OK
)
async def healthcheck(
    repo: SystemRepo = Depends(get_system_repo)
):
    await repo.get_now()
    return {"status": "OK"}
