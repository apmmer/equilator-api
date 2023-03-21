import numpy as np

from openapi.modules.equilator.engine.bin import precompiled


def calc_equity_postflop(
    stage: int,
    OOP_range_array: np.ndarray,
    IP_range_array: np.ndarray,
    board: np.ndarray
) -> np.ndarray:
    """
    """

    return precompiled.calc_equity_postflop(
        stage,
        OOP_range_array,
        IP_range_array,
        board
    )


def calc_equity_preflop(
    full_preflop_matrix: np.ndarray,
    OOP_range_array: np.ndarray,
    IP_range_array: np.ndarray
) -> np.ndarray:
    """
    Doc
    """

    return precompiled.calc_equity_preflop(
        full_preflop_matrix,
        OOP_range_array,
        IP_range_array
    )


def get_card_representation(card: str) -> int:
    return precompiled.get_card_representation(card)
