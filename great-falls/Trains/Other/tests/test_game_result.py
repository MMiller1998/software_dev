import unittest
from unittest.mock import MagicMock

from Trains.Other.game_result import GameResult


class GameResultTest(unittest.TestCase):
    def test_game_result_constructor_valid(self):
        players = [MagicMock(), MagicMock(), MagicMock()]
        scores = [1, 2, 3]
        cheaters = [MagicMock()]
        game_result = GameResult(players, scores, cheaters)
        self.assertEqual(1, len(game_result.cheaters))

    def test_game_result_get_winners_no_players(self):
        game_result = GameResult([], [] , [MagicMock(), MagicMock()])
        self.assertListEqual([], game_result.get_winners())

    def test_game_result_get_winners(self):
        player1 = MagicMock()
        player2 = MagicMock()
        player3 = MagicMock()
        players = [player1, player2, player3]
        scores = [1, 2, 3]
        cheaters = [MagicMock()]
        game_result = GameResult(players, scores, cheaters)
        self.assertListEqual([player3], game_result.get_winners())

    def test_game_result_get_winners_multiple(self):
        player1 = MagicMock()
        player2 = MagicMock()
        player3 = MagicMock()
        players = [player1, player2, player3]
        scores = [1, 3, 3]
        cheaters = [MagicMock()]
        game_result = GameResult(players, scores, cheaters)
        self.assertListEqual([player2, player3], game_result.get_winners())

    def test_game_result_get_rankings_with_ties(self):
        player1 = MagicMock()
        player2 = MagicMock()
        player3 = MagicMock()
        players = [player1, player2, player3]
        scores = [1, 3, 3]
        cheaters = [MagicMock()]
        game_result = GameResult(players, scores, cheaters)
        rankings = game_result.get_rankings()
        self.assertListEqual([player2, player3], rankings[0])
        self.assertListEqual([player1], rankings[1])
