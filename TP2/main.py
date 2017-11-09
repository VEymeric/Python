import begin
import logging
import random
import numpy
import TrouveFigure
from logging.handlers import RotatingFileHandler

COLORS = [i for i in range(1, 5)]
VALUES = [i for i in range(2, 15)]
DEFAULT_MIN_PLAYER = 2
DEFAULT_MAX_PLAYER = 8
DEFAULT_NB_PLAYER = 2
DEFAULT_NB_BURN = 1
DEFAULT_CARD_FLOP = 3
DEFAULT_CARD_THE_TURN = 1
DEFAULT_CARD_RIVER = 1
VALUE_STRAIGHT_FLUSH = 8
VALUE_FOUR = 7
VALUE_FULL = 6
VALUE_FLUSH = 5
VALUE_STRAIGHT = 4
VALUE_THREE = 3
VALUE_TWO_PAIR = 2
VALUE_PAIR = 1

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)

file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


def init_deck_52():
    """
    :return: a list of 52 cards with deck[O]=[1,2] and deck[51]=[4,14]
    """
    deck = []
    for color in COLORS:
        for value in VALUES:
            deck.append([color, value])
    return deck


def deck_shuffle(deck):
    """
    :param deck: a random deck
    :return: another random deck with same cards
    """
    random.shuffle(deck)
    return True


def disp_card(card):
    """
    :param card: one card[color, value]
    :return: a string for real value of card like King♦
    """
    txt = ""
    value = [str(i) for i in range(2, 11)] + ["Jack", "Queen", "King", "Ace"]
    color = ["C", "D", "H", "S"]

    if not len(value) > 0 < card[1]:
        logger.warning("value=" + str(card[1]) + ' : Wrong value -> set to 2')
        card[1] = 1
    txt += value[card[1] - 1]
    if not card[0] > 0 < len(color):
        logger.warning("color=" + str(card[0]) + ' : Wrong color -> set to 1')
        card[0] = 1
    txt += color[card[0]-1]

    return txt


def disp_n_top_cards(cards, index=1, n=-1):
    """
    :param cards: deck of cards
    :param index: index of the first card we disp
    :param n: number of card we disp
    :return: True if the function end
    """
    if n < 0:  # default value
        n = len(cards) - index
    card_list = {}
    for i in range(index, n + index):
        card_list[i] = disp_card(cards[i])
    return True


def give_card_to_player(deck, player):
    player += [deck[0]]
    player += [deck[1]]
    deck.pop(0)
    deck.pop(0)
    logger.info("one player get these cards : %s", player)
    return deck, player


def set_table(deck, table, nb_cards):
    if nb_cards < 1:
        return

    burn = deck[0]
    logger.info("This card have been burn : %s", burn)
    deck.pop(0)

    for i in range(nb_cards):
        table += [deck[0]]
        deck.pop(0)
    logger.info("Table changed : %s", table)
    return deck, table


def check_winner(players_hand, board):
    leader_board = []
    for index, player in enumerate(players_hand):
        player_board = board+player
        leader_board.append(TrouveFigure.DetermineMeilleur(player_board))
        print(max(leader_board[0]))
    # We try to find best hand
    best_id_hand = 0
    for index, test in enumerate(leader_board[1:]):
        index += 1  # As we didn't took first card
        check_best_hand = True
        test = 0
        while check_best_hand and leader_board[best_id_hand]:
            if leader_board[best_id_hand][test] < leader_board[index][test]:
                best_index_hand = index
                check_best_hand = False
            elif leader_board[best_id_hand][test] > leader_board[index][test]:
                check_best_hand = False
            elif leader_board[best_id_hand][test] == leader_board[index][test]:
                test += 1
    best_hand = leader_board[best_id_hand]
    logger.info("Best hand is : " + str(best_hand) + " from player " + str(best_id_hand + 1))


@begin.start(auto_convert=True, lexical_order=True)
def start(player: "How much players" = 2):
    if not DEFAULT_MIN_PLAYER <= int(player) <= DEFAULT_MAX_PLAYER:
        logger.info("player=" + str(player) + ' : Wrong value -> set to ' + str(DEFAULT_NB_PLAYER))
        player = DEFAULT_NB_PLAYER
    logger.info("nb players = " + str(player))

    players = []
    table = []

    deck = init_deck_52()
    deck_shuffle(deck)

    for i in range(player):
        players.append([])
        deck, players[i] = give_card_to_player(deck, players[i])

    deck, table = set_table(deck, table, DEFAULT_CARD_FLOP)
    deck, table = set_table(deck, table, DEFAULT_CARD_THE_TURN)
    deck, table = set_table(deck, table, DEFAULT_CARD_RIVER)

    check_winner(players, table)
    # functions qui check la main ici
