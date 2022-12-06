import numpy as np
from numba import float32, float64, njit, uint8, uint16, uint32, vectorize
from numba.pycc import CC

# cc = CC(extension_name='precompiled_test', )


@njit(cache=True)
def calculate_w_of_array(array, default_slot=2):
    """
        Available for nJIT.
        Calculates total weight of player's range. Returns it.
    """
    w = 0
    for h in range(len(array)):
        w += array[h][default_slot]
    return w


@njit(cache=True)
def from_string_to_numbers(string):
    """
        Available for nJIT.
        If will see a point in the text = returns float, else = int.
    """

    number = 0.0
    before_point_count = 0
    after_point_count = 0
    was_point = False
    for char in string:
        if char == ".":
            was_point = True
        elif (
            char == "0"
            or char == "1"
            or char == "2"
            or char == "3"
            or char == "4"
            or char == "5"
            or char == "6"
            or char == "7"
            or char == "8"
            or char == "9"
        ):
            if was_point is False:
                before_point_count += 1
            else:
                after_point_count += 1
    if before_point_count > 0:
        was_point = False
    if before_point_count + after_point_count == 0:
        print(
            "[from_string_to_numbers]\n     zero numbers detected in text. returned 0"
        )
        return 0

    after_point_counter = 1
    for char in string:
        if char == "." or before_point_count == 0:
            was_point = True
        if was_point is False:
            # if char=='0':
            #     continue
            if char == "1":
                number += 1 * 10 ** (before_point_count - 1)
                before_point_count -= 1
            elif char == "2":
                number += 2 * 10 ** (before_point_count - 1)
                before_point_count -= 1
            elif char == "3":
                number += 3 * 10 ** (before_point_count - 1)
                before_point_count -= 1
            elif char == "4":
                number += 4 * 10 ** (before_point_count - 1)
                before_point_count -= 1
            elif char == "5":
                number += 5 * 10 ** (before_point_count - 1)
                before_point_count -= 1
            elif char == "6":
                number += 6 * 10 ** (before_point_count - 1)
                before_point_count -= 1
            elif char == "7":
                number += 7 * 10 ** (before_point_count - 1)
                before_point_count -= 1
            elif char == "8":
                number += 8 * 10 ** (before_point_count - 1)
                before_point_count -= 1
            elif char == "9":
                number += 9 * 10 ** (before_point_count - 1)
                before_point_count -= 1
        if was_point is True:
            # if char=='0':
            #     continue
            if char == "1":
                number += 1 / (10 ** (after_point_counter))
                after_point_counter += 1
            elif char == "2":
                number += 2 / (10 ** (after_point_counter))
                after_point_counter += 1
            elif char == "3":
                number += 3 / (10 ** (after_point_counter))
                after_point_counter += 1
            elif char == "4":
                number += 4 / (10 ** (after_point_counter))
                after_point_counter += 1
            elif char == "5":
                number += 5 / (10 ** (after_point_counter))
                after_point_counter += 1
            elif char == "6":
                number += 6 / (10 ** (after_point_counter))
                after_point_counter += 1
            elif char == "7":
                number += 7 / (10 ** (after_point_counter))
                after_point_counter += 1
            elif char == "8":
                number += 8 / (10 ** (after_point_counter))
                after_point_counter += 1
            elif char == "9":
                number += 9 / (10 ** (after_point_counter))
                after_point_counter += 1
    if after_point_count == 0:
        number = int(number)

    return number


@njit(cache=True)
def card_strength(card):
    """
    Available for nJIT.
    Returns a certain sequential number of the card,
    based on a custom hierarchy
    """

    # переводит карты А, К и подобные в ЧИСЛА (int от 2 до 14)
    if card == "A":
        return 14
    elif card == "K":
        return 13
    elif card == "Q":
        return 12
    elif card == "J":
        return 11
    elif card == "T":
        return 10
    elif card == "9":
        return 9
    elif card == "8":
        return 8
    elif card == "7":
        return 7
    elif card == "6":
        return 6
    elif card == "5":
        return 5
    elif card == "4":
        return 4
    elif card == "3":
        return 3
    elif card == "2":
        return 2
    elif card == "h":
        return 4
    elif card == "d":
        return 3
    elif card == "c":
        return 2
    elif card == "s":
        return 1
    else:
        return 0


@njit(cache=True)
def strength_to_card(strength):
    """
        Available for nJIT.
        From custom hierarchy to -> directly text view
    """

    if strength > 100:
        rank = strength // 10
        suit = strength % 10
        if rank == 24:
            rank = "A"
        elif rank == 23:
            rank = "K"
        elif rank == 22:
            rank = "Q"
        elif rank == 21:
            rank = "J"
        elif rank == 20:
            rank = "T"
        elif rank == 19:
            rank = "9"
        elif rank == 18:
            rank = "8"
        elif rank == 17:
            rank = "7"
        elif rank == 16:
            rank = "6"
        elif rank == 15:
            rank = "5"
        elif rank == 14:
            rank = "4"
        elif rank == 13:
            rank = "3"
        elif rank == 12:
            rank = "2"
        else:
            rank = "2"
        if suit == 4:
            suit = "h"
        elif suit == 3:
            suit = "d"
        elif suit == 2:
            suit = "c"
        else:
            suit = "s"
        return rank + suit
    else:
        if strength == 14:
            return "A"
        elif strength == 13:
            return "K"
        elif strength == 12:
            return "Q"
        elif strength == 11:
            return "J"
        elif strength == 10:
            return "T"
        elif strength == 9:
            return "9"
        elif strength == 8:
            return "8"
        elif strength == 7:
            return "7"
        elif strength == 6:
            return "6"
        elif strength == 5:
            return "5"
        elif strength == 4:
            return "4"
        elif strength == 3:
            return "3"
        elif strength == 2:
            return "2"


@njit(cache=True)
def jcard_strength(card):
    """
        Available for nJIT.
        Returns a certain sequential number of the card, based on a custom hierarchy.
        Works with a pair of cards.
    """

    rank = card[0]
    suit = card[1]
    r = 0
    s = 0
    if rank == "A":
        r = 240
    if rank == "K":
        r = 230
    if rank == "Q":
        r = 220
    if rank == "J":
        r = 210
    if rank == "T":
        r = 200
    if rank == "9":
        r = 190
    if rank == "8":
        r = 180
    if rank == "7":
        r = 170
    if rank == "6":
        r = 160
    if rank == "5":
        r = 150
    if rank == "4":
        r = 140
    if rank == "3":
        r = 130
    if rank == "2":
        r = 120
    if suit == "h":
        s = 4
    if suit == "d":
        s = 3
    if suit == "c":
        s = 2
    if suit == "s":
        s = 1
    return r + s


@njit(cache=True)
def convert_range_from_text_to_weighted_array(weighted_range_text):
    """
        Returns an array of numeric hands with weights from input
    """

    player_range_array = np.zeros((1326, 3), dtype=float32)
    text_temp = ""
    hand_number = 0
    for char in weighted_range_text:
        if char == "[" or char == "]" or char == "," or char == " ":
            continue
        elif char == "(":
            card1, card2 = text_temp[:2], text_temp[2:]
            card1, card2 = jcard_strength(card1), jcard_strength(card2)
            player_range_array[hand_number][0], player_range_array[hand_number][1] = (
                card1,
                card2,
            )
            text_temp = ""
        elif char == ")":
            w = from_string_to_numbers(text_temp)
            player_range_array[hand_number][2] = w
            text_temp = ""
            hand_number += 1
        else:
            text_temp += char

    weighted_hands_count = 0
    for h in range(len(player_range_array)):
        if player_range_array[h][2] > 0:
            weighted_hands_count += 1
    real_player_range_array = np.zeros((weighted_hands_count, 3), dtype=float32)
    current_hand_number = 0
    for h in range(len(player_range_array)):
        if player_range_array[h][2] != 0:
            real_player_range_array[current_hand_number] = player_range_array[h]
            current_hand_number += 1
    return real_player_range_array


@njit(cache=True)
def make_all_board_possible_cards_array():
    """
        creates 52-cards array and set default weigth, returns it
    """

    all_cards_array_with_weigth = np.ones((52, 4), dtype=uint16)
    for i in range(13):
        for j in range(4):
            all_cards_array_with_weigth[i * 4 + j][0] = i * 10 + 120 + j + 1
    return all_cards_array_with_weigth


