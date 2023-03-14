from typing import List

from openapi.core.exceptions import DefaultException
from openapi.modules.equilator.engine.equilator import Equilator
from openapi.modules.ranges.repositories.ranges import RangesRepo
from openapi.modules.ranges.schemas.ranges import WeightedRange
from openapi.modules.reports.schemas.reports import (EquityReport,
                                                     ReportsPostBody)


class EquityReportsHandler:

    def __init__(
        self,
        ranges_repo: RangesRepo = RangesRepo(),
        equilator: Equilator = Equilator()
    ) -> None:
        self.ranges_repo = ranges_repo
        self.equilator = equilator

    async def create_equity_report(
        self,
        data: ReportsPostBody
    ) -> EquityReport:

        definitions = await self.get_valid_definitions(
            hero_range_id=data.hero_range_id,
            opponent_range_id=data.opponent_range_id
        )

        # looking for correct definitions
        oop_valid_definition, ip_valid_definition = (
            (definitions[0], definitions[1])
            if definitions[0].id == data.hero_range_id
            else (definitions[1], definitions[0])
        )

        # getting equity results
        resulting_dict = self.equilator.get_equity_report_dict(
            oop_valid_definition=oop_valid_definition.definition,
            ip_valid_definition=ip_valid_definition.definition,
            valid_board=data.board
        )

        # returning valid item
        return EquityReport.parse_obj(resulting_dict)

    async def get_valid_definitions(
        self,
        hero_range_id: int,
        opponent_range_id: int
    ) -> List[WeightedRange]:

        if hero_range_id == opponent_range_id:
            raise DefaultException(
                detail="Input ranges's IDs must be different.",
                status_code=422
            )

        definitions: List[WeightedRange] = await self.ranges_repo.get_many(
            in_filters={"id": [hero_range_id, opponent_range_id]}
        )

        if len(definitions) < 2:
            got_ids = [model.id for model in definitions]
            missed_ids = [
                item_id for item_id in [hero_range_id, opponent_range_id]
                if item_id not in got_ids
            ]
            raise DefaultException(
                detail=f"Objects with IDs ({missed_ids}) were not found.",
                status_code=406
            )
        elif len(definitions) > 2:
            raise DefaultException(
                detail=(
                    "Faced unknown error during getting "
                    "definitions with given ids."
                )
            )
        return definitions
