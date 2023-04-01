from typing import Dict

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from openapi.core.schemas import HTTPExceptionModel
from openapi.modules.system.api.dependencies import get_system_session
from openapi.modules.system.repositories.system import SystemRepo

router = APIRouter()


@router.get(
    "/healthcheck",
    responses={
        500: {"model": HTTPExceptionModel},
    },
    response_model=Dict,
    status_code=status.HTTP_200_OK,
)
async def healthcheck(
    session: AsyncSession = Depends(get_system_session)
):
    """
    Makes simple DB request to check connection.
    """

    repo_manager = SystemRepo(db_sess=session)
    await repo_manager.test_get_now()
    return {"Status": "OK"}
