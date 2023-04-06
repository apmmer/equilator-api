from pytest import fixture
from typing import Dict
from openapi.modules.equilator.engine.equilator import Equilator
from openapi.tests.test_engine.cases import (
    flop_cases,
    turn_cases,
    river_cases,
    preflop_cases
)


invalid_cases = []
for cases in [
    flop_cases.invalid_flop_cases,
    turn_cases.invalid_turn_cases,
    river_cases.invalid_river_cases
]:
    invalid_cases.extend(cases)


class EquilatorTest:

    @fixture()
    def equilator_fixt(self) -> Equilator:
        return Equilator()

    @fixture(params=preflop_cases.preflop_cases)
    async def preflop_eq_case_fixt(self, request) -> Dict:
        return request.param

    @fixture(params=flop_cases.valid_flop_cases)
    async def flop_eq_case_fixt(self, request) -> Dict:
        return request.param

    @fixture(params=turn_cases.valid_turn_cases)
    async def turn_eq_case_fixt(self, request) -> Dict:
        return request.param

    @fixture(params=river_cases.valid_river_cases)
    async def river_eq_case_fixt(self, request) -> Dict:
        return request.param

    @fixture(params=invalid_cases)
    async def invalid_eq_case_fixt(self, request) -> Dict:
        return request.param
