import begin
import logging
import random

from logging.handlers import RotatingFileHandler

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
    for color in range(1, 5):
        for value in range(2, 15):
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
    value = [str(i) for i in range(1, 11)] + ["Jack", "Queen", "King", "Ace"]
    color = ["♠", "♣", "♥", "♦"]

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


@begin.start(auto_convert=True, lexical_order=True)
def start(player: "How much players" = 2):
    if not 1 < int(player) < 11:
        logger.info("player=" + str(player) + ' : Wrong value -> set to 2')
        player = 2
    logger.info("nb players = " + str(player))

    players = []
    deck = init_deck_52()
    deck_shuffle(deck)

    for i in range(player):
        players.append([])
        deck, players[i] = give_card_to_player(deck, players[i])

    #fonctions qui check la main ici