@njit(cache=True)
def any_pair(r):
    """
        Returns the strength of a combination in which a pair may be present
    """

    r1, r2, r3, r4, r5, r6, r7 = r[0], r[1], r[2], r[3], r[4], r[5], r[6]
    if r1 != r2 and r2 != r3 and r3 != r4 and r4 != r5 and r5 != r6 and r6 != r7:
        return r1 * 28561 + r2 * 2197 + r3 * 169 + r4 * 13 + r5

    if r1 == r4:
        return 3150000 + r1 * 13 + r5

    elif r2 == r5 or r3 == r6 or r4 == r7:
        return 3150000 + r4 * 13 + r1

    else:
        if r1 == r3:
            if r4 == r5:
                return 2700000 + r1 * 13 + r4

            if r5 == r6 or r6 == r7:
                return 2700000 + r1 * 13 + r6

            return 1350000 + r1 * 169 + r4 * 13 + r5
        elif r2 == r4:
            if r5 == r6 or r6 == r7:
                return 2700000 + r2 * 13 + r6

            return 1350000 + r2 * 169 + r1 * 13 + r5

        elif r3 == r5:
            if r1 == r2:
                return 2700000 + r3 * 13 + r1

            if r6 == r7:
                return 2700000 + r3 * 13 + r6

            return 1350000 + r5 * 169 + r1 * 13 + r2
        elif r4 == r6:
            if r1 == r2 or r2 == r3:
                return 2700000 + r4 * 13 + r2

            return 1350000 + r5 * 169 + r1 * 13 + r2

        elif r5 == r7:
            if r1 == r2:
                return 2700000 + r5 * 13 + r1

            if r2 == r3 or r3 == r4:
                return 2700000 + r5 * 13 + r3

            return 1350000 + r5 * 169 + r1 * 13 + r2

        else:
            if r1 == r2:
                if r3 == r4:
                    return 900000 + r1 * 169 + r3 * 13 + r5

                if r4 == r5:
                    return 900000 + r1 * 169 + r4 * 13 + r3

                if r5 == r6 or r6 == r7:
                    return 900000 + r1 * 169 + r6 * 13 + r3

                return 450000 + r1 * 2197 + r3 * 169 + r4 * 13 + r5

            elif r2 == r3:
                if r4 == r5:
                    return 900000 + r2 * 169 + r4 * 13 + r1

                if r5 == r6 or r6 == r7:
                    return 900000 + r2 * 169 + r6 * 13 + r1

                return 450000 + r2 * 2197 + r1 * 169 + r4 * 13 + r5

            elif r3 == r4:
                if r5 == r6 or r6 == r7:
                    return 900000 + r3 * 169 + r6 * 13 + r1

                return 450000 + r3 * 2197 + r1 * 169 + r2 * 13 + r5

            elif r4 == r5:
                if r6 == r7:
                    return 900000 + r4 * 169 + r6 * 13 + r1

                return 450000 + r4 * 2197 + r1 * 169 + r2 * 13 + r3

            elif r5 == r6 or r6 == r7:
                return 450000 + r6 * 2197 + r1 * 169 + r2 * 13 + r3

            return r1 * 28561 + r2 * 2197 + r3 * 169 + r4 * 13 + r5


@njit(cache=True)
def current_strength_of_this_hand(zeros):
    """
        Counts and returns the final strength of the combination.
        Input - a special prepared data array with shape (5,7).
        This func contains a lot of repetitions, but it works faster with them than if you take them out separately.
    """
    # 0=cards(empty),1=r(empty),2=s(empty),3=ss(empty),4=full board

    board1 = zeros[4]
    (
        zeros[0][0],
        zeros[0][1],
        zeros[0][2],
        zeros[0][3],
        zeros[0][4],
        zeros[0][5],
        zeros[0][6],
    ) = (board1[0], board1[1], board1[2], board1[3], board1[4], board1[5], board1[6])
    cards = zeros[0]
    for i in range(7):
        for j in range(i + 1, 7):
            if cards[i] > cards[j]:
                cards[i], cards[j] = cards[j], cards[i]
    cards = np.flip(cards)
    r = zeros[1]
    r[0], r[1], r[2], r[3], r[4], r[5], r[6] = (
        int(cards[0] / 10 - 10),
        int(cards[1] / 10 - 10),
        int(cards[2] / 10 - 10),
        int(cards[3] / 10 - 10),
        int(cards[4] / 10 - 10),
        int(cards[5] / 10 - 10),
        int(cards[6] / 10 - 10),
    )
    s = zeros[2]

    s[0], s[1], s[2], s[3], s[4], s[5], s[6] = (
        cards[0] - r[0] * 10,
        cards[1] - r[1] * 10,
        cards[2] - r[2] * 10,
        cards[3] - r[3] * 10,
        cards[4] - r[4] * 10,
        cards[5] - r[5] * 10,
        cards[6] - r[6] * 10,
    )

    ss = zeros[3]  # можно и по-раньше это сделать
    if s[4] > 0:
        ss[0], ss[1], ss[2], ss[3], ss[4], ss[5], ss[6] = (
            s[0],
            s[1],
            s[2],
            s[3],
            s[4],
            s[5],
            s[6],
        )
        for i in range(7):
            for j in range(i + 1, 7):
                if ss[i] > ss[j]:
                    ss[i], ss[j] = ss[j], ss[i]

    # оценка силы

    pair_str1 = any_pair(r)

    # print('pair_str1 = ',pair_str1)
    if s[4] > 0:
        str1 = 0
        if ss[0] == ss[4] or ss[1] == ss[5] or ss[2] == ss[6]:
            suit = ss[2]
            count = 0
            for i in range(7):
                if s[i] == suit:
                    ss[count] = r[i]
                    count += 1

            x1, x2, x3, x4, x5 = ss[0], ss[1], ss[2], ss[3], ss[4]
            if x4 - x5 != 1:
                str1 = 2250000 + x1 * 28561 + x2 * 2197 + x3 * 169 + x4 * 13 + x5
            elif count == 5:
                if x1 - x2 == x2 - x3 == x3 - x4 == x4 - x5 == 1:
                    return 3600000 + x1
                else:
                    if x1 == 14 and x2 - x3 == x3 - x4 == x4 - x5 == x5 - 1 == 1:
                        return 3600000 + x2
                    else:
                        str1 = (
                            2250000 + x1 * 28561 + x2 * 2197 + x3 * 169 + x4 * 13 + x5
                        )
            elif count == 6:
                x6 = ss[5]
                if x1 - x2 == x2 - x3 == x3 - x4 == x4 - x5 == 1:
                    return 3600000 + x1
                if x5 - x6 == x2 - x3 == x3 - x4 == x4 - x5 == 1:
                    return 3600000 + x2
                else:
                    if x1 == 14 and x3 - x4 == x4 - x5 == x5 - x6 == x6 - 1 == 1:
                        return 3600000 + x3
                    else:
                        str1 = (
                            2250000 + x1 * 28561 + x2 * 2197 + x3 * 169 + x4 * 13 + x5
                        )
            elif count == 7:
                x6 = ss[5]
                x7 = ss[6]
                if x1 - x2 == x2 - x3 == x3 - x4 == x4 - x5 == 1:
                    return 3600000 + x1
                if x5 - x6 == x2 - x3 == x3 - x4 == x4 - x5 == 1:
                    return 3600000 + x2
                if x5 - x6 == x6 - x7 == x3 - x4 == x4 - x5 == 1:
                    return 3600000 + x3
                else:
                    if x1 == 14 and x4 - x5 == x5 - x6 == x6 - x7 == x7 - 1 == 1:
                        return 3600000 + x4
                    else:
                        str1 = (
                            2250000 + x1 * 28561 + x2 * 2197 + x3 * 169 + x4 * 13 + x5
                        )
            else:
                str1 = 2250000 + x1 * 28561 + x2 * 2197 + x3 * 169 + x4 * 13 + x5

            # str1=j_is_strtfl_or_fl(r,s,ss)
        if str1 > pair_str1:
            return str1

    if pair_str1 > 2250000:
        return pair_str1

    # раз флаша нету и фулла тоже - то проверяем на стрит
    count = 0
    ss[0] = r[0]
    for i in range(6):
        if r[i] != r[i + 1]:
            ss[count] = r[i]
            count += 1
    ss[count] = r[6]
    r1, r2, r3, r4, r5, r6, r7 = ss[0], ss[1], ss[2], ss[3], ss[4], ss[5], ss[6]
    if r1 != 14 and r3 != r4 and r3 - r4 != 1:
        return pair_str1
    elif r1 - r2 == r2 - r3 == r3 - r4 == r4 - r5 == 1:
        return 1800000 + r1
    elif r2 - r3 == r3 - r4 == r4 - r5 == r5 - r6 == 1:
        return 1800000 + r2
    elif r3 - r4 == r4 - r5 == r5 - r6 == r6 - r7 == 1:
        return 1800000 + r3
    elif r1 == 14:
        if r2 - r3 == r3 - r4 == r4 - r5 == r5 - 1 == 1:
            return 1800000 + r2
        elif r3 - r4 == r4 - r5 == r5 - r6 == r6 - 1 == 1:
            return 1800000 + r3
        elif r4 - r5 == r5 - r6 == r6 - r7 == r7 - 1 == 1:
            return 1800000 + r4
        else:
            return pair_str1
    else:
        return pair_str1


@njit(cache=True)
def find_each_equity_turn(
    hero_range_array,
    opps_range_array,
    hero_rivers_strength,
    opps_rivers_strength,
    basic_turns_paired_matrix,
):
    """
        Calculates an equity on every turn and writes it.
        Returns None
    """

    turns_count = len(basic_turns_paired_matrix)
    range_len_hr = range(len(hero_range_array))
    range_len_or = range(len(opps_range_array))
    range_48 = range(48)
    for k in range(turns_count):
        for i in range_len_hr:
            for j in range_len_or:
                if basic_turns_paired_matrix[k][i][j] < 0:
                    continue
                eq = 0
                games = 44
                for k2 in range_48:
                    str1 = hero_rivers_strength[k][k2][i]
                    str2 = opps_rivers_strength[k][k2][j]
                    if str1 == 0 or str2 == 0:
                        continue
                    if str1 > str2:
                        eq += 1
                    elif str1 == str2:
                        eq += 0.5
                basic_turns_paired_matrix[k][i][j] = eq / games

    return


