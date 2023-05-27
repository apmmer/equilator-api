from typing import Dict

import pytest

from openapi.modules.equilator import range_converter
from openapi.tests.test_range_converter.conftest import RangeConverterTest


class TestCaseRangeConverter(RangeConverterTest):
    def test_strength_to_card_correct_cases(
        self,
        user_input_case_fixt: Dict
    ):
        result = range_converter.convert_from_string(
            user_input=user_input_case_fixt["range_definition"]
        )
        assert isinstance(result, list)
        assert len(result) == user_input_case_fixt["expected_length"]

    def test_card_strength(
        self,
        card_case_fixt: Dict
    ):
        res = range_converter.card_strength(
            card_or_suit=card_case_fixt["card"])
        assert res == card_case_fixt["strength"]

    def test_wrong_input_exception(
        self,
        wrong_user_input_case_fixt: Dict
    ):
        with pytest.raises(
            wrong_user_input_case_fixt["convert_from_string_error"]
        ):
            range_converter.convert_from_string(
                user_input=wrong_user_input_case_fixt["user_input"]
            )
