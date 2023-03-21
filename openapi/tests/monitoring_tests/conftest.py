import pytest
from fastapi import FastAPI

from openapi.modules.monitoring.api.routes import router


class FakeSentrySDK:
    init_called_times = 0

    def init(self, *args, **kwargs):
        self.init_called_times += 1
        self.args = args
        self.kwargs = kwargs


@pytest.fixture
def fake_sentry_sdk_fixt() -> FakeSentrySDK:
    return FakeSentrySDK()


@pytest.fixture
async def test_app(
    test_app_base_fixt: FastAPI
) -> FastAPI:

    test_app_base_fixt.include_router(router)
    yield test_app_base_fixt
