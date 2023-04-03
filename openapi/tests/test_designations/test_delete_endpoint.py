from fastapi import FastAPI
from openapi.modules.designations.settings import DesignationsSettings
from httpx import AsyncClient, Response
from openapi.tests.test_designations.conftest import DesignationsTest
from openapi.core.settings import TestSettings


class TestCaseDesignationsDeleteEndpoint(DesignationsTest):
    endpoint_url: str = f"{DesignationsSettings.router_prefix}/1"

    async def test_endpoint_exists_and_returns_response(
        self, test_app_fixt: FastAPI
    ):
        async with AsyncClient(
            app=test_app_fixt, base_url=self.base_url_prefix
        ) as client:
            res = await client.delete(self.endpoint_url)
        assert isinstance(res, Response)

    async def test_endpoint_returns_403_if_no_apikey(
        self, test_app_fixt: FastAPI
    ):
        async with AsyncClient(
            app=test_app_fixt, base_url=self.base_url_prefix
        ) as client:
            res = await client.delete(self.endpoint_url)
        assert res.status_code == 403

    async def test_endpoint_returns_401_if_wrong_auth_token(
        self, test_app_fixt: FastAPI
    ):
        async with AsyncClient(
            app=test_app_fixt, base_url=self.base_url_prefix
        ) as client:
            res = await client.delete(
                self.endpoint_url,
                headers={
                    "api-key": (
                        f"wrong{TestSettings.test_api_key}"
                    )
                }
            )
        assert res.status_code == 401

    async def test_endpoint_returns_200_and_correct_result_when_success(
        self, test_app_fixt: FastAPI
    ):
        async with AsyncClient(
            app=test_app_fixt, base_url=self.base_url_prefix
        ) as client:
            res = await client.delete(
                self.endpoint_url,
                headers={
                    "api-key": (
                        f"{TestSettings.test_api_key}"
                    )
                }
            )
        assert res.status_code == 202
        assert res.json() == {"accepted deletion of id": "1"}
