import unittest

from typing import Tuple, List

from trains.map import TrainMap
from trains.game.constants import MIN_PLAYERS_IN_GAME
from trains.game.player import PlayerActor
from trains.strategy.buy_now import MyStrategy as BuyNow
from trains.tournament.manager import TournamentManager

from tests.examples import decks
from tests.helpers.dummy_player_actors import StartRaisePlayerActor


class TestTournamentManager(unittest.TestCase):

    def test_allocate_players_base(self):
        players, manager = self._create_manager_with_num_players(2)

        self.assertEqual(manager.allocate_players(), [players])

        players, manager = self._create_manager_with_num_players(8)

        self.assertEqual(manager.allocate_players(), [players])

    def test_allocate_players_recursive(self):
        players, manager = self._create_manager_with_num_players(18)

        self.assertEqual(manager.allocate_players(), [
            players[:8],
            players[8:16],
            players[16:]
        ])

    def test_allocate_players_backtrack(self):
        players, manager = self._create_manager_with_num_players(9)

        self.assertEqual(manager.allocate_players(), [
            players[:7],
            players[7:]
        ])

        players, manager = self._create_manager_with_num_players(17)

        self.assertEqual(manager.allocate_players(), [
            players[:8],
            players[8:15],
            players[15:]
        ])

    def test_stop_condition_reached_consecutive_winners(self):
        players, manager = self._create_manager_with_num_players(10)

        manager.previous_round_winners = set(players[:4])
        manager.current_players = players[:4]

        self.assertTrue(manager.stop_condition_reached())

    def test_stop_condition_reached_too_few_players(self):
        players, manager = self._create_manager_with_num_players(10)

        manager.current_players = players[: MIN_PLAYERS_IN_GAME - 1]

        self.assertTrue(manager.stop_condition_reached())

    def test_stop_condition_reached_final_game_flag(self):
        _, manager = self._create_manager_with_num_players(10)

        manager.final_game_flag = True

        self.assertTrue(manager.stop_condition_reached())

    def test_start_up(self):
        players, manager = self._create_manager_with_num_players(10)

        chosen_map = manager.start_up()

        self.assertIsInstance(chosen_map, TrainMap)

    def test_start_up_cheaters(self):
        good_players = [PlayerActor(BuyNow()) for _ in range(4)]
        expected_cheaters = [StartRaisePlayerActor() for _ in range(2)]
        manager = TournamentManager(good_players + expected_cheaters, decks.green_deck)

        manager.start_up()

        self.assertEqual(len(manager.current_players), 4)
        self.assertSetEqual(manager.cheaters, set(expected_cheaters))


    def _create_manager_with_num_players(self, num_players: int) -> Tuple[List[PlayerActor], TournamentManager]:
        players = [PlayerActor(BuyNow()) for _ in range(num_players)]
        return players, TournamentManager(players, decks.green_deck)
