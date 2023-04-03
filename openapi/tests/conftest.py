import inspect
import pytest
from _pytest.runner import runtestprotocol
from fastapi import FastAPI
from openapi.modules.auth.dependencies import verify_api_key
from openapi.tests.auth import override_verify_api_key
from openapi.core.settings import TestSettings
from sqlalchemy.ext.asyncio.session import AsyncSession
from openapi.core.db.db_session import db_session
import asyncio
from loguru import logger
from openapi.tests import alembic_scripts
import alembic.config


class BaseTest:
    test_api_key: str = TestSettings.test_api_key

    @pytest.fixture(scope="session")
    async def db_session(self) -> AsyncSession:
        async with db_session() as sess:
            yield sess

    @pytest.fixture(scope="session")
    def event_loop(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
        yield loop

    def setup(self):
        alembic_scripts.setup_db()

    def teardown(self):
        alembic_scripts.teardown_db()

    @staticmethod
    def setup_db():
        logger.info("Setup test DB schema.")
        alembic.config.main(argv=(["upgrade", "head"]))
        logger.info("DB schema success setup finished")

    @staticmethod
    def teardown_db():
        logger.info("Teardown process started")
        alembic.config.main(argv=(["downgrade", "base"]))
        logger.info("All migrations downgraded.")

    @pytest.fixture
    async def test_app_base_fixt(self) -> FastAPI:
        """
        Base app fixture with overridden dependencies.
        """

        app = FastAPI()
        app.dependency_overrides[verify_api_key] = override_verify_api_key
        yield app


def pytest_runtest_protocol(item, nextitem):
    """
    Adds timing for output records.
    """

    reports = runtestprotocol(item, nextitem=nextitem)
    for report in reports:
        if report.when == "call":
            report_string = f"\ntime = {round(report.duration, 4)} s"
            print(report_string, end="")
    return True


def pytest_collection_modifyitems(config, items):
    """
    Automark tests as async if coroutine.
    """

    for item in items:
        if inspect.iscoroutinefunction(item.function):
            item.add_marker(pytest.mark.asyncio)



