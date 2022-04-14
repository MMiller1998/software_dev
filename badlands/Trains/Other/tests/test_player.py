import unittest
from unittest.mock import MagicMock, patch

from Trains.Other.color import Color
from Trains.Other.interfaces.i_strategy import MORE_CARDS_REQUEST
from Trains.Player.player import Player


class PlayerTests(unittest.TestCase):
    MOCK_TRAIN_MAP = MagicMock()
    NUM_RAILS = 45
    NUM_CARDS = 4
    CARD_LIST = [Color.BLUE] * NUM_CARDS
    CARD_DICT = {c: 4 if c == Color.BLUE else 0 for c in Color}

    @patch('Trains.Player.player.IStrategy')
    def test_player_constructor_valid(self, mock_strategy):
        player = Player(mock_strategy)
        self.assertEqual(mock_strategy, player.strategy)
        self.assertIsNone(player.trains_map)
        self.assertIsNone(player.initial_rails)
        self.assertIsNone(player.initial_cards)

    @patch('Trains.Player.player.AStrategy')
    def test_player_from_strategy_file(self, mock_abstract_strategy):
        mock_strategy = MagicMock()
        mock_abstract_strategy.from_file.return_value = mock_strategy
        player = Player.player_from_strategy_file('')
        self.assertEqual(mock_strategy, player.strategy)

    @patch('Trains.Player.player.IStrategy')
    @patch('Trains.Player.player.Cards')
    def test_setup(self, mock_cards, mock_strategy):
        mock_cards.from_list.return_value = self.CARD_DICT
        player = Player(mock_strategy)
        player.setup(self.MOCK_TRAIN_MAP, self.NUM_RAILS, self.CARD_LIST)
        self.assertEqual(self.MOCK_TRAIN_MAP, player.trains_map)
        self.assertEqual(self.NUM_RAILS, player.initial_rails)
        self.assertEqual(self.CARD_DICT, player.initial_cards)

    @patch('Trains.Player.player.IStrategy')
    def test_pick(self, mock_strategy):
        mock_destinations = {MagicMock() for _ in range(5)}
        mock_strategy.select_destinations.return_value = set()
        player = Player(mock_strategy)
        self.assertSetEqual(mock_destinations, player.pick(mock_destinations))

    @patch('Trains.Player.player.IStrategy')
    def test_play(self, mock_strategy):
        mock_strategy.get_turn.return_value = MORE_CARDS_REQUEST
        player = Player(mock_strategy)
        self.assertEqual(MORE_CARDS_REQUEST, player.play(MagicMock()))
