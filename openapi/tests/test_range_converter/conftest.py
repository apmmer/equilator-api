from openapi.tests.test_designations.conftest import correct_post_data_cases
from pytest import fixture
from typing import Dict
from openapi.modules.equilator.exceptions import ConverterError


cards_cases = [
    {
        "card": "2",
        "strength": 0
    },
    {
        "card": "3",
        "strength": 1
    },
    {
        "card": "4",
        "strength": 2
    },
    {
        "card": "5",
        "strength": 3
    },
    {
        "card": "6",
        "strength": 4
    },
    {
        "card": "7",
        "strength": 5
    },
    {
        "card": "8",
        "strength": 6
    },
    {
        "card": "9",
        "strength": 7
    },
    {
        "card": "T",
        "strength": 8
    },
    {
        "card": "J",
        "strength": 9
    },
    {
        "card": "Q",
        "strength": 10
    },
    {
        "card": "K",
        "strength": 11
    },
    {
        "card": "A",
        "strength": 12
    },
    {
        "card": "h",
        "strength": 3
    },
    {
        "card": "d",
        "strength": 2
    },
    {
        "card": "c",
        "strength": 1
    },
    {
        "card": "s",
        "strength": 0
    }
]


converter_error_cases = [
    {
        "user_input": "",
        "convert_from_string_error": ConverterError
    },
    {
        "user_input": "AKss",
        "convert_from_string_error": ConverterError
    },
    {
        "user_input": "sss",
        "convert_from_string_error": ConverterError
    },
    {
        "user_input": "asdf",
        "convert_from_string_error": ConverterError
    },
    {
        "user_input": "23",
        "convert_from_string_error": ValueError
    },
    {
        "user_input": "AhTh,AhTh,",
        "convert_from_string_error": ValueError
    },
    {
        "user_input": "AhTh,,AhTs,",
        "convert_from_string_error": ConverterError
    },
    {
        "user_input": "22,AhTs,33,,",
        "convert_from_string_error": ConverterError
    },
    {
        "user_input": "LL",
        "convert_from_string_error": ValueError
    },
    {
        "user_input": "EE",
        "convert_from_string_error": ValueError
    },
    {
        "user_input": "LhLs",
        "convert_from_string_error": ValueError
    },
    {
        "user_input": "YcYs",
        "convert_from_string_error": ValueError
    },
    {
        "user_input": "KsAs",
        "convert_from_string_error": ValueError
    },
    {
        "user_input": "5hKs",
        "convert_from_string_error": ValueError
    },
    {
        "user_input": "9dJs",
        "convert_from_string_error": ValueError
    },
    {
        "user_input": "67s",
        "convert_from_string_error": ValueError
    },
    {
        "user_input": "KAs",
        "convert_from_string_error": ValueError
    },
    {
        "user_input": "PP+",
        "convert_from_string_error": ValueError
    },
    {
        "user_input": "KYo+",
        "convert_from_string_error": ValueError
    },
]


class RangeConverterTest:
    @fixture(params=correct_post_data_cases)
    async def user_input_case_fixt(self, request) -> Dict:
        return request.param

    @fixture(params=cards_cases)
    async def card_case_fixt(self, request) -> Dict:
        return request.param

    @fixture(params=converter_error_cases)
    async def wrong_user_input_case_fixt(self, request) -> Dict:
        return request.param