@njit(cache=True)
def translate_abstractions_flop(
    basic_flop_paired_matrix, basic_turns_paired_matrix, turns
):
    turns_count = len(basic_turns_paired_matrix)
    r_turns_count = range(turns_count)

    for i in r_turns_count:
        basic_flop_paired_matrix = vectorized_summ_matrix(
            basic_flop_paired_matrix, basic_turns_paired_matrix[i]
        )
    played_turns = turns_count - 4
    for h1 in range(len(basic_flop_paired_matrix)):
        for h2 in range(len(basic_flop_paired_matrix[0])):
            if basic_flop_paired_matrix[h1][h2] < 0:
                continue
            basic_flop_paired_matrix[h1][h2] = (
                basic_flop_paired_matrix[h1][h2] / played_turns
            )

    return basic_flop_paired_matrix


@njit(cache=True)
def convert_range_from_array_with_weigths(range_array):
    text = "["
    for i in range(len(range_array)):
        hand_string = ""
        if i > 0:
            hand_string += ","
        hand = range_array[i]
        card1, card2, w = int(hand[0]), int(hand[1]), int(hand[2])

        hand_string += strength_to_card(card1) + strength_to_card(card2)
        hand_string += "(" + str(w) + ")"
        text += hand_string
    text += "]"
    return text


@vectorize(cache=True)
def vectorized_summ_matrix(a, b):
    """
        A very specialized sum of matrices
    """
    if b < 0:
        return a
    elif a < 0:
        return a
    return a + b


@njit(cache=True)
def convert_char_to_float_array(char_array):
    """
        Converts array full of hand names to numeric array with default weight = 1.
        Returns a new array
    """

    float_array = np.empty((len(char_array), 3), dtype=float32)
    for i in range(len(char_array)):
        card1, card2 = (
            char_array[i][0] + char_array[i][1],
            char_array[i][2] + char_array[i][3],
        )
        jcard1, jcard2 = jcard_strength(card1), jcard_strength(card2)
        float_array[i][0], float_array[i][1] = jcard1, jcard2
        float_array[i][2] = 1
    return float_array


