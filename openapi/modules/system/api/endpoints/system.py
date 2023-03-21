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
    status_code=status.HTTP_200_OK,
)
async def healthcheck(session: AsyncSession = Depends(get_system_session)):
    repo_manager = SystemRepo(db_sess=session)
    await repo_manager.get_now()
    return {"status": "OK"}
