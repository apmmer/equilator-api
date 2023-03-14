from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from openapi.core.settings import OpenapiSettings
from openapi.routes.router import router

# this should be setup before app declaration
if OpenapiSettings.monitoring_enabled:
    from openapi.modules.monitoring.setup import setup_sentry
    logger.info('Enabling monitoring.')
    setup_sentry()


app = FastAPI(
    title=OpenapiSettings.title,
    description=OpenapiSettings.description,
    version=OpenapiSettings.version
)

# avoiding CORS errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=OpenapiSettings.CORS_middleware_origins,
    allow_credentials=True,
    allow_methods=OpenapiSettings.CORS_middleware_methods,
    allow_headers=OpenapiSettings.CORS_middleware_headers,
)

app.include_router(router)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass
