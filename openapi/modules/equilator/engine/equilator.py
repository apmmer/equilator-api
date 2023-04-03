from time import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from loguru import logger

from openapi.modules.equilator.engine import precompiled_wrapper
from openapi.modules.equilator.engine.data_getter import DataGetter


class Equilator:

    def __init__(
        self,
        full_preflop_matrix: np.ndarray = DataGetter.load_preflop_matrix()
    ) -> None:
        self.full_preflop_matrix = full_preflop_matrix

    def get_equity_report_array(
        self,
        oop_range_array: np.ndarray,
        ip_range_array: np.ndarray,
        board: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """
        Returns not readable array,
        but containing all necessary equity results.
        Those results can be used by another software, but for API response
        or for read must be adapted.

        Args:
            oop_range_array (np.ndarray): out of position player's range,
                converted to numeric array
            ip_range_array (np.ndarray): in position player's range,
                converted to numeric array
            board (Optional[np.ndarray], optional): Board cards,
                converted to numeric type.
                Defaults to None.
                If None - that means stage is 'preflop'.

        Returns:
            np.ndarray: not readable array, but containing
            all necessary equity results.
        """

        stage: int = 0 if board is None else len([c for c in board if c]) - 2

        tik = time()
        if stage == 0:
            result_array = precompiled_wrapper.calc_equity_preflop(
                self.full_preflop_matrix,
                oop_range_array,
                ip_range_array
            )
        else:
            result_array = precompiled_wrapper.calc_equity_postflop(
                stage=stage,
                OOP_range_array=oop_range_array,
                IP_range_array=ip_range_array,
                board=board
            )

        logger.success(
            f"Equilation time = {time() - tik}, EQ = {result_array[-1]}"
        )
        return result_array

    def get_equity_report_dict(
        self,
        oop_valid_definition: Dict[str, float],
        ip_valid_definition: Dict[str, float],
        valid_board: List[str]
    ) -> Dict[str, Any]:
        """
        Operates with readable player's poker ranges, calculates and
        produces readable equity report with each 'OOP' player hand's
        and total equity.

        Args:
            oop_valid_definition (Dict[str, float]): validated range
                definition of OOP (out of position) player
            ip_valid_definition (Dict[str, float]): validated range
                definition of IP (in position) player
            valid_board (List[str]): current board for computations

        Returns:
            Dict[str, Any]: equity report, ready to serialize
        """

        # adjust weights
        # look if some hands can not be played at all
        oop_playable_hands, oop_not_playable_hands = self._get_playable_hands(
            valid_definition=oop_valid_definition,
            board=valid_board
        )
        ip_range_list, _ = self._get_playable_hands(
            valid_definition=ip_valid_definition,
            board=valid_board
        )
        # getting arrays
        oop_range_array = self._get_range_array(
            valid_definition=oop_valid_definition,
            playable_hands=oop_playable_hands
        )
        ip_range_array = self._get_range_array(
            valid_definition=ip_valid_definition,
            playable_hands=ip_range_list
        )
        board_array: Optional[np.ndarray] = self._convert_board_list_to_array(
            board=valid_board
        )

        # getting equity results
        resulting_dict = self._parse_equity_array(
            oop_range_array=oop_range_array,
            ip_range_array=ip_range_array,
            oop_playable_hands=oop_playable_hands,
            oop_not_playable_hands=oop_not_playable_hands,
            board=board_array
        )

        return resulting_dict

    def _parse_equity_array(
        self,
        oop_range_array: np.ndarray,
        ip_range_array: np.ndarray,
        oop_playable_hands: List[str],
        oop_not_playable_hands: List[str],
        board: Optional[np.ndarray] = None,
    ) -> Dict[str, Any]:
        """
        Encapsulates logic of equity report (np.ndarray) parsing.
        """

        # getting equity report (array)
        result_array = self.get_equity_report_array(
            oop_range_array=oop_range_array,
            ip_range_array=ip_range_array,
            board=board
        )
        # declaring future readable report
        resulting_dict: Dict[str, Any] = {"hands_equity": {}}

        # parsing array, setting values in resulting_dict
        total_equity_exists = False
        for i, hand in enumerate(oop_playable_hands):
            result_in_array = result_array[i]
            if result_in_array >= 0:
                hand_equity = result_in_array
                total_equity_exists = True
            else:
                hand_equity = None
            resulting_dict["hands_equity"][hand] = hand_equity

        if total_equity_exists:
            resulting_dict["total_equity"] = result_array[-1]
        else:
            resulting_dict["total_equity"] = None

        for hand in oop_not_playable_hands:
            resulting_dict["hands_equity"][hand] = None

        return resulting_dict

    def _get_playable_hands(
        self,
        valid_definition: Dict[str, float],
        board: List[str]
    ) -> Tuple[List[str], List[str]]:
        """
        Excludes hands from range, which can not be played in corrent board.
        Returns 2 lists: playable and not playable.
        """

        playable_hands = []
        not_playable_hands = []
        for hand, weight in valid_definition.items():
            if weight and hand[:2] not in board and hand[2:] not in board:
                playable_hands.append(hand)
            else:
                not_playable_hands.append(hand)
        return playable_hands, not_playable_hands

    def _get_range_array(
        self,
        valid_definition: Dict[str, float],
        playable_hands: List[str]
    ) -> np.ndarray:
        """
        Converts typical python list into numeric numpy array.
        Numeric array will provide faster computations in compiled module.
        """

        player_range_array = np.empty(
            (len(playable_hands), 3),
            dtype=np.float32
        )
        for i, hand in enumerate(playable_hands):
            player_range_array[i][0] = (
                precompiled_wrapper.get_card_representation(hand[:2])
            )
            player_range_array[i][1] = (
                precompiled_wrapper.get_card_representation(hand[2:])
            )
            player_range_array[i][2] = valid_definition[hand]

        return player_range_array

    def _convert_board_list_to_array(
        self, board: List[str]
    ) -> Optional[np.ndarray]:
        """
        Converts typical python list into numeric numpy array.
        Numeric array will provide faster computations in compiled module.
        """

        board_array = None
        if board:
            board_array = np.zeros(5, dtype=np.float32)
            for i, card in enumerate(board):
                board_array[i] = (
                    precompiled_wrapper.get_card_representation(card)
                )
        return board_array
