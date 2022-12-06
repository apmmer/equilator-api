"""
    All current app endpoints will be added to the router here.
"""

from fastapi import APIRouter

from openapi.modules.auth.api.endpoints import auth
from openapi.modules.auth.settings import AuthSettings

router = APIRouter()

router.include_router(
    auth.router,
    prefix=AuthSettings.router_prefix
)