# from equilator
# @cc.export('make_equity_array', 'u1,f4[:],f4[:],f4[:](f4[:])')
# @cc.export('make_equity_array', 'f4[:,:](u1, f4[:,:], f4[:,:], f4[:])')
@njit(cache=True)
def make_equity_array(
    stage,
    OOP_range_array,
    IP_range_array,
    board,
):
    """
        Here we make arrays of equity / fill them up.
        Postflop only.
        Each stage needs its own approach.
        Contains alot of repetions,
        but splitting the function into smaller ones leads to faster compilation and slower execution
    """

    range_len_OOP = range(len(OOP_range_array))
    range_len_IP = range(len(IP_range_array))

    # flop
    if stage == 1:
        # 1. INITIALIZATION
        turns = np.ones((49, 2), dtype=uint8)
        flops = np.empty((3), dtype=uint8)
        all_cards_array_with_weigth = make_all_board_possible_cards_array()
        board_card1, board_card2, board_card3 = (
            int(board[0]),
            int(board[1]),
            int(board[2]),
        )
        flops[0], flops[1], flops[2] = board_card1, board_card2, board_card3
        suit1, suit2, suit3 = (
            board_card1 - int(board_card1 / 10) * 10,
            board_card2 - int(board_card2 / 10) * 10,
            board_card3 - int(board_card3 / 10) * 10,
        )

        index = 0
        for i in range(52):
            new_card = all_cards_array_with_weigth[i][0]
            if (
                new_card == board_card1
                or new_card == board_card2
                or new_card == board_card3
            ):
                continue
            turns[index][0] = new_card
            index += 1

        turns_count = len(turns)
        OOP_rivers_strength = np.zeros(
            (turns_count, 48, len(OOP_range_array)), dtype=uint32
        )
        IP_rivers_strength = np.zeros(
            (turns_count, 48, len(IP_range_array)), dtype=uint32
        )
        basic_flop_paired_matrix = np.zeros(
            (len(OOP_range_array), len(IP_range_array)), dtype=float32
        )  # include playability player vs player
        basic_turns_paired_matrix = np.zeros(
            (turns_count, len(OOP_range_array), len(IP_range_array)), dtype=float32
        )
        for i in range(len(OOP_range_array)):
            OOP_card1 = OOP_range_array[i][0]
            OOP_card2 = OOP_range_array[i][1]
            for j in range(len(IP_range_array)):
                IP_card1, IP_card2 = IP_range_array[j][0], IP_range_array[j][1]
                if (
                    OOP_card1 == IP_card1
                    or OOP_card2 == IP_card1
                    or OOP_card1 == IP_card2
                    or OOP_card2 == IP_card2
                ):
                    basic_flop_paired_matrix[i][j] = -1
                    for k in range(turns_count):
                        basic_turns_paired_matrix[k][i][j] = -1
                    continue

        rivers = np.zeros((turns_count, 48, 2), dtype=uint8)
        for i in range(turns_count):
            turn_card = turns[i][0]
            rvr_index = 0
            for j in range(52):
                new_card = all_cards_array_with_weigth[j][0]
                if (
                    new_card == board_card1
                    or new_card == board_card2
                    or new_card == board_card3
                    or new_card == turn_card
                ):
                    continue
                rivers[i][rvr_index][0] = new_card
                rvr_index += 1

        data_massive_small = np.zeros((6, 7), dtype=uint8)
        (
            data_massive_small[5][0],
            data_massive_small[5][1],
            data_massive_small[5][2],
        ) = (suit1, suit2, suit3)
        (
            data_massive_small[4][0],
            data_massive_small[4][1],
            data_massive_small[4][2],
        ) = (board_card1, board_card2, board_card3)

        # 2. calculate strength of each hand

        for k2 in range(2):
            # k2 number is a numeric player position equivalent.
            # Used to define a player 0 or player 1
            len_r_a = len(OOP_range_array)
            len_ops_r_a = len(IP_range_array)
            range_array = OOP_range_array
            rivers_strength = OOP_rivers_strength
            if k2 == 1:
                len_r_a, len_ops_r_a = len_ops_r_a, len_r_a
                rivers_strength = IP_rivers_strength
                range_array = IP_range_array
            for i in range(len_r_a):
                h_card1, h_card2 = range_array[i][0], range_array[i][1]
                data_massive_small[4][5], data_massive_small[4][6] = (
                    h_card1,
                    h_card2,
                )
                hc_suit1, hc_suit2 = (
                    h_card1 - int(h_card1 / 10) * 10,
                    h_card2 - int(h_card2 / 10) * 10,
                )
                data_massive_small[5][3], data_massive_small[5][4] = (
                    hc_suit1,
                    hc_suit2,
                )
                for j in range(turns_count):
                    b_card4 = turns[j][0]
                    if h_card1 == b_card4 or h_card2 == b_card4:
                        if k2 == 0:
                            for k in range(len_ops_r_a):
                                basic_turns_paired_matrix[j][i][k] = -1
                        else:
                            for k in range(len_ops_r_a):
                                basic_turns_paired_matrix[j][k][i] = -1
                        continue
                    data_massive_small[4][3] = b_card4

                    fd = 0
                    suit4 = b_card4 - int(b_card4 / 10) * 10
                    data_massive_small[5][5] = suit4
                    fd_suit = 0
                    fd_cards_count = 0
                    for k1 in range(1, 5):
                        count = 0
                        for k in range(6):
                            if data_massive_small[5][k] == k1:
                                count += 1
                        if count > 3:
                            fd_suit = k1
                            fd = 1
                            fd_cards_count = count
                            break

                    if fd == 0:
                        old_river_rank = 0
                        str1 = 0
                        for k in range(48):
                            river_card = rivers[j][k][0]
                            if river_card == h_card1 or river_card == h_card2:
                                rivers_strength[j][k][i] = 0
                                continue
                            river_rank = int(river_card / 10) * 10
                            if river_rank == old_river_rank:
                                rivers_strength[j][k][i] = str1
                                continue
                            data_massive_small[4][4] = river_rank
                            old_river_rank = river_rank
                            str1 = current_strength_of_this_hand(data_massive_small)
                            rivers_strength[j][k][i] = str1

                    else:
                        old_river_rank = 0
                        str1 = 0
                        for k in range(48):
                            river_card = rivers[j][k][0]
                            if river_card == h_card1 or river_card == h_card2:
                                rivers_strength[j][k][i] = 0
                                continue
                            river_suit = river_card - int(river_card / 10) * 10
                            if river_suit == fd_suit or fd_cards_count > 4:
                                data_massive_small[4][4] = river_card
                                str2 = current_strength_of_this_hand(
                                    data_massive_small
                                )
                                rivers_strength[j][k][i] = str2
                                continue

                            river_rank = int(river_card / 10) * 10
                            if river_rank == old_river_rank:
                                rivers_strength[j][k][i] = str1
                                continue
                            data_massive_small[4][4] = river_rank
                            old_river_rank = river_rank
                            str1 = current_strength_of_this_hand(data_massive_small)
                            rivers_strength[j][k][i] = str1

        # 3. CALC EQUITY

        find_each_equity_turn(
            OOP_range_array,
            IP_range_array,
            OOP_rivers_strength,
            IP_rivers_strength,
            basic_turns_paired_matrix
        )
        basic_flop_paired_matrix = translate_abstractions_flop(
            basic_flop_paired_matrix, basic_turns_paired_matrix, turns
        )

        return basic_flop_paired_matrix

    # turn
    elif stage == 2:
        # 1. INITIALIZATION
        board_card1, board_card2, board_card3 = (
            int(board[0]),
            int(board[1]),
            int(board[2]),
        )
        suit1, suit2, suit3 = (
            board_card1 - int(board_card1 / 10) * 10,
            board_card2 - int(board_card2 / 10) * 10,
            board_card3 - int(board_card3 / 10) * 10,
        )
        turns = np.ones((1, 2), dtype=uint8)
        turns[0] = int(board[3])
        turns_count = 1  # we are on the turn
        all_cards_array_with_weigth = make_all_board_possible_cards_array()
        OOP_rivers_strength = np.zeros(
            (turns_count, 48, len(OOP_range_array)), dtype=uint32
        )
        IP_rivers_strength = np.zeros(
            (turns_count, 48, len(IP_range_array)), dtype=uint32
        )
        main_paired_matrix = np.zeros(
            (len(OOP_range_array), len(IP_range_array)), dtype=float32
        )  # include playability player vs player
        side_paired_matrix = np.zeros(
            (48, len(OOP_range_array), len(IP_range_array)), dtype=float32
        )
        rivers = np.zeros((turns_count, 48, 2), dtype=uint8)
        for i in range(turns_count):
            turn_card = turns[i][0]
            rvr_index = 0
            for j in range(52):
                new_card = all_cards_array_with_weigth[j][0]
                if (
                    new_card == board_card1
                    or new_card == board_card2
                    or new_card == board_card3
                    or new_card == turn_card
                ):
                    continue
                rivers[i][rvr_index][0] = new_card
                rvr_index += 1
        data_massive_small = np.zeros((6, 7), dtype=uint8)
        (
            data_massive_small[5][0],
            data_massive_small[5][1],
            data_massive_small[5][2],
        ) = (suit1, suit2, suit3)
        (
            data_massive_small[4][0],
            data_massive_small[4][1],
            data_massive_small[4][2],
        ) = (board_card1, board_card2, board_card3)

        # 2. calculate strength of each hand
        for k2 in range(2):
            # k2 number is a numeric player position equivalent.
            # Used to define a player 0 or player 1
            len_r_a = len(OOP_range_array)
            len_ops_r_a = len(IP_range_array)
            range_array = OOP_range_array
            rivers_strength = OOP_rivers_strength
            if k2 == 1:
                len_r_a, len_ops_r_a = len_ops_r_a, len_r_a
                rivers_strength = IP_rivers_strength
                range_array = IP_range_array
            for i in range(len_r_a):
                h_card1, h_card2 = range_array[i][0], range_array[i][1]
                data_massive_small[4][5], data_massive_small[4][6] = (
                    h_card1,
                    h_card2,
                )
                hc_suit1, hc_suit2 = (
                    h_card1 - int(h_card1 / 10) * 10,
                    h_card2 - int(h_card2 / 10) * 10,
                )
                data_massive_small[5][3], data_massive_small[5][4] = (
                    hc_suit1,
                    hc_suit2,
                )
                for j in range(turns_count):
                    b_card4 = turns[j][0]
                    data_massive_small[4][3] = b_card4
                    fd = 0
                    suit4 = b_card4 - int(b_card4 / 10) * 10
                    data_massive_small[5][5] = suit4
                    fd_suit = 0
                    fd_cards_count = 0
                    for k1 in range(1, 5):
                        count = 0
                        for k in range(6):
                            if data_massive_small[5][k] == k1:
                                count += 1
                        if count > 3:
                            fd_suit = k1
                            fd = 1
                            fd_cards_count = count
                            break

                    if fd == 0:
                        old_river_rank = 0
                        str1 = 0
                        for k in range(48):
                            river_card = rivers[j][k][0]
                            if river_card == h_card1 or river_card == h_card2:
                                rivers_strength[j][k][i] = 0
                                continue
                            river_rank = int(river_card / 10) * 10
                            if river_rank == old_river_rank:
                                rivers_strength[j][k][i] = str1
                                continue

                            data_massive_small[4][4] = river_rank
                            old_river_rank = river_rank
                            str1 = current_strength_of_this_hand(data_massive_small)
                            rivers_strength[j][k][i] = str1

                    else:
                        old_river_rank = 0
                        str1 = 0
                        for k in range(48):
                            river_card = rivers[j][k][0]
                            if river_card == h_card1 or river_card == h_card2:
                                rivers_strength[j][k][i] = 0
                                continue
                            river_suit = river_card - int(river_card / 10) * 10
                            if river_suit == fd_suit or fd_cards_count > 4:
                                data_massive_small[4][4] = river_card
                                str2 = current_strength_of_this_hand(
                                    data_massive_small
                                )
                                rivers_strength[j][k][i] = str2
                                continue

                            river_rank = int(river_card / 10) * 10
                            if river_rank == old_river_rank:
                                rivers_strength[j][k][i] = str1
                                continue

                            data_massive_small[4][4] = river_rank
                            old_river_rank = river_rank
                            str1 = current_strength_of_this_hand(data_massive_small)
                            rivers_strength[j][k][i] = str1

        # 3. CALC EQUITY
        range_eq = 0
        range_games = 0
        range_48 = range(48)
        for i in range_len_OOP:
            hero_card1, hero_card2 = OOP_range_array[i][0], OOP_range_array[i][1]
            w1 = OOP_range_array[i][2]
            for j in range_len_IP:
                opps_card1, opps_card2 = IP_range_array[j][0], IP_range_array[j][1]
                if (
                    hero_card1 == opps_card1
                    or hero_card2 == opps_card1
                    or hero_card1 == opps_card2
                    or hero_card2 == opps_card2
                ):
                    main_paired_matrix[i][j] = -1
                    for k2 in range_48:
                        side_paired_matrix[k2][i][j] = -1
                    continue
                eq = 0
                games = 44  # allways =44
                for k2 in range_48:
                    str1 = OOP_rivers_strength[0][k2][i]
                    str2 = IP_rivers_strength[0][k2][j]
                    if str1 == 0 or str2 == 0:
                        side_paired_matrix[k2][i][j] = -1
                        continue
                    if str1 > str2:
                        side_paired_matrix[k2][i][j] = 1
                        eq += 1
                    elif str1 == str2:
                        eq += 0.5
                        side_paired_matrix[k2][i][j] = 0.5
                main_paired_matrix[i][j] = eq / games
                w2 = IP_range_array[j][2]
                range_eq += main_paired_matrix[i][j] * w1 * w2
                range_games += w1 * w2
        if range_games > 0:
            range_eq /= range_games
        return main_paired_matrix

    # river
    else:
        # 1. INITIALIZATION
        board_card1, board_card2, board_card3, board_card4, board_card5 = (
            int(board[0]),
            int(board[1]),
            int(board[2]),
            int(board[3]),
            int(board[4]),
        )
        turns = np.ones((1, 2), dtype=uint8)
        OOP_rivers_strength = np.zeros((1, 1, len(OOP_range_array)), dtype=uint32)
        IP_rivers_strength = np.zeros((1, 1, len(IP_range_array)), dtype=uint32)
        main_paired_matrix = np.zeros(
            (len(OOP_range_array), len(IP_range_array)), dtype=float32
        )  # include playability player vs player
        side_paired_matrix = np.zeros((1, 1, 1), dtype=float32)
        rivers = np.zeros((1, 1, 2), dtype=uint8)
        rivers[0][0][0] = board_card5
        data_massive_small = np.zeros((6, 7), dtype=uint8)
        (
            data_massive_small[4][0],
            data_massive_small[4][1],
            data_massive_small[4][2],
            data_massive_small[4][3],
            data_massive_small[4][4],
        ) = (board_card1, board_card2, board_card3, board_card4, board_card5)

        # 2. calculate strength of each hand
        for k2 in range(2):
            # k2 number is a numeric player position equivalent.
            # Used to define a player 0 or player 1
            len_r_a = len(OOP_range_array)
            len_ops_r_a = len(IP_range_array)
            range_array = OOP_range_array
            rivers_strength = OOP_rivers_strength
            if k2 == 1:
                len_r_a, len_ops_r_a = len_ops_r_a, len_r_a
                rivers_strength = IP_rivers_strength
                range_array = IP_range_array
            for i in range(len_r_a):
                h_card1, h_card2 = range_array[i][0], range_array[i][1]
                data_massive_small[4][5], data_massive_small[4][6] = (
                    h_card1,
                    h_card2,
                )
                current_strength = current_strength_of_this_hand(data_massive_small)
                rivers_strength[0][0][i] = current_strength

        # 3. CALC EQUITY
        range_eq = 0
        range_games = 0
        for i in range_len_OOP:
            hero_card1, hero_card2 = OOP_range_array[i][0], OOP_range_array[i][1]
            str1 = OOP_rivers_strength[0][0][i]
            hand_eq = 0
            hand_games = 0
            for j in range_len_IP:
                opps_card1, opps_card2 = IP_range_array[j][0], IP_range_array[j][1]
                if (
                    hero_card1 == opps_card1
                    or hero_card2 == opps_card1
                    or hero_card1 == opps_card2
                    or hero_card2 == opps_card2
                ):
                    main_paired_matrix[i][j] = -1
                    continue
                str2 = IP_rivers_strength[0][0][j]
                if str1 == 0 or str2 == 0:
                    main_paired_matrix[i][j] = -1
                    continue
                range_games += 1
                hand_games += 1
                if str1 > str2:
                    main_paired_matrix[i][j] = 1
                    hand_eq += 1
                    range_eq += 1
                elif str1 == str2:
                    main_paired_matrix[i][j] = 0.5
                    hand_eq += 0.5
                    range_eq += 0.5
            if hand_games > 0:
                hand_eq /= hand_games

        if range_games > 0:
            range_eq /= range_games

        return main_paired_matrix


