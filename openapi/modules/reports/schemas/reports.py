from pydantic import confloat, constr, Field, PositiveInt, validator
from typing import Dict, List, Optional
from openapi.core.exceptions import PydanticValidationError
from openapi.core.schemas import ImprovedBaseModel


class ReportsPostBody(ImprovedBaseModel):
    """
    This scheme contains the necessary attributes for equity calculation
    and used as a POST-body for request.
    """

    hero_range_id: PositiveInt = Field(
        ...,
        title="Hero range ID",
        description="ID of a range of target player (hero)",
        example=1
    )
    opponent_range_id: PositiveInt = Field(
        ...,
        title="Opponent's range ID",
        description="ID of a range of second player (opponent)",
        example=2
    )
    board: List[constr(min_length=2, max_length=2)] = Field(
        ...,
        title="Board",
        description=(
            "A list of cards on the board. Variants: "
            "Preflop = 0 cards, "
            "Flop = exactly 3 cards, "
            "Turn = 4 cards, "
            "River = 5 cards. "
            "Each card should be unique and exist in standart 52-cards deck."
        ),
        example=["Ah", "Kd", "Qc", "Js"]
    )

    @validator("board")
    def validate_board(cls, input_board):
        if len(input_board) not in (0, 3, 4, 5):
            raise PydanticValidationError(
                detail="Board cards count should be in (0, 3, 4, 5)."
            )

        wrong_cards = []
        for card in input_board:
            rank, suit = card[0], card[1]
            if rank not in "AKQJT98765432" or suit not in "hdcs":
                wrong_cards.append(card)
        if wrong_cards:
            raise PydanticValidationError(
                detail=(
                    f"Unknown board cards designation(s): {wrong_cards}. "
                    "Ensure rank is in 'AKQJT98765432' and suit is in 'hdcs'")
            )

        if len(set(input_board)) != len(input_board):
            raise PydanticValidationError(
                detail="Duplication of board cards is prohibited."
            )
        return input_board


class EquityReport(ImprovedBaseModel):
    """
    Schema for equilator results. Result will not be saved in DB.
    """

    hands_equity: Optional[Dict[str, Optional[confloat(ge=0, le=1)]]] = Field(
        None,
        title="Hands equity",
        description="Equity map for each hand in range"
    )
    total_equity: Optional[confloat(ge=0, le=1)] = Field(
        None,
        title="Total equity"
    )

    @validator("hands_equity")
    def round_hands_equity(cls, hands_equity):
        for hand, value in hands_equity.items():
            if value:
                hands_equity[hand] = round(value, 6)
        return hands_equity

    @validator("total_equity")
    def round_total_equity(cls, value):
        if value:
            value = round(value, 6)
        return value
