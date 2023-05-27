from typing import Dict

from fastapi import FastAPI
from pytest import fixture

from openapi.modules.designations.api.dependencies import get_designations_repo
from openapi.modules.designations.api.routes import router
from openapi.modules.designations.schemas.designations import Designation
from openapi.tests.conftest import BaseTest

wrong_post_data_cases = [
    {},
    {"range_definition": "asdf"},
    {"wrong field": "test"},
    {"range_definition": 123},
    {"range_definition": 0.5},
    {"range_definition": ["AA"]},
    {"range_definition": "test"}
]


correct_post_data_cases = [
    # basic definitions
    {
        "range_definition": "2h2d",
        "expected_length": 1,
        "expected_hash": (
            "0eef66ecc0e3e6aab3460ca0fee8f8ead2ce923ad83648eb0ded2a38f1a6fdff")
    },
    {
        "range_definition": "22",
        "expected_length": 6,
        "expected_hash": (
            "202678508ec7ca3d42b0c9b8f02777afdc8884815b373129704b173ef8fe1d2a")
    },
    {
        "range_definition": "22+",
        "expected_length": 78,
        "expected_hash": (
            "ca644b4cd7b4d45e18e350dab6e47ad93fe50e6ebfa899c536a8230292addab7")
    },
    {
        "range_definition": "88-22",
        "expected_length": 42,
        "expected_hash": (
            "5b32fae10b1193a57784b45848ec4a3c26254bf268af7a8ac227509010f1cd85")
    },
    {
        "range_definition": "AhJd",
        "expected_length": 1,
        "expected_hash": (
            "03ae3c907922cafcb77d4c10f1a0e4ffe11a5409ce56e412258dadc2bded2e3b")
    },
    {
        "range_definition": "AJo",
        "expected_length": 12,
        "expected_hash": (
            "d0eb2d666d0ecca883fbe810e29449ca9cbef048e7001b95cda27fe2d746540d")
    },
    {
        "range_definition": "AJo+",
        "expected_length": 36,
        "expected_hash": (
            "f46cec232d7de053ff1750b2e9a0263596505e6c972d4b7124cd127fe85f3a16")
    },
    {
        "range_definition": "A5o-A2o",
        "expected_length": 48,
        "expected_hash": (
            "cc0dc4ead310bd8fd7002796e3f7c20fb178052cb0a40ff83895147ed6ebcd81")
    },
    {
        "range_definition": "AhTh",
        "expected_length": 1,
        "expected_hash": (
            "87f45eddac012963573f4fff8ba15708d2d2d18b3b8f75048085b13b886a8e25")
    },
    {
        "range_definition": "ATs",
        "expected_length": 4,
        "expected_hash": (
            "e78960f7b349a7001fec202ec251a4ee34988e6059909eff4e7d09920d672215")
    },
    {
        "range_definition": "ATs+",
        "expected_length": 16,
        "expected_hash": (
            "7ae8902225c5d0cf01c716cf64f93beb10ed26adeb85169c0fb0316bf2b4a5c5")
    },
    {
        "range_definition": "A5s-A2s",
        "expected_length": 16,
        "expected_hash": (
            "52e524936b882ce5bbb44e37e16f787304bcb34b8af981cd7d9182f52224f66c")
    },
    {
        "range_definition": "all",
        "expected_length": 1326,
        "expected_hash": (
            "c92daa372b03b5dbd122d28529f2f656b0a378b28cafa7ca993dde66f4e7e8b9")
    },
    {
        "range_definition": "suited",
        "expected_length": 312,
        "expected_hash": (
            "614a41b855dfdadc42058edef936039703f61b5e6e11c9b8928603818ac84ef2")
    },
    {
        "range_definition": "offsuited",
        "expected_length": 936,
        "expected_hash": (
            "5a702cb85a07fcee4fc22d239801e693c444c4f88125ec77468c97c48165a131")
    },
    {
        "range_definition": "pockets",
        "expected_length": 78,
        "expected_hash": (
            "ca644b4cd7b4d45e18e350dab6e47ad93fe50e6ebfa899c536a8230292addab7")
    },
    # complex
    {
        "range_definition": "QQ+,AKs",
        "expected_length": 22,
        "expected_hash": (
            "bc447ec7d8f594f5cb0af48abe5beefff383b6eb71bc2fca8cad71bc03688db4")
    },
    {
        "range_definition": "A5s-A2s,AA,QQ,22,QTo",
        "expected_length": 46,
        "expected_hash": (
            "faa2531cd362396e87357800adb77cc0cab757681d85c73d49faa482fea0ea93")
    },
    {
        "range_definition": "77+,AKs,87s,QTs+",
        "expected_length": 64,
        "expected_hash": (
            "cc702139c8f4efcfaaf0f49cb3687dd75fe065c41a64e96fec341f7e0af04f3b")
    },
    {
        "range_definition": "22+,A7s+,KTs+,QTs+,JTs",
        "expected_length": 130,
        "expected_hash": (
            "e153810cf004084c7cd3c139079350a494072d9eccdec9854381708f38b39a34")
    },
    {
        "range_definition": "AhKh,AdAc,AhQh,Ah7d",
        "expected_length": 4,
        "expected_hash": (
            "2cd3309d1fdd76a943b0efb34804dd34b3831a0cfe6dc966f054bfd83fa1d763")
    },
    {
        "range_definition": "any2",
        "expected_length": 1326,
        "expected_hash": (
            "c92daa372b03b5dbd122d28529f2f656b0a378b28cafa7ca993dde66f4e7e8b9")
    }
]


wrong_get_many_params_cases = [
    {"limit": -1},
    {"offset": -2},
    {"limit": "test"},
    {"offset": "test"},
    {"limit": ["test"]},
    {"offset": ["test"]},
]


class FakeDesignationsRepo:
    default_designation = Designation(
            range_definition="AhAd",
            range_length=1,
            id="test"
        )

    async def add_an_item(self, data: Dict):
        self.default_designation.range_definition = data["range_definition"]
        return self.default_designation

    async def get_collection(self, *args, **kwargs):
        return [self.default_designation]

    async def delete_an_item(self, id):
        pass

    async def get_an_item(self, id):
        return self.default_designation


class DesignationsTest(BaseTest):
    base_url_prefix: str = "http://test"

    @fixture
    async def test_app_fixt(
        self,
        test_app_base_fixt: FastAPI
    ) -> FastAPI:
        async def fake_get_designations_repo():
            return FakeDesignationsRepo()

        test_app_base_fixt.include_router(router)
        test_app_base_fixt.dependency_overrides[
            get_designations_repo
        ] = fake_get_designations_repo
        yield test_app_base_fixt

    @fixture(params=wrong_post_data_cases)
    async def wrong_post_data_case_fixt(self, request) -> Dict:
        return request.param

    @fixture(params=correct_post_data_cases)
    async def post_data_case_fixt(self, request) -> Dict:
        return request.param

    @fixture(params=wrong_get_many_params_cases)
    async def wrong_get_many_params_case(self, request) -> Dict:
        return request.param
