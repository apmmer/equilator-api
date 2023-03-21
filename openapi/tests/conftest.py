import inspect
import pytest
from _pytest.runner import runtestprotocol
from fastapi import FastAPI
from openapi.modules.auth.dependencies import verify_api_key
from openapi.tests.auth import override_verify_api_key


class BaseTest:
    pass


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


@pytest.fixture
async def test_app_base_fixt() -> FastAPI:
    """
    Base app fixture with overridden dependencies.
    """

    app = FastAPI()
    app.dependency_overrides[verify_api_key] = override_verify_api_key
    yield app
