"""
All current module endpoints will be added to the router here.
"""

from fastapi import APIRouter

from openapi.modules.designations.api.endpoints import designations
from openapi.modules.designations.settings import DesignationsSettings

router = APIRouter()


for file in [designations]:

    router.include_router(
        file.router,
        prefix=DesignationsSettings.router_prefix
    )