@njit(cache=True)
def calculate_eq(matrix, transformed_range1, transformed_range2):
    total_eq = 0
    total_games = 0
    for i in range(len(matrix)):
        w1 = transformed_range1[i][2]
        for j in range(len(matrix[0])):
            eq = matrix[i][j]
            if eq < 0:
                continue
            w2 = transformed_range2[j][2]
            ww = w1 * w2
            total_eq += ww * eq
            total_games += ww
    if total_games > 0:
        total_eq /= total_games
    return round(total_eq, 6)


@njit(cache=True)
def make_index_array(
    target_range_array: np.ndarray,
    all_paired_hands_array: np.ndarray
):
    len_range = len(target_range_array)
    index_array = np.empty((len_range), dtype=uint16)
    for i in range(len(target_range_array)):
        h1, h2 = target_range_array[i][0], target_range_array[i][1]
        for j in range(len(all_paired_hands_array)):
            if h1 == all_paired_hands_array[j][0] and h2 == all_paired_hands_array[j][1]:
                index_array[i] = j
                break
    return index_array


@njit(cache=True)
def recalculate_preflop_matrix(full_preflop_matrix, index_array_1, index_array_2):
    recalculated_preflop_matrix = np.empty(
        (len(index_array_1), len(index_array_2)), dtype=float32
    )
    for i in range(len(index_array_1)):
        idx1 = index_array_1[i]
        for j in range(len(index_array_2)):
            idx2 = index_array_2[j]
            eq = full_preflop_matrix[idx1][idx2]
            recalculated_preflop_matrix[i][j] = eq
    return recalculated_preflop_matrix


