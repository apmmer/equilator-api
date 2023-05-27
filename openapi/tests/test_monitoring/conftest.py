import pytest
from fastapi import FastAPI

from openapi.modules.monitoring.api.routes import router
from openapi.tests.conftest import BaseTest

class FakeSentrySDK:
    init_called_times = 0

    def init(self, *args, **kwargs):
        self.init_called_times += 1
        self.args = args
        self.kwargs = kwargs


class MonitoringTest(BaseTest):

    @pytest.fixture
    def fake_sentry_sdk_fixt(self) -> FakeSentrySDK:
        return FakeSentrySDK()

    @pytest.fixture
    async def test_app(
        self,
        test_app_base_fixt: FastAPI
    ) -> FastAPI:

        test_app_base_fixt.include_router(router)
        yield test_app_base_fixt
