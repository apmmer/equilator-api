import importlib

from fastapi import APIRouter

from openapi.core.settings import OpenapiSettings

router = APIRouter()


# go through all necessary modules and include them to api
for module_name in OpenapiSettings.included_modules:
    module = importlib.import_module(
        f"openapi.modules.{module_name}.api.routes"
    )
    router.include_router(
        module.router,
        prefix=OpenapiSettings.router_prefix
    )