@njit(cache=True)
def get_all_paired_hands_array():
    all_paired_hands_array = np.array([
        [124.0, 123.0], [124.0, 122.0], [124.0, 121.0], [123.0, 122.0], [123.0, 121.0], [122.0, 121.0], [134.0, 133.0], [134.0, 132.0], [134.0, 131.0], [133.0, 132.0], [133.0, 131.0], [132.0, 131.0], [144.0, 143.0], [144.0, 142.0], [144.0, 141.0], [143.0, 142.0], [143.0, 141.0], [142.0, 141.0], [154.0, 153.0], [154.0, 152.0], [154.0, 151.0], [153.0, 152.0], [153.0, 151.0], [152.0, 151.0], [164.0, 163.0], [164.0, 162.0], [164.0, 161.0], [163.0, 162.0], [163.0, 161.0], [162.0, 161.0], [174.0, 173.0], [174.0, 172.0], [174.0, 171.0], [173.0, 172.0], [173.0, 171.0], [172.0, 171.0], [184.0, 183.0], [184.0, 182.0], [184.0, 181.0], [183.0, 182.0], [183.0, 181.0], [182.0, 181.0], [194.0, 193.0], [194.0, 192.0], [194.0, 191.0], [193.0, 192.0], [193.0, 191.0], [192.0, 191.0], [204.0, 203.0], [204.0, 202.0], [204.0, 201.0], [203.0, 202.0], [203.0, 201.0], [202.0, 201.0], [214.0, 213.0], [214.0, 212.0], [214.0, 211.0], [213.0, 212.0], [213.0, 211.0], [212.0, 211.0], [224.0, 223.0], [224.0, 222.0], [224.0, 221.0], [223.0, 222.0], [223.0, 221.0], [222.0, 221.0], [234.0, 233.0], [234.0, 232.0], [234.0, 231.0], [233.0, 232.0], [233.0, 231.0], [232.0, 231.0], [244.0, 243.0], [244.0, 242.0], [244.0, 241.0], [243.0, 242.0], [243.0, 241.0], [242.0, 241.0], [244.0, 124.0], [243.0, 123.0], [242.0, 122.0], [241.0, 121.0], [244.0, 134.0], [243.0, 133.0], [242.0, 132.0], [241.0, 131.0], [244.0, 144.0], [243.0, 143.0], [242.0, 142.0], [241.0, 141.0], [244.0, 154.0], [243.0, 153.0], [242.0, 152.0], [241.0, 151.0], [244.0, 164.0], [243.0, 163.0], [242.0, 162.0], [241.0, 161.0], [244.0, 174.0], [243.0, 173.0], [242.0, 172.0], [241.0, 171.0], [244.0, 184.0], [243.0, 183.0], [242.0, 182.0], [241.0, 181.0], [244.0, 194.0], [243.0, 193.0], [242.0, 192.0], [241.0, 191.0], [244.0, 204.0], [243.0, 203.0], [242.0, 202.0], [241.0, 201.0], [244.0, 214.0], [243.0, 213.0], [242.0, 212.0], [241.0, 211.0], [244.0, 224.0], [243.0, 223.0], [242.0, 222.0], [241.0, 221.0], [244.0, 234.0], [243.0, 233.0], [242.0, 232.0], [241.0, 231.0], [234.0, 124.0], [233.0, 123.0], [232.0, 122.0], [231.0, 121.0], [234.0, 134.0], [233.0, 133.0], [232.0, 132.0], [231.0, 131.0], [234.0, 144.0], [233.0, 143.0], [232.0, 142.0], [231.0, 141.0], [234.0, 154.0], [233.0, 153.0], [232.0, 152.0], [231.0, 151.0], [234.0, 164.0], [233.0, 163.0], [232.0, 162.0], [231.0, 161.0], [234.0, 174.0], [233.0, 173.0], [232.0, 172.0], [231.0, 171.0], [234.0, 184.0], [233.0, 183.0], [232.0, 182.0], [231.0, 181.0], [234.0, 194.0], [233.0, 193.0], [232.0, 192.0], [231.0, 191.0], [234.0, 204.0], [233.0, 203.0], [232.0, 202.0], [231.0, 201.0], [234.0, 214.0], [233.0, 213.0], [232.0, 212.0], [231.0, 211.0], [234.0, 224.0], [233.0, 223.0], [232.0, 222.0], [231.0, 221.0], [224.0, 124.0], [223.0, 123.0], [222.0, 122.0], [221.0, 121.0], [224.0, 134.0], [223.0, 133.0], [222.0, 132.0], [221.0, 131.0], [224.0, 144.0], [223.0, 143.0], [222.0, 142.0], [221.0, 141.0], [224.0, 154.0], [223.0, 153.0], [222.0, 152.0], [221.0, 151.0], [224.0, 164.0], [223.0, 163.0], [222.0, 162.0], [221.0, 161.0], [224.0, 174.0], [223.0, 173.0], [222.0, 172.0], [221.0, 171.0], [224.0, 184.0], [223.0, 183.0], [222.0, 182.0], [221.0, 181.0], [224.0, 194.0], [223.0, 193.0], [222.0, 192.0], [221.0, 191.0], [224.0, 204.0], [223.0, 203.0], [222.0, 202.0], [221.0, 201.0], [224.0, 214.0], [223.0, 213.0], [222.0, 212.0], [221.0, 211.0], [214.0, 124.0], [213.0, 123.0], [212.0, 122.0], [211.0, 121.0], [214.0, 134.0], [213.0, 133.0], [212.0, 132.0], [211.0, 131.0], [214.0, 144.0], [213.0, 143.0], [212.0, 142.0], [211.0, 141.0], [214.0, 154.0], [213.0, 153.0], [212.0, 152.0], [211.0, 151.0], [214.0, 164.0], [213.0, 163.0], [212.0, 162.0], [211.0, 161.0], [214.0, 174.0], [213.0, 173.0], [212.0, 172.0], [211.0, 171.0], [214.0, 184.0], [213.0, 183.0], [212.0, 182.0], [211.0, 181.0], [214.0, 194.0], [213.0, 193.0], [212.0, 192.0], [211.0, 191.0], [214.0, 204.0], [213.0, 203.0], [212.0, 202.0], [211.0, 201.0], [204.0, 124.0], [203.0, 123.0], [202.0, 122.0], [201.0, 121.0], [204.0, 134.0], [203.0, 133.0], [202.0, 132.0], [201.0, 131.0], [204.0, 144.0], [203.0, 143.0], [202.0, 142.0], [201.0, 141.0], [204.0, 154.0], [203.0, 153.0], [202.0, 152.0], [201.0, 151.0], [204.0, 164.0], [203.0, 163.0], [202.0, 162.0], [201.0, 161.0], [204.0, 174.0], [203.0, 173.0], [202.0, 172.0], [201.0, 171.0], [204.0, 184.0], [203.0, 183.0], [202.0, 182.0], [201.0, 181.0], [204.0, 194.0], [203.0, 193.0], [202.0, 192.0], [201.0, 191.0], [194.0, 124.0], [193.0, 123.0], [192.0, 122.0], [191.0, 121.0], [194.0, 134.0], [193.0, 133.0], [192.0, 132.0], [191.0, 131.0], [194.0, 144.0], [193.0, 143.0], [192.0, 142.0], [191.0, 141.0], [194.0, 154.0], [193.0, 153.0], [192.0, 152.0], [191.0, 151.0], [194.0, 164.0], [193.0, 163.0], [192.0, 162.0], [191.0, 161.0], [194.0, 174.0], [193.0, 173.0], [192.0, 172.0], [191.0, 171.0], [194.0, 184.0], [193.0, 183.0], [192.0, 182.0], [191.0, 181.0], [184.0, 124.0], [183.0, 123.0], [182.0, 122.0], [181.0, 121.0], [184.0, 134.0], [183.0, 133.0], [182.0, 132.0], [181.0, 131.0], [184.0, 144.0], [183.0, 143.0], [182.0, 142.0], [181.0, 141.0], [184.0, 154.0], [183.0, 153.0], [182.0, 152.0], [181.0, 151.0], [184.0, 164.0], [183.0, 163.0], [182.0, 162.0], [181.0, 161.0], [184.0, 174.0], [183.0, 173.0], [182.0, 172.0], [181.0, 171.0], [174.0, 124.0], [173.0, 123.0], [172.0, 122.0], [171.0, 121.0], [174.0, 134.0], [173.0, 133.0], [172.0, 132.0], [171.0, 131.0], [174.0, 144.0], [173.0, 143.0], [172.0, 142.0], [171.0, 141.0], [174.0, 154.0], [173.0, 153.0], [172.0, 152.0], [171.0, 151.0], [174.0, 164.0], [173.0, 163.0], [172.0, 162.0], [171.0, 161.0], [164.0, 124.0], [163.0, 123.0], [162.0, 122.0], [161.0, 121.0], [164.0, 134.0], [163.0, 133.0], [162.0, 132.0], [161.0, 131.0], [164.0, 144.0], [163.0, 143.0], [162.0, 142.0], [161.0, 141.0], [164.0, 154.0], [163.0, 153.0], [162.0, 152.0], [161.0, 151.0], [154.0, 124.0], [153.0, 123.0], [152.0, 122.0], [151.0, 121.0], [154.0, 134.0], [153.0, 133.0], [152.0, 132.0], [151.0, 131.0], [154.0, 144.0], [153.0, 143.0], [152.0, 142.0], [151.0, 141.0], [144.0, 124.0], [143.0, 123.0], [142.0, 122.0], [141.0, 121.0], [144.0, 134.0], [143.0, 133.0], [142.0, 132.0], [141.0, 131.0], [134.0, 124.0], [133.0, 123.0], [132.0, 122.0], [131.0, 121.0], [244.0, 123.0], [244.0, 122.0], [244.0, 121.0], [243.0, 124.0], [243.0, 122.0], [243.0, 121.0], [242.0, 124.0], [242.0, 123.0], [242.0, 121.0], [241.0, 124.0], [241.0, 123.0], [241.0, 122.0], [244.0, 133.0], [244.0, 132.0], [244.0, 131.0], [243.0, 134.0], [243.0, 132.0], [243.0, 131.0], [242.0, 134.0], [242.0, 133.0], [242.0, 131.0], [241.0, 134.0], [241.0, 133.0], [241.0, 132.0], [244.0, 143.0], [244.0, 142.0], [244.0, 141.0], [243.0, 144.0], [243.0, 142.0], [243.0, 141.0], [242.0, 144.0], [242.0, 143.0], [242.0, 141.0], [241.0, 144.0], [241.0, 143.0], [241.0, 142.0], [244.0, 153.0], [244.0, 152.0], [244.0, 151.0], [243.0, 154.0], [243.0, 152.0], [243.0, 151.0], [242.0, 154.0], [242.0, 153.0], [242.0, 151.0], [241.0, 154.0], [241.0, 153.0], [241.0, 152.0], [244.0, 163.0], [244.0, 162.0], [244.0, 161.0], [243.0, 164.0], [243.0, 162.0], [243.0, 161.0], [242.0, 164.0], [242.0, 163.0], [242.0, 161.0], [241.0, 164.0], [241.0, 163.0], [241.0, 162.0], [244.0, 173.0], [244.0, 172.0], [244.0, 171.0], [243.0, 174.0], [243.0, 172.0], [243.0, 171.0], [242.0, 174.0], [242.0, 173.0], [242.0, 171.0], [241.0, 174.0], [241.0, 173.0], [241.0, 172.0], [244.0, 183.0], [244.0, 182.0], [244.0, 181.0], [243.0, 184.0], [243.0, 182.0], [243.0, 181.0], [242.0, 184.0], [242.0, 183.0], [242.0, 181.0], [241.0, 184.0], [241.0, 183.0], [241.0, 182.0], [244.0, 193.0], [244.0, 192.0], [244.0, 191.0], [243.0, 194.0], [243.0, 192.0], [243.0, 191.0], [242.0, 194.0], [242.0, 193.0], [242.0, 191.0], [241.0, 194.0], [241.0, 193.0], [241.0, 192.0], [244.0, 203.0], [244.0, 202.0], [244.0, 201.0], [243.0, 204.0], [243.0, 202.0], [243.0, 201.0], [242.0, 204.0], [242.0, 203.0], [242.0, 201.0], [241.0, 204.0], [241.0, 203.0], [241.0, 202.0], [244.0, 213.0], [244.0, 212.0], [244.0, 211.0], [243.0, 214.0], [243.0, 212.0], [243.0, 211.0], [242.0, 214.0], [242.0, 213.0], [242.0, 211.0], [241.0, 214.0], [241.0, 213.0], [241.0, 212.0], [244.0, 223.0], [244.0, 222.0], [244.0, 221.0], [243.0, 224.0], [243.0, 222.0], [243.0, 221.0], [242.0, 224.0], [242.0, 223.0], [242.0, 221.0], [241.0, 224.0], [241.0, 223.0], [241.0, 222.0], [244.0, 233.0], [244.0, 232.0], [244.0, 231.0], [243.0, 234.0], [243.0, 232.0], [243.0, 231.0], [242.0, 234.0], [242.0, 233.0], [242.0, 231.0], [241.0, 234.0], [241.0, 233.0], [241.0, 232.0], [234.0, 123.0], [234.0, 122.0], [234.0, 121.0], [233.0, 124.0], [233.0, 122.0], [233.0, 121.0], [232.0, 124.0], [232.0, 123.0], [232.0, 121.0], [231.0, 124.0], [231.0, 123.0], [231.0, 122.0], [234.0, 133.0], [234.0, 132.0], [234.0, 131.0], [233.0, 134.0], [233.0, 132.0], [233.0, 131.0], [232.0, 134.0], [232.0, 133.0], [232.0, 131.0], [231.0, 134.0], [231.0, 133.0], [231.0, 132.0], [234.0, 143.0], [234.0, 142.0], [234.0, 141.0], [233.0, 144.0], [233.0, 142.0], [233.0, 141.0], [232.0, 144.0], [232.0, 143.0], [232.0, 141.0], [231.0, 144.0], [231.0, 143.0], [231.0, 142.0], [234.0, 153.0], [234.0, 152.0], [234.0, 151.0], [233.0, 154.0], [233.0, 152.0], [233.0, 151.0], [232.0, 154.0], [232.0, 153.0], [232.0, 151.0], [231.0, 154.0], [231.0, 153.0], [231.0, 152.0], [234.0, 163.0], [234.0, 162.0], [234.0, 161.0], [233.0, 164.0], [233.0, 162.0], [233.0, 161.0], [232.0, 164.0], [232.0, 163.0], [232.0, 161.0], [231.0, 164.0], [231.0, 163.0], [231.0, 162.0], [234.0, 173.0], [234.0, 172.0], [234.0, 171.0], [233.0, 174.0], [233.0, 172.0], [233.0, 171.0], [232.0, 174.0], [232.0, 173.0], [232.0, 171.0], [231.0, 174.0], [231.0, 173.0], [231.0, 172.0], [234.0, 183.0], [234.0, 182.0], [234.0, 181.0], [233.0, 184.0], [233.0, 182.0], [233.0, 181.0], [232.0, 184.0], [232.0, 183.0], [232.0, 181.0], [231.0, 184.0], [231.0, 183.0], [231.0, 182.0], [234.0, 193.0], [234.0, 192.0], [234.0, 191.0], [233.0, 194.0], [233.0, 192.0], [233.0, 191.0], [232.0, 194.0], [232.0, 193.0], [232.0, 191.0], [231.0, 194.0], [231.0, 193.0], [231.0, 192.0], [234.0, 203.0], [234.0, 202.0], [234.0, 201.0], [233.0, 204.0], [233.0, 202.0], [233.0, 201.0], [232.0, 204.0], [232.0, 203.0], [232.0, 201.0], [231.0, 204.0], [231.0, 203.0], [231.0, 202.0], [234.0, 213.0], [234.0, 212.0], [234.0, 211.0], [233.0, 214.0], [233.0, 212.0], [233.0, 211.0], [232.0, 214.0], [232.0, 213.0], [232.0, 211.0], [231.0, 214.0], [231.0, 213.0], [231.0, 212.0], [234.0, 223.0], [234.0, 222.0], [234.0, 221.0], [233.0, 224.0], [233.0, 222.0], [233.0, 221.0], [232.0, 224.0], [232.0, 223.0], [232.0, 221.0], [231.0, 224.0], [231.0, 223.0], [231.0, 222.0], [224.0, 123.0], [224.0, 122.0], [224.0, 121.0], [223.0, 124.0], [223.0, 122.0], [223.0, 121.0], [222.0, 124.0], [222.0, 123.0], [222.0, 121.0], [221.0, 124.0], [221.0, 123.0], [221.0, 122.0], [224.0, 133.0], [224.0, 132.0], [224.0, 131.0], [223.0, 134.0], [223.0, 132.0], [223.0, 131.0], [222.0, 134.0], [222.0, 133.0], [222.0, 131.0], [221.0, 134.0], [221.0, 133.0], [221.0, 132.0], [224.0, 143.0], [224.0, 142.0], [224.0, 141.0], [223.0, 144.0], [223.0, 142.0], [223.0, 141.0], [222.0, 144.0], [222.0, 143.0], [222.0, 141.0], [221.0, 144.0], [221.0, 143.0], [221.0, 142.0], [224.0, 153.0], [224.0, 152.0], [224.0, 151.0], [223.0, 154.0], [223.0, 152.0], [223.0, 151.0], [222.0, 154.0], [222.0, 153.0], [222.0, 151.0], [221.0, 154.0], [221.0, 153.0], [221.0, 152.0], [224.0, 163.0], [224.0, 162.0], [224.0, 161.0], [223.0, 164.0], [223.0, 162.0], [223.0, 161.0], [222.0, 164.0], [222.0, 163.0], [222.0, 161.0], [221.0, 164.0], [221.0, 163.0], [221.0, 162.0], [224.0, 173.0], [224.0, 172.0], [224.0, 171.0], [223.0, 174.0], [223.0, 172.0], [223.0, 171.0], [222.0, 174.0], [222.0, 173.0], [222.0, 171.0], [221.0, 174.0], [221.0, 173.0], [221.0, 172.0], [224.0, 183.0], [224.0, 182.0], [224.0, 181.0], [223.0, 184.0], [223.0, 182.0], [223.0, 181.0], [222.0, 184.0], [222.0, 183.0], [222.0, 181.0], [221.0, 184.0], [221.0, 183.0], [221.0, 182.0], [224.0, 193.0], [224.0, 192.0], [224.0, 191.0], [223.0, 194.0], [223.0, 192.0], [223.0, 191.0], [222.0, 194.0], [222.0, 193.0], [222.0, 191.0], [221.0, 194.0], [221.0, 193.0], [221.0, 192.0], [224.0, 203.0], [224.0, 202.0], [224.0, 201.0], [223.0, 204.0], [223.0, 202.0], [223.0, 201.0], [222.0, 204.0], [222.0, 203.0], [222.0, 201.0], [221.0, 204.0], [221.0, 203.0], [221.0, 202.0], [224.0, 213.0], [224.0, 212.0], [224.0, 211.0], [223.0, 214.0], [223.0, 212.0], [223.0, 211.0], [222.0, 214.0], [222.0, 213.0], [222.0, 211.0], [221.0, 214.0], [221.0, 213.0], [221.0, 212.0], [214.0, 123.0], [214.0, 122.0], [214.0, 121.0], [213.0, 124.0], [213.0, 122.0], [213.0, 121.0], [212.0, 124.0], [212.0, 123.0], [212.0, 121.0], [211.0, 124.0], [211.0, 123.0], [211.0, 122.0], [214.0, 133.0], [214.0, 132.0], [214.0, 131.0], [213.0, 134.0], [213.0, 132.0], [213.0, 131.0], [212.0, 134.0], [212.0, 133.0], [212.0, 131.0], [211.0, 134.0], [211.0, 133.0], [211.0, 132.0], [214.0, 143.0], [214.0, 142.0], [214.0, 141.0], [213.0, 144.0], [213.0, 142.0], [213.0, 141.0], [212.0, 144.0], [212.0, 143.0], [212.0, 141.0], [211.0, 144.0], [211.0, 143.0], [211.0, 142.0], [214.0, 153.0], [214.0, 152.0], [214.0, 151.0], [213.0, 154.0], [213.0, 152.0], [213.0, 151.0], [212.0, 154.0], [212.0, 153.0], [212.0, 151.0], [211.0, 154.0], [211.0, 153.0], [211.0, 152.0], [214.0, 163.0], [214.0, 162.0], [214.0, 161.0], [213.0, 164.0], [213.0, 162.0], [213.0, 161.0], [212.0, 164.0], [212.0, 163.0], [212.0, 161.0], [211.0, 164.0], [211.0, 163.0], [211.0, 162.0], [214.0, 173.0], [214.0, 172.0], [214.0, 171.0], [213.0, 174.0], [213.0, 172.0], [213.0, 171.0], [212.0, 174.0], [212.0, 173.0], [212.0, 171.0], [211.0, 174.0], [211.0, 173.0], [211.0, 172.0], [214.0, 183.0], [214.0, 182.0], [214.0, 181.0], [213.0, 184.0], [213.0, 182.0], [213.0, 181.0], [212.0, 184.0], [212.0, 183.0], [212.0, 181.0], [211.0, 184.0], [211.0, 183.0], [211.0, 182.0], [214.0, 193.0], [214.0, 192.0], [214.0, 191.0], [213.0, 194.0], [213.0, 192.0], [213.0, 191.0], [212.0, 194.0], [212.0, 193.0], [212.0, 191.0], [211.0, 194.0], [211.0, 193.0], [211.0, 192.0], [214.0, 203.0], [214.0, 202.0], [214.0, 201.0], [213.0, 204.0], [213.0, 202.0], [213.0, 201.0], [212.0, 204.0], [212.0, 203.0], [212.0, 201.0], [211.0, 204.0], [211.0, 203.0], [211.0, 202.0], [204.0, 123.0], [204.0, 122.0], [204.0, 121.0], [203.0, 124.0], [203.0, 122.0], [203.0, 121.0], [202.0, 124.0], [202.0, 123.0], [202.0, 121.0], [201.0, 124.0], [201.0, 123.0], [201.0, 122.0], [204.0, 133.0], [204.0, 132.0], [204.0, 131.0], [203.0, 134.0], [203.0, 132.0], [203.0, 131.0], [202.0, 134.0], [202.0, 133.0], [202.0, 131.0], [201.0, 134.0], [201.0, 133.0], [201.0, 132.0], [204.0, 143.0], [204.0, 142.0], [204.0, 141.0], [203.0, 144.0], [203.0, 142.0], [203.0, 141.0], [202.0, 144.0], [202.0, 143.0], [202.0, 141.0], [201.0, 144.0], [201.0, 143.0], [201.0, 142.0], [204.0, 153.0], [204.0, 152.0], [204.0, 151.0], [203.0, 154.0], [203.0, 152.0], [203.0, 151.0], [202.0, 154.0], [202.0, 153.0], [202.0, 151.0], [201.0, 154.0], [201.0, 153.0], [201.0, 152.0], [204.0, 163.0], [204.0, 162.0], [204.0, 161.0], [203.0, 164.0], [203.0, 162.0], [203.0, 161.0], [202.0, 164.0], [202.0, 163.0], [202.0, 161.0], [201.0, 164.0], [201.0, 163.0], [201.0, 162.0], [204.0, 173.0], [204.0, 172.0], [204.0, 171.0], [203.0, 174.0], [203.0, 172.0], [203.0, 171.0], [202.0, 174.0], [202.0, 173.0], [202.0, 171.0], [201.0, 174.0], [201.0, 173.0], [201.0, 172.0], [204.0, 183.0], [204.0, 182.0], [204.0, 181.0], [203.0, 184.0], [203.0, 182.0], [203.0, 181.0], [202.0, 184.0], [202.0, 183.0], [202.0, 181.0], [201.0, 184.0], [201.0, 183.0], [201.0, 182.0], [204.0, 193.0], [204.0, 192.0], [204.0, 191.0], [203.0, 194.0], [203.0, 192.0], [203.0, 191.0], [202.0, 194.0], [202.0, 193.0], [202.0, 191.0], [201.0, 194.0], [201.0, 193.0], [201.0, 192.0], [194.0, 123.0], [194.0, 122.0], [194.0, 121.0], [193.0, 124.0], [193.0, 122.0], [193.0, 121.0], [192.0, 124.0], [192.0, 123.0], [192.0, 121.0], [191.0, 124.0], [191.0, 123.0], [191.0, 122.0], [194.0, 133.0], [194.0, 132.0], [194.0, 131.0], [193.0, 134.0], [193.0, 132.0], [193.0, 131.0], [192.0, 134.0], [192.0, 133.0], [192.0, 131.0], [191.0, 134.0], [191.0, 133.0], [191.0, 132.0], [194.0, 143.0], [194.0, 142.0], [194.0, 141.0], [193.0, 144.0], [193.0, 142.0], [193.0, 141.0], [192.0, 144.0], [192.0, 143.0], [192.0, 141.0], [191.0, 144.0], [191.0, 143.0], [191.0, 142.0], [194.0, 153.0], [194.0, 152.0], [194.0, 151.0], [193.0, 154.0], [193.0, 152.0], [193.0, 151.0], [192.0, 154.0], [192.0, 153.0], [192.0, 151.0], [191.0, 154.0], [191.0, 153.0], [191.0, 152.0], [194.0, 163.0], [194.0, 162.0], [194.0, 161.0], [193.0, 164.0], [193.0, 162.0], [193.0, 161.0], [192.0, 164.0], [192.0, 163.0], [192.0, 161.0], [191.0, 164.0], [191.0, 163.0], [191.0, 162.0], [194.0, 173.0], [194.0, 172.0], [194.0, 171.0], [193.0, 174.0], [193.0, 172.0], [193.0, 171.0], [192.0, 174.0], [192.0, 173.0], [192.0, 171.0], [191.0, 174.0], [191.0, 173.0], [191.0, 172.0], [194.0, 183.0], [194.0, 182.0], [194.0, 181.0], [193.0, 184.0], [193.0, 182.0], [193.0, 181.0], [192.0, 184.0], [192.0, 183.0], [192.0, 181.0], [191.0, 184.0], [191.0, 183.0], [191.0, 182.0], [184.0, 123.0], [184.0, 122.0], [184.0, 121.0], [183.0, 124.0], [183.0, 122.0], [183.0, 121.0], [182.0, 124.0], [182.0, 123.0], [182.0, 121.0], [181.0, 124.0], [181.0, 123.0], [181.0, 122.0], [184.0, 133.0], [184.0, 132.0], [184.0, 131.0], [183.0, 134.0], [183.0, 132.0], [183.0, 131.0], [182.0, 134.0], [182.0, 133.0], [182.0, 131.0], [181.0, 134.0], [181.0, 133.0], [181.0, 132.0], [184.0, 143.0], [184.0, 142.0], [184.0, 141.0], [183.0, 144.0], [183.0, 142.0], [183.0, 141.0], [182.0, 144.0], [182.0, 143.0], [182.0, 141.0], [181.0, 144.0], [181.0, 143.0], [181.0, 142.0], [184.0, 153.0], [184.0, 152.0], [184.0, 151.0], [183.0, 154.0], [183.0, 152.0], [183.0, 151.0], [182.0, 154.0], [182.0, 153.0], [182.0, 151.0], [181.0, 154.0], [181.0, 153.0], [181.0, 152.0], [184.0, 163.0], [184.0, 162.0], [184.0, 161.0], [183.0, 164.0], [183.0, 162.0], [183.0, 161.0], [182.0, 164.0], [182.0, 163.0], [182.0, 161.0], [181.0, 164.0], [181.0, 163.0], [181.0, 162.0], [184.0, 173.0], [184.0, 172.0], [184.0, 171.0], [183.0, 174.0], [183.0, 172.0], [183.0, 171.0], [182.0, 174.0], [182.0, 173.0], [182.0, 171.0], [181.0, 174.0], [181.0, 173.0], [181.0, 172.0], [174.0, 123.0], [174.0, 122.0], [174.0, 121.0], [173.0, 124.0], [173.0, 122.0], [173.0, 121.0], [172.0, 124.0], [172.0, 123.0], [172.0, 121.0], [171.0, 124.0], [171.0, 123.0], [171.0, 122.0], [174.0, 133.0], [174.0, 132.0], [174.0, 131.0], [173.0, 134.0], [173.0, 132.0], [173.0, 131.0], [172.0, 134.0], [172.0, 133.0], [172.0, 131.0], [171.0, 134.0], [171.0, 133.0], [171.0, 132.0], [174.0, 143.0], [174.0, 142.0], [174.0, 141.0], [173.0, 144.0], [173.0, 142.0], [173.0, 141.0], [172.0, 144.0], [172.0, 143.0], [172.0, 141.0], [171.0, 144.0], [171.0, 143.0], [171.0, 142.0], [174.0, 153.0], [174.0, 152.0], [174.0, 151.0], [173.0, 154.0], [173.0, 152.0], [173.0, 151.0], [172.0, 154.0], [172.0, 153.0], [172.0, 151.0], [171.0, 154.0], [171.0, 153.0], [171.0, 152.0], [174.0, 163.0], [174.0, 162.0], [174.0, 161.0], [173.0, 164.0], [173.0, 162.0], [173.0, 161.0], [172.0, 164.0], [172.0, 163.0], [172.0, 161.0], [171.0, 164.0], [171.0, 163.0], [171.0, 162.0], [164.0, 123.0], [164.0, 122.0], [164.0, 121.0], [163.0, 124.0], [163.0, 122.0], [163.0, 121.0], [162.0, 124.0], [162.0, 123.0], [162.0, 121.0], [161.0, 124.0], [161.0, 123.0], [161.0, 122.0], [164.0, 133.0], [164.0, 132.0], [164.0, 131.0], [163.0, 134.0], [163.0, 132.0], [163.0, 131.0], [162.0, 134.0], [162.0, 133.0], [162.0, 131.0], [161.0, 134.0], [161.0, 133.0], [161.0, 132.0], [164.0, 143.0], [164.0, 142.0], [164.0, 141.0], [163.0, 144.0], [163.0, 142.0], [163.0, 141.0], [162.0, 144.0], [162.0, 143.0], [162.0, 141.0], [161.0, 144.0], [161.0, 143.0], [161.0, 142.0], [164.0, 153.0], [164.0, 152.0], [164.0, 151.0], [163.0, 154.0], [163.0, 152.0], [163.0, 151.0], [162.0, 154.0], [162.0, 153.0], [162.0, 151.0], [161.0, 154.0], [161.0, 153.0], [161.0, 152.0], [154.0, 123.0], [154.0, 122.0], [154.0, 121.0], [153.0, 124.0], [153.0, 122.0], [153.0, 121.0], [152.0, 124.0], [152.0, 123.0], [152.0, 121.0], [151.0, 124.0], [151.0, 123.0], [151.0, 122.0], [154.0, 133.0], [154.0, 132.0], [154.0, 131.0], [153.0, 134.0], [153.0, 132.0], [153.0, 131.0], [152.0, 134.0], [152.0, 133.0], [152.0, 131.0], [151.0, 134.0], [151.0, 133.0], [151.0, 132.0], [154.0, 143.0], [154.0, 142.0], [154.0, 141.0], [153.0, 144.0], [153.0, 142.0], [153.0, 141.0], [152.0, 144.0], [152.0, 143.0], [152.0, 141.0], [151.0, 144.0], [151.0, 143.0], [151.0, 142.0], [144.0, 123.0], [144.0, 122.0], [144.0, 121.0], [143.0, 124.0], [143.0, 122.0], [143.0, 121.0], [142.0, 124.0], [142.0, 123.0], [142.0, 121.0], [141.0, 124.0], [141.0, 123.0], [141.0, 122.0], [144.0, 133.0], [144.0, 132.0], [144.0, 131.0], [143.0, 134.0], [143.0, 132.0], [143.0, 131.0], [142.0, 134.0], [142.0, 133.0], [142.0, 131.0], [141.0, 134.0], [141.0, 133.0], [141.0, 132.0], [134.0, 123.0], [134.0, 122.0], [134.0, 121.0], [133.0, 124.0], [133.0, 122.0], [133.0, 121.0], [132.0, 124.0], [132.0, 123.0], [132.0, 121.0], [131.0, 124.0], [131.0, 123.0], [131.0, 122.0], ])

    return all_paired_hands_array


