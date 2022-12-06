"""
This module contains functions for converting user input
to a List of valid poker hand combos.
"""

from loguru import logger
from openapi.modules.equilator.exceptions import ConverterError
from typing import List, Optional


RANKS = "23456789TJQKA"
SUITS = "hdcs"


def card_strength(card_or_suit: str) -> int:
    """
    Translates card to it's strength to understand
    which card has higher rank.

    Args:
        card_or_suit (str): a card like: "A", "K" or "3"

    Returns:
        int: abstract strength of a card
    """

    ordered_ranks = "23456789TJQKA"
    strength = None
    if card_or_suit in ordered_ranks:
        strength = ordered_ranks.index(card_or_suit)
    else:
        strength = "scdh".index(card_or_suit)
    return strength


def strength_to_card(strength: int) -> str:
    """
    Converts back abstract hand's strength to card.
    The "strength" must be validated before
    calling this function.

    Args:
        strength (int): abstract strength of hand from 0 to 12

    Returns:
        str: a card w/o suit
    """

    return "23456789TJQKA"[strength]


def convert_from_string(user_input: str) -> List[str]:
    """
    Main function of this module. Translates user raw input string
    to a sorted List of combos.
    BTW collects exceptions if raised to create good description of
    final exception, to know whats wrong with input.

    Args:
        user_input (str): short designation of the range of hands

    Syntax:
        "2h2d" - single combo of a pocket pair (1 combo)
        "22" - single pocket pair (including all suits:  6 combos)
            Correct inputs: "33", "JJ", "AA"
        "22+" - all pocket pairs combos from AA to 22 (78 combos)
        "88-22" - all pocket pairs between 88 and 22 (42 combos)
            Note: higher pocket should be first, "22-88" - is wrong input
        "AhJd" - Single ofsuited combo. (1 combo)
            Note: the highest rank can be written second, "JdAh" is valid,
                but it will be replaced to AhJd automatically.
        "AJo" - All combos of offsuited AJ (AhJd, AhJc...AsJc: 12 combos)
            Note: higher rank should be first, "QAo" - is wrong input
        "AJo+" - all offsuited Ace-high hands with kickers from J to K,
            (AJo, AQo, AKo: 36 combos)
            Note: higher rank should be first, "QAo+" - is wrong input
            Correct inputs: "A2o+" (144 combos), "K3o+" (120 combos),
                "75o+" (24 combos), "87o+" (12 combos)
        "A5o-A2o" - all offsuited Ace-high hands with kickers from 5 to 2,
            (A2o, A3o, A4o, A5o: 48 combos)
            Note: higher kicker rank should be first, "A2o-A5o" - is wrong
            Correct inputs: "A7o-A5o" (36 combos), "KJo-KTo" (24 combos)
        "AhTh" - Single suited combo. (1 combo)
            Note: the highest rank can be written second, "ThAh" is valid,
                but it will be replaced to AhTh automatically.
        "ATs+" - all suited Ace-high hands with kickers from T to K,
            (ATs, AJs, AQs, AKs: 16 combos)
            Note: higher rank should be first, "TAs+" - is wrong input
            Correct inputs: "A3s+" (44 combos), "K4s+" (36 combos)
        "A5s-A2s" - all suited Ace-high hands with kickers from 5 to 2,
            (A2s, A3s, A4s, A5s: 16 combos)
            Note: higher kicker rank should be first, "A2s-A5s" - is wrong
            Correct inputs: "A7s-A5s" (12 combos), "KJs-KTs" (8 combos)
        "all" - all 1326 combos. Also valid: "any2", "any two", "anytwo"
        "suited" - all suited hands ()
        "offsuited" - all offsuited hands ()
        "pockets" - all pocket pairs (the same as 22+)
    Correct examples:
        "55+,AKo" - 72 combos
        "8h8d,7d7s,2h2d,AJo+,55-44,AA-KK" - 63 combos.

    Raises:
        ValueError: when encountered some errors. Creates good description.

    Returns:
        List[str]: a sorted list of combos.
    """

    adjusted_input = adjust_input(
        user_input=user_input
    )

    # a fragment is any representation of a player's range (small part)
    fragments_list: List[str] = adjusted_input.split(",")

    resulting_list: List[str] = []
    repeated_hands: List[str] = []
    wrong_fragments_errors: List[str] = []

    for fragment in fragments_list:
        try:
            translated_fragment: List[str] = (
                translate_fragment(fragment=fragment)
            )
        except ValueError as ex:
            wrong_fragments_errors.append(str(ex))
            continue

        for hand in translated_fragment:
            if hand not in resulting_list:
                resulting_list.append(hand)
            elif hand not in repeated_hands:
                repeated_hands.append(hand)

    if wrong_fragments_errors:
        raise ValueError(
            "Got errors during parsing: "
            f"{[e for e in wrong_fragments_errors]}."
        )
    if repeated_hands:
        raise ValueError(
            "Some of hands in range were repeated: "
            f"{[h for h in repeated_hands]}. "
            "It is not optimal, please check input."
        )

    return sorted(resulting_list)


def adjust_input(user_input: str) -> str:
    """
    Removes unnecessary symbols from user_input,
    also replaces super-short input (like "all") to
    correct designation to continue processing.

    Args:
        user_input (str): short designation of the range of hands

    Returns:
        str: replaced user_input with correct designation.
    """

    if not user_input:
        raise ConverterError("Got empty user_input.")

    user_input = user_input.replace(" ", "")
    # extra comma added
    if user_input[-1] == ",":
        user_input = user_input[:-1]

    if user_input in ["any two", "anytwo", "all", "any2"]:
        user_input = (
            "22+,A2s+,K2s+,Q2s+,J2s+,T2s+,92s+,82s+,72s+,62s+,52s+,"
            "42s+,32s+,A2o+,K2o+,Q2o+,J2o+,T2o+,92o+,82o+,72o+,62o+,"
            "52o+,42o+,32o+"
        )
    elif user_input == "offsuited":
        user_input = (
            "A2o+,K2o+,Q2o+,J2o+,T2o+,92o+,82o+,72o+,62o+,52o+,42o+,32o+"
        )
    elif user_input == "suited":
        user_input = (
            "A2s+,K2s+,Q2s+,J2s+,T2s+,92s+,82s+,72s+,62s+,52s+,42s+,32s+"
        )
    elif user_input == "pockets":
        user_input = "22+"
    return user_input


def translate_fragment(fragment: str) -> List[str]:
    """
    Tryes to convert a fragment into List of combos,
    according declared syntax.

    Args:
        fragment (str): short part of raw user input,
            usually with length from 2 to 10

    Raises:
        ConverterError: exception with detailed description.

    Returns:
        List[str]: List of combos

    Example:
        >>>translate_fragment(fragment="AKs")
        >>>['AhKh', 'AdKd', 'AcKc', 'AsKs']
    """

    translated_fragment: Optional[List[str]] = None
    if not fragment:
        raise ConverterError(
            "Got empty fragment, which is forbidden.")

    if len(fragment) == 2:
        # expected pocket here
        translated_fragment = get_pocket_combos(
            fragment=fragment)
    elif len(fragment) == 3:
        # expected pp+ or suited/ofsuited range
        if (
            fragment[2] == "+"
            and fragment[0] == fragment[1]
        ):
            # expected range of pockets
            translated_fragment = get_pockets_plus_combos(
                fragment=fragment)
        elif (
            fragment[2] == "s"
            and fragment[0] != fragment[1]
        ):
            # expected suited hand
            logger.info(f"{fragment=}")
            translated_fragment = get_suited_combos(
                fragment=fragment)
        elif (
            fragment[2] == "o"
            and fragment[0] != fragment[1]
        ):
            logger.info(f"OFFSUITED {fragment=}")
            translated_fragment = get_offsuited_combos(
                fragment=fragment)
    elif len(fragment) == 4:
        if (
            fragment[3] == "+"
            and fragment[2] == "o"
            and fragment[0] != fragment[1]
        ):
            # expected offsuited hand plus
            logger.info(f"{fragment=}")
            translated_fragment = get_offsuited_combos_plus(
                fragment=fragment)
        elif (
            fragment[3] == "+"
            and fragment[2] == "s"
            and fragment[0] != fragment[1]
        ):
            # expected suited hand plus
            logger.info(f"{fragment=}")
            translated_fragment = get_suited_combos_plus(
                fragment=fragment)
        elif (
            fragment[1] in SUITS
            and fragment[3] in SUITS
        ):
            # expected raw combo input like "AsKc"
            logger.info(f"{fragment=}")
            _validate_ranks(ranks=f"{fragment[0]}{fragment[2]}")
            translated_fragment = [fragment]
    elif len(fragment) == 5:
        if (
            fragment[2] == "-"
            and fragment[0] == fragment[1]
            and fragment[3] == fragment[4]
        ):
            # expected pockets range from XX to YY
            translated_fragment = get_pockets_from_to(
                fragment=fragment)
    elif len(fragment) == 7:
        if fragment[3] == "-" and fragment[0] == fragment[4]:
            # expected from-to
            if fragment[2] == "o" and fragment[6] == "o":
                # expected offsuited range from-to
                translated_fragment = get_offsuited_from_to(
                    fragment=fragment)
            elif fragment[2] == "s" and fragment[6] == "s":
                # expected suited range from-to
                translated_fragment = get_suited_from_to(
                    fragment=fragment)

    if translated_fragment is None:
        raise ConverterError(
            f"Fragment ({fragment}) cannot be interpreted.")
    return translated_fragment


