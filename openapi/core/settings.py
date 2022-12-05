from os import getenv
from pathlib import Path
from typing import List

from dotenv import load_dotenv

from openapi.utils.config_utils import convert_to_boolean
from loguru import logger

BASE_PATH = Path(__file__).resolve().parent.parent
PROJECT_PATH = BASE_PATH.resolve().parent

logger.info(f"Loading env from {PROJECT_PATH}")
load_dotenv(f'{PROJECT_PATH}/.env')


class OpenapiSettings:
    """
    General settings for main application.
    """

    database_url: str = getenv(
        "DATABASE_URL",
        getenv("TEST_DATABASE_URL")
    )

    included_modules: List[str] = [
        'designations',
        # 'auth',
        # 'monitoring',
        'reports',
        'system',
        'ranges'
    ]
    uvicorn_port: int = int(getenv('UVICORN_PORT', 8000))
    uvicorn_host: str = getenv('UVICORN_HOST', '0.0.0.0')
    router_prefix: str = '/api/v1'
    title: str = getenv('API_TITLE', 'OpenAPI')
    version: str = getenv('API_VERSION', 'v0.1.0')
    description: str = "Api for equilator engine."
    # next variable should be changed to real domain name
    # like ['http://ngrok.io', 'https://ngrok.io']
    CORS_middleware_origins: List[str] = [
        'http://localhost:3000',
        'http://localhost:8000',
    ]
    CORS_middleware_methods: List[str] = ["*"]
    CORS_middleware_headers: List[str] = ["*"]
    monitoring_enabled: bool = convert_to_boolean(
        getenv("MONITORING_ENABLED", False))
    sql_engine_echo: bool = convert_to_boolean(
        getenv("SQL_ENGINE_ECHO", False))


class TestSettings:
    """
        Settings for tests.
    """

    tests_path: str = f"{BASE_PATH}/tests"
    server_type: str = getenv('SERVER_TYPE', 'test')
    # modules for testing
    included_modules: List[str] = [
        'designations',
        # 'auth',
        # 'monitoring',
        'reports',
        'system',
        'ranges'
    ]
    test_api_key: str = 'test'