@njit(cache=True)
def decode_arr(array):
    new = np.empty((1326, 1326), dtype=float64)
    for i in range(1326):
        for j in range(1326):
            new[i][j] = array[i][j] - 1.618 - i*0.0002 - j*0.0003
    return new


# @cc.export('calc_equity_preflop', 'f4[:](f8[:,:], f4[:,:], f4[:,:])')
@njit(cache=True)
def calc_equity_preflop(
    preflop_matrix: np.ndarray,
    OOP_range_array: np.ndarray,
    IP_range_array: np.ndarray
) -> np.ndarray:

    full_preflop_matrix = decode_arr(preflop_matrix)

    result_array = np.empty((len(OOP_range_array) + 1), dtype=float32)
    all_paired_hands_array = get_all_paired_hands_array()

    OOP_indexes_array = make_index_array(
        target_range_array=OOP_range_array,
        all_paired_hands_array=all_paired_hands_array)

    IP_indexes_array = make_index_array(
        target_range_array=IP_range_array,
        all_paired_hands_array=all_paired_hands_array
    )

    recalculated_preflop_matrix = recalculate_preflop_matrix(
        full_preflop_matrix,
        OOP_indexes_array,
        IP_indexes_array
    )
    total_eq = 0
    total_games = 0
    for i in range(len(recalculated_preflop_matrix)):
        w1 = OOP_range_array[i][2]

        hand_eq = 0
        hand_games = 0

        for j in range(len(recalculated_preflop_matrix[0])):
            eq = recalculated_preflop_matrix[i][j]
            if eq < 0:
                continue
            w2 = IP_range_array[j][2]
            ww = w1 * w2
            total_eq += ww * eq
            total_games += ww

            hand_eq += ww * eq
            hand_games += ww

        # hand eq writing
        if hand_games > 0:
            hand_eq /= hand_games
        else:
            hand_eq = -1.0
        result_array[i] = hand_eq

    if total_games > 0:
        total_eq /= total_games

    result_array[-1] = total_eq
    return result_array