def get_suited_from_to(fragment: str) -> List[str]:
    """
    Parses fragment like "AKs-A2s"

    Args:
        fragment (str): a part of the opponent's range
            representation, example: "AKo" or "22+"

    Returns:
        List[str]: List of combos (strings)
    """

    _validate_ranks(ranks=f"{fragment[0]}{fragment[1]}")
    _validate_ranks(ranks=f"{fragment[4]}{fragment[5]}")
    suited_combos: List[str] = []
    kicker_strength1 = card_strength(fragment[1])
    kicker_strength2 = card_strength(fragment[5])
    for kicker_strength in range(
        kicker_strength2,
        kicker_strength1 + 1
    ):
        suited_combos.extend(
            make_suits_for_suited_hand(
                hand=f"{fragment[0]}{strength_to_card(kicker_strength)}"
            )
        )
    return suited_combos


def get_offsuited_from_to(fragment: str) -> List[str]:
    """
    Parses fragment like "AKo-A2o"

    Args:
        fragment (str): a part of the opponent's range
            representation, example "AKo" or "22+"

    Returns:
        List[str]: List of combos (strings), like ['AhKd', ... , 'Ad2c']
    """

    _validate_ranks(ranks=f"{fragment[0]}{fragment[1]}")
    _validate_ranks(ranks=f"{fragment[4]}{fragment[5]}")

    offsuited_combos: List[str] = []
    kicker_strength1 = card_strength(fragment[1])
    kicker_strength2 = card_strength(fragment[5])
    for kicker_strength in range(
        kicker_strength2,
        kicker_strength1 + 1
    ):
        offsuited_combos.extend(
            make_suits_for_offsuited_hand(
                hand=f"{fragment[0]}{strength_to_card(kicker_strength)}"
            )
        )
    return offsuited_combos


def get_pockets_from_to(fragment: str) -> List[str]:
    """
    Parses fragment like "77-22"

    Args:
        fragment (str): a part of the opponent's range
            representation, example "AKo" or "22+"

    Returns:
        List[str]: List of combos (strings), like ['7h7d', ... , '2d2c']
    """

    _validate_ranks(ranks=f"{fragment[0]}{fragment[3]}")
    pockets_combos: List[str] = []
    lowest_pocket_strength = card_strength(fragment[3])
    highest_pocket_strength = card_strength(fragment[0])
    for strength in range(
        lowest_pocket_strength,
        highest_pocket_strength + 1
    ):
        pockets_combos.extend(
            make_suits_for_pocket(strength_to_card(strength))
        )
    return pockets_combos


def get_suited_combos_plus(fragment: str) -> List[str]:
    """
    Produces combos for designation like "65s+".

    Args:
        fragment (str): a part of the opponent's range
            representation, example "AKo" or "22+"

    Returns:
        List[str]: List of combos, like ['6h5h', ... , '3d2d']
    """

    _validate_ranks(ranks=fragment[:2])

    suited_combos: List[str] = []
    for strength in range(
        card_strength(fragment[1]),
        card_strength(fragment[0])
    ):
        second_card = strength_to_card(strength=strength)
        suited_combos.extend(
            make_suits_for_suited_hand(
                hand=f"{fragment[0]}{second_card}"
            )
        )
    return suited_combos


def get_pocket_combos(fragment: str) -> List[str]:
    """
    Parses designation of a single pocket ('22' or 'KK')

    Args:
        fragment (str): a part of the opponent's range
            representation, example "AKo" or "22+"

    Raises:
        ValueError: error with description

    Returns:
        List[str]: List of combos, like ['6h6d', ... , '6c6s']
    """

    if fragment[0] != fragment[1]:
        raise ValueError(
            "Fragment with 2 symbols must contain a pocket pair")

    for symbol in fragment:
        if symbol not in "23456789TJQKA":
            raise ValueError(
                f"Fragment ({fragment}) contains wrong symbol ({symbol})")
    return make_suits_for_pocket(pocket_rank=fragment[0])


def make_suits_for_pocket(pocket_rank: str) -> List[str]:
    """
    Produces all pocket combos for given pocket rank.
    Input should be validated on higher level.

    Args:
        pocket_rank (str): rank of a pocket, like "2"

    Returns:
        List[str]: List of 6 combos (strings)
    """

    pocket_combos: List[str] = []
    for suits in ["hd", "hc", "hs", "dc", "ds", "cs"]:
        pocket_combos.append(
            f"{pocket_rank}{suits[0]}{pocket_rank}{suits[1]}")
    return pocket_combos


