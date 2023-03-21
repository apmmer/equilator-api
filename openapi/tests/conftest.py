
import inspect


import pytest
from _pytest.runner import runtestprotocol
from fastapi import FastAPI


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
    Automark tests as async.
    """

    for item in items:
        if inspect.iscoroutinefunction(item.function):
            item.add_marker(pytest.mark.asyncio)


@pytest.fixture
async def test_app_base_fixt() -> FastAPI:
    app = FastAPI()
    yield app
