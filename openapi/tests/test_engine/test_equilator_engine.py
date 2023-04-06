from typing import Dict
from openapi.tests.test_engine.conftest import EquilatorTest
from openapi.modules.equilator.engine.equilator import Equilator


class TestCaseRangeConverter(EquilatorTest):

    def test_equilator_output_on_preflop_cases(
        self,
        equilator_fixt: Equilator,
        preflop_eq_case_fixt: Dict
    ):
        expected_result = preflop_eq_case_fixt.pop("total_equity")
        equity_report = equilator_fixt.get_equity_report_dict(
            **preflop_eq_case_fixt
        )

        # numpy.float32 != python float
        res = float(equity_report["total_equity"])
        assert round(res, 4) == round(expected_result, 4)

    def test_equilator_output_on_flop_cases(
        self,
        equilator_fixt: Equilator,
        flop_eq_case_fixt: Dict
    ):
        expected_result = flop_eq_case_fixt.pop("total_equity")
        equity_report = equilator_fixt.get_equity_report_dict(
            **flop_eq_case_fixt
        )

        res = float(equity_report["total_equity"])
        assert round(res, 4) == round(expected_result, 4)

    def test_equilator_output_on_turn_cases(
        self,
        equilator_fixt: Equilator,
        turn_eq_case_fixt: Dict
    ):
        expected_result = turn_eq_case_fixt.pop("total_equity")
        equity_report = equilator_fixt.get_equity_report_dict(
            **turn_eq_case_fixt
        )

        res = float(equity_report["total_equity"])
        assert round(res, 4) == round(expected_result, 4)

    def test_equilator_output_on_river_cases(
        self,
        equilator_fixt: Equilator,
        river_eq_case_fixt: Dict
    ):
        expected_result = river_eq_case_fixt.pop("total_equity")
        equity_report = equilator_fixt.get_equity_report_dict(
            **river_eq_case_fixt
        )

        res = float(equity_report["total_equity"])
        assert round(res, 4) == round(expected_result, 4)

    def test_equilator_output_on_invalid_cases(
        self,
        equilator_fixt: Equilator,
        invalid_eq_case_fixt: Dict
    ):
        invalid_eq_case_fixt.pop("total_equity")
        expected_result = None
        equity_report = equilator_fixt.get_equity_report_dict(
            **invalid_eq_case_fixt
        )
        res = equity_report["total_equity"]
        assert res == expected_result
