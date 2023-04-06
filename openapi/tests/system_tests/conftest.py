import pytest
from fastapi import FastAPI

from openapi.modules.system.api.routes import router
from openapi.modules.system.settings import SystemSettings
from openapi.tests.conftest import BaseTest
from openapi.modules.system.api.dependencies import get_system_repo
from sqlalchemy.ext.asyncio.session import AsyncSession
from openapi.core.db.db_session import db_session



class FakeSystemRepo:
    async def get_now(self):
        return


class BaseSystemTest(BaseTest):
    url_prefix: str = f"http://test{SystemSettings.router_prefix}"


    @staticmethod
    async def override_get_system_repo():
        return FakeSystemRepo()

    @pytest.fixture
    async def test_app(
        self,
        test_app_base_fixt: FastAPI
    ) -> FastAPI:
        test_app_base_fixt.include_router(router)
        test_app_base_fixt.dependency_overrides[get_system_repo] = (
            BaseSystemTest.override_get_system_repo)
        yield test_app_base_fixt
