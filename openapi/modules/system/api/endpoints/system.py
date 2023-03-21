from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from openapi.core.schemas import HTTPExceptionModel
from openapi.modules.system.api.dependencies import get_system_session
from openapi.modules.system.repositories.system import SystemRepo
from openapi.modules.auth.dependencies import verify_api_key

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
    session: AsyncSession = Depends(get_system_session)
):
    repo = SystemRepo(model=None)
    await repo.get_now(existing_session=session)
    return {"status": "OK"}