@njit(cache=True)
def calc_equity_postflop(
    stage: int,
    OOP_range_array: np.ndarray,
    IP_range_array: np.ndarray,
    board: np.ndarray
) -> np.ndarray:
    result_array = np.empty(len(OOP_range_array) + 1, dtype=float32)
    
    main_paired_matrix = make_equity_array(
        stage,
        OOP_range_array,
        IP_range_array,
        board
    )
    print("№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№")
    print("OOP_range_array = ", OOP_range_array)
    print("IP_range_array = ", IP_range_array)
    print("board = ", board)
    print("MAIN PAIRED MATRIX = ", main_paired_matrix)
    

    total_eq = 0
    total_games = 0
    for i in range(len(main_paired_matrix)):
        w1 = OOP_range_array[i][2]

        hand_eq = 0
        hand_games = 0

        for j in range(len(main_paired_matrix[0])):
            eq = main_paired_matrix[i][j]
            if eq < 0:
                continue
            w2 = IP_range_array[j][2]
            ww = w1 * w2
            total_eq += ww * eq
            total_games += ww

            hand_eq += ww * eq
            hand_games += ww

        # hand eq writing
        if hand_games > 0:
            hand_eq /= hand_games
        else:
            hand_eq = -1.0
        result_array[i] = hand_eq

    if total_games > 0:
        total_eq /= total_games

    result_array[-1] = total_eq
    return result_array
