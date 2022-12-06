"""
All current module endpoints will be added to the router here.
"""

from fastapi import APIRouter

from openapi.modules.reports.api.endpoints import reports
from openapi.modules.reports.settings import EquityReportsSettings

router = APIRouter()


for file in [reports]:

    router.include_router(
        file.router,
        prefix=EquityReportsSettings.router_prefix
    )
