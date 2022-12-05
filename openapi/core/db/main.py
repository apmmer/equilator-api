"""
The most important entities for using models and
database should be created here
"""

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import declarative_base
from openapi.core.settings import OpenapiSettings
from loguru import logger


logger.info(
    f"Creating engine for db-url: {OpenapiSettings.database_url}"
)
engine: AsyncEngine = create_async_engine(
    OpenapiSettings.database_url,
    echo=OpenapiSettings.sql_engine_echo
)

Base = declarative_base()
