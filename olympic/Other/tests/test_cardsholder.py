import unittest

from trains.graph_elements import RailColor
from trains.state.cardsholder import card_deck_to_card_hand


class TestCardsholder(unittest.TestCase):

    def test_card_deck_to_card_hand(self):
        deck = [RailColor.BLUE, RailColor.BLUE, RailColor.RED, RailColor.GREEN]
        hand = card_deck_to_card_hand(deck)

        self.assertDictEqual(hand, {RailColor.BLUE: 2, RailColor.RED: 1, RailColor.GREEN: 1, RailColor.WHITE: 0})
