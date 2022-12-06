"""
All current module endpoints will be added to the router here.
"""

from fastapi import APIRouter

from openapi.modules.ranges.api.endpoints import ranges
from openapi.modules.ranges.settings import RangesSettings

router = APIRouter()


for file in [ranges]:

    router.include_router(
        file.router,
        prefix=RangesSettings.router_prefix
    )
