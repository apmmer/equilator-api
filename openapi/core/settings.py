"""
Module for general settings
"""


from os import getenv
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from loguru import logger

from openapi.utils.config_utils import convert_to_boolean

BASE_PATH = Path(__file__).resolve().parent.parent
PROJECT_PATH = BASE_PATH.resolve().parent

logger.info(f"Loading alternative env from {PROJECT_PATH}/.env")
load_dotenv(f"{PROJECT_PATH}/.env")


class OpenapiSettings:
    """
    General settings for main application.
    """

    database_url: str = getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://root:root@equilator_api_db:5432/eq_db"
    )

    included_modules: List[str] = [
        'designations',
        'monitoring',
        'reports',
        'system',
        'ranges'
    ]
    uvicorn_port: int = int(getenv("UVICORN_PORT", 8000))
    uvicorn_host: str = getenv("UVICORN_HOST", "0.0.0.0")
    router_prefix: str = "/api/v1"
    title: str = getenv("API_TITLE", "Equilator API")
    version: str = getenv("API_VERSION", "v0.1.0")
    description: str = (
        "API for using the equalator engine "
        "and converting/storing ranges."
    )
    # next variable should be changed to real domain name
    # like ["http://ngrok.io", "https://ngrok.io"]
    CORS_middleware_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    CORS_middleware_methods: List[str] = ["*"]
    CORS_middleware_headers: List[str] = ["*"]

    # next is usually True in prod
    monitoring_enabled: bool = convert_to_boolean(
        getenv("MONITORING_ENABLED", False))
    sql_engine_echo: bool = convert_to_boolean(
        getenv("SQL_ENGINE_ECHO", False))
    # This is a limitation for querying db (list of items)
    # if more than this value is requested
    # pagination will be used
    list_items_db_limit: str = 5000


class TestSettings:
    """
    Settings for tests.
    """

    tests_path: str = f"{BASE_PATH}/tests"

    # modules for testing
    included_modules: List[str] = [
        'designations',
        'monitoring',
        'reports',
        'system',
        'ranges'
    ]
    test_api_key: str = "test"
