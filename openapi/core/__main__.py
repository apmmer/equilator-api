import uvicorn
from loguru import logger

from openapi.core.settings import OpenapiSettings

logger.success('Starting api.')
uvicorn.run(
    'openapi.app:app',
    port=OpenapiSettings.uvicorn_port,
    host=OpenapiSettings.uvicorn_host,
    reload=True
)
logger.warning('The server is stopped.')