def make_suits_for_suited_hand(hand: str) -> List[str]:
    """
    Produces suited combos for given hand like "AK" or "QT".
    Input should be validated on higher level.

    Args:
        hand (str): very short hand representation: "32" or "AK"

    Returns:
        List[str]: List of combos
    """

    logger.info(f"making suits for {hand}")
    hand_combos: List[str] = []
    for suit in "hdcs":
        hand_combos.append(f"{hand[0]}{suit}{hand[1]}{suit}")
    return hand_combos


def _validate_ranks(ranks: str) -> True:
    """
    Validates given ranks record.
    Checks whether the specified ranks can be used

    Args:
        ranks (str): Two ranks (string with len=2)

    Raises:
        ValueError: exception with description.

    Returns:
        True: all is Ok, validation was successfull.
    """

    for rank in ranks:
        if rank not in "23456789TJQKA":
            msg = f'Record ({ranks}): rank must be in "23456789TJQKA".'
            raise ValueError(msg)

    if card_strength(ranks[1]) > card_strength(ranks[0]):
        msg = f"Record ({ranks}): higher rank must be written first."
        raise ValueError(msg)
    return True


def make_suits_for_offsuited_hand(hand: str) -> List[str]:
    """
    Produces offsuited combos for given hand like "AK" or "QT"
    Input should be validated on higher level.

    Args:
        hand (str): hand like "AK" or "QT"

    Returns:
        List[str]: List of 12 combos.
    """

    logger.info(f"making suits for {hand}")
    rank1, rank2 = hand[0], hand[1]
    possible_suits = [
        "hd", "dh", "hc", "ch", "hs", "sh",
        "dc", "cd", "ds", "sd", "cs", "sc"]
    hand_combos = [
        f"{rank1}{suit[0]}{rank2}{suit[1]}" for suit in possible_suits
    ]
    return hand_combos


def get_offsuited_combos(fragment: str) -> List[str]:
    """
    Returns correct combos for designation like "XYo"

    Args:
        fragment (str): a part of the opponent's range
            representation, example "AKo" or "22+"

    Returns:
        List[str]: List of all 16 offsuited combos (strings).
    """

    _validate_ranks(ranks=fragment[:2])
    return make_suits_for_offsuited_hand(
        hand=fragment[:2]
    )


def get_offsuited_combos_plus(fragment: str) -> List[str]:
    """
    Produces combos for designation like "65o+".

    Args:
        fragment (str): a part of the opponent's range
            representation, example "AKo" or "22+"

    Returns:
        List[str]: List of combos like ['8h2d', ... , '8h3d']
    """

    _validate_ranks(ranks=fragment[:2])

    offsuited_combos: List[str] = []
    for strength in range(
        card_strength(fragment[1]),
        card_strength(fragment[0])
    ):
        second_card = strength_to_card(strength=strength)
        offsuited_combos.extend(
            make_suits_for_offsuited_hand(
                hand=f"{fragment[0]}{second_card}"
            )
        )
    return offsuited_combos


def get_suited_combos(fragment: str) -> List[str]:
    """
    Returns correct combos for designation like "XYs",
    examples: "AKs", "QTs", "72s"

    Args:
        fragment (str): a part of the opponent's range
            representation, example "AKo" or "22+"

    Raises:
        ValueError: error with details

    Returns:
        List[str]: List of 4 suited combos
    """

    # ensure higher rank goes first
    if card_strength(fragment[1]) > card_strength(fragment[0]):
        msg = f"Fragment ({fragment}): higher rank must be written first."
        raise ValueError(msg)

    logger.info(f"making suits for {fragment}")
    return make_suits_for_suited_hand(
        hand=fragment[:2]
    )


def get_pockets_plus_combos(fragment: str) -> List[str]:
    """
    Fragment should be like "xx+"

    Args:
        fragment (str): a part of the opponent's range
            representation, example "AKo" or "22+"

    Raises:
        ValueError: error with details

    Returns:
        List[str]: List of all pockets combos according designation.
    """

    for symbol in fragment[:2]:
        if symbol not in "23456789TJQKA":
            raise ValueError(
                f"Fragment ({fragment}) contains wrong symbol ({symbol})")

    pockets_combos: List[str] = []
    for strength in range(card_strength(fragment[0]), 13):
        pockets_combos.extend(
            make_suits_for_pocket(
                pocket_rank=strength_to_card(strength)
            )
        )
    return pockets_combos
