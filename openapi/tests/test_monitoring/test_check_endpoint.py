import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient, Response

from openapi.core.settings import TestSettings
from openapi.modules.monitoring.settings import SentrySettings
from openapi.tests.test_monitoring.conftest import MonitoringTest


class Testsuite_check_sentry_endpoint(MonitoringTest):
    url_prefix: str = f"http://test{SentrySettings.router_prefix}"
    endpoint_url: str = "/check"

    async def test_endpoint_exists_and_returns_response(self, test_app: FastAPI):
        async with AsyncClient(app=test_app, base_url=self.url_prefix) as client:
            res = await client.get(self.endpoint_url)
            assert isinstance(res, Response)

    async def test_endpoint_returns_403_if_no_auth_token(self, test_app: FastAPI):
        async with AsyncClient(app=test_app, base_url=self.url_prefix) as client:
            res = await client.get(self.endpoint_url)
            assert res.status_code == status.HTTP_403_FORBIDDEN

    async def test_endpoint_returns_401_if_token_is_invalid(self, test_app: FastAPI):
        headers = {"api-key": f"invalid {TestSettings.test_api_key}"}
        async with AsyncClient(app=test_app, base_url=self.url_prefix) as client:
            res = await client.get(self.endpoint_url, headers=headers)
            assert res.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_endpoint_raised_exception_when_accessed(self, test_app: FastAPI):
        headers = {"api-key": f"{TestSettings.test_api_key}"}

        with pytest.raises(Exception):
            async with AsyncClient(app=test_app, base_url=self.url_prefix) as client:
                res = await client.get(self.endpoint_url, headers=headers)
