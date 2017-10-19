import begin
import logging

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
    deck = {}
    for color in range(1, 5):
        for value in range(1, 14):
            deck[value + 13*(color-1)] = [color, value]
    return deck


def disp_card(card):
    txt = ""
    value = ["Ace"]+[str(i) for i in range(2, 11)]+["Jack", "Queen", "King"]
    color = ["♠", "♣", "♥", "♦"]

    if not len(value) > 0 < card[1]:
        logger.warning("value=" + str(card[1]) + ' : Wrong value -> set to 1')
        card[1] = 1
    txt += value[card[1]]

    if not card[0] > 0 < len(color):
        logger.warning("color=" + str(card[0]) + ' : Wrong value -> set to 1')
        card[0] = 1
    txt += value[card[0]]

    return txt


def disp_n_top_cards(cards, index=1, n=-1):
    if n < 0:
        n = len(cards)
    liste = {}
    for i in range(n):
        liste[i] = disp_card(cards[i])
    print(liste)

@begin.start(auto_convert=True, lexical_order=True)
def start(player: "How much players" =2):
    if not 1 < int(player) < 11:
        logger.warning("player=" + str(player) + ' : Wrong value -> set to 2')
        player = 2
    logger.info("player=" + str(player))
    deck = init_deck_52()
    disp_card(deck[23])
