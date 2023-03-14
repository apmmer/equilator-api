"""
    All current module endpoints will be added to the router here.
"""

from fastapi import APIRouter

from openapi.modules.system.api.endpoints import system
from openapi.modules.system.settings import SystemSettings

router = APIRouter()


for module in [system]:

    router.include_router(module.router, prefix=SystemSettings.router_prefix)
