from fastapi import FastAPI
from openapi.modules.designations.settings import DesignationsSettings
from httpx import AsyncClient, Response
from openapi.tests.test_designations.conftest import DesignationsTest
from openapi.core.settings import TestSettings
from typing import Dict
from openapi.modules.designations.schemas.designations import Designation


class TestCaseDesignationsCreateEndpoint(DesignationsTest):
    endpoint_url: str = f"{DesignationsSettings.router_prefix}"

    async def test_endpoint_exists_and_returns_response(
        self, test_app_fixt: FastAPI
    ):
        async with AsyncClient(
            app=test_app_fixt, base_url=self.base_url_prefix
        ) as client:
            res = await client.post(self.endpoint_url)
        assert isinstance(res, Response)

    async def test_endpoint_returns_403_if_no_apikey(
        self, test_app_fixt: FastAPI
    ):
        async with AsyncClient(
            app=test_app_fixt, base_url=self.base_url_prefix
        ) as client:
            res = await client.post(self.endpoint_url)
        assert res.status_code == 403

    async def test_endpoint_returns_401_if_wrong_auth_token(
        self, test_app_fixt: FastAPI
    ):
        async with AsyncClient(
            app=test_app_fixt, base_url=self.base_url_prefix
        ) as client:
            res = await client.post(
                self.endpoint_url,
                headers={
                    "api-key": (
                        f"wrong{TestSettings.test_api_key}"
                    )
                }
            )
        assert res.status_code == 401

    async def test_endpoint_returns_422_if_wrong_data(
        self, test_app_fixt: FastAPI, wrong_post_data_case_fixt: Dict
    ):
        async with AsyncClient(
            app=test_app_fixt, base_url=self.base_url_prefix
        ) as client:
            res = await client.post(
                self.endpoint_url,
                headers={
                    "api-key": (
                        f"{TestSettings.test_api_key}"
                    )
                },
                data=wrong_post_data_case_fixt
            )
        assert res.status_code == 422

    async def test_endpoint_returns_201_if_correct_data(
        self, test_app_fixt: FastAPI, post_data_case_fixt: Dict
    ):
        async with AsyncClient(
            app=test_app_fixt, base_url=self.base_url_prefix
        ) as client:
            res = await client.post(
                self.endpoint_url,
                headers={
                    "api-key": (
                        f"{TestSettings.test_api_key}"
                    )
                },
                json=post_data_case_fixt
            )
        assert res.status_code == 201

    async def test_endpoint_returns_correct_scheme_and_result_with_fake_repo(
        self, test_app_fixt: FastAPI, post_data_case_fixt: Dict
    ):
        async with AsyncClient(
            app=test_app_fixt, base_url=self.base_url_prefix
        ) as client:
            res = await client.post(
                self.endpoint_url,
                headers={
                    "api-key": (
                        f"{TestSettings.test_api_key}"
                    )
                },
                json=post_data_case_fixt
            )

        res_json = res.json()
        assert Designation.parse_obj(res_json)
        assert res_json["range_definition"] == (
            post_data_case_fixt["range_definition"])
