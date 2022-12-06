"""
    All current app endpoints will be added to the router here.
"""

from fastapi import APIRouter

from openapi.modules.monitoring.api.endpoints import sentry_check
from openapi.modules.monitoring.settings import SentrySettings

router = APIRouter()


for module in [sentry_check]:

    router.include_router(module.router, prefix=SentrySettings.router_prefix)
