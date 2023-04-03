import numpy as np

from openapi.modules.equilator.engine.bin import precompiled


def calc_equity_postflop(
    stage: int,
    OOP_range_array: np.ndarray,
    IP_range_array: np.ndarray,
    board: np.ndarray
) -> np.ndarray:
    """
    Calls precompiled function to perform equity computations.
    Input values must be validated before usage.

    Args:
        stage (int): 0 - preflop, 1 - flop, 2 - turn, 3 - river
        OOP_range_array (np.ndarray): array containing each hand
            of out-of-position player (and weights).
        IP_range_array (np.ndarray): array containing each hand
            of in-position player (and weights).
        board (np.ndarray): board cards (numeric)

    Returns:
        np.ndarray: new array with equity results.
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
    Calls precompiled function to perform preflop equity computations.
    Input values must be validated before usage.

    Args:
        full_preflop_matrix (np.ndarray): encrypted matrix,
            containing each hand precalculated preflop equity
        OOP_range_array (np.ndarray): array containing each hand
            of out-of-position player (and weights).
        IP_range_array (np.ndarray): array containing each hand
            of in-position player (and weights).

    Returns:
        np.ndarray: new array with equity results.
    """

    return precompiled.calc_equity_preflop(
        full_preflop_matrix,
        OOP_range_array,
        IP_range_array
    )


def get_card_representation(card: str) -> int:
    """
    Translates string card designation into numeric
    according it's rank and suit.

    Args:
        card (str): a card designation, like 'As' or '2d'

    Returns:
        int: number associated with this card, examples: 172 or 244
    """

    return precompiled.get_card_representation(card)
