from fastapi import FastAPI, status
from httpx import Response, AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession
from openapi.tests.system_tests.conftest import BaseSystemTest

app = FastAPI()


class TestSystem(BaseSystemTest):
    endpoint_url: str = "/healthcheck"

    # async def test_endpoint_exists_and_returns_response(self, test_app: FastAPI):
    #     async with AsyncClient(app=test_app, base_url=self.url_prefix) as client:
    #         res = await client.get(self.endpoint_url)
    #         assert isinstance(res, Response)

    # async def test_endpoint_returns_401_if_token_is_invalid(self, test_app: FastAPI):
    #     headers = {"api-key": f"invalid {self.test_api_key}"}
    #     async with AsyncClient(app=test_app, base_url=self.url_prefix) as client:
    #         res = await client.get(self.endpoint_url, headers=headers)
    #         assert res.status_code == 401

    # async def test_endpoint_returns_403_if_no_auth_token(self, test_app: FastAPI):
    #     async with AsyncClient(app=test_app, base_url=self.url_prefix) as client:
    #         res = await client.get(self.endpoint_url)
    #         assert res.status_code == status.HTTP_403_FORBIDDEN

    # async def test_endpoint_returns_type_dict(
    #     self,
    #     test_app: FastAPI,
    #     db_session: AsyncSession
    # ):
    #     async with AsyncClient(app=test_app, base_url=self.url_prefix) as client:
    #         res = await client.get(
    #             self.endpoint_url,
    #             headers={"api-key": f"{self.test_api_key}"}
    #         )
    #         res_json = res.json()
    #     assert isinstance(res_json, dict)

    async def test_endpoint_returns_exact_dict_data(self, test_app: FastAPI):
        async with AsyncClient(app=test_app, base_url=self.url_prefix) as client:
            res = await client.get(
                self.endpoint_url,
                headers={"api-key": f"{self.test_api_key}"}
            )
            res_json = res.json()
        assert res_json == {"status": "OK"}

#     async def test_endpoint_returns_correct_status(self, test_app: FastAPI):
#         async with AsyncClient(app=test_app, base_url=self.url_prefix) as client:
#             res = await client.get(
#                 self.endpoint_url,
#                 headers={"api-key": f"{self.test_api_key}"}
#             )
#         assert res.status_code == status.HTTP_200_OK
