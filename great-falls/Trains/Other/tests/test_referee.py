import unittest
from collections import deque
from typing import Set, Union
from unittest.mock import MagicMock, patch

from Trains.Admin.referee import Referee
from Trains.Common.map import Map
from Trains.Common.player_game_state import PlayerGameState
from Trains.Other.city import City
from Trains.Other.color import Color
from Trains.Other.destination import Destination
from Trains.Other.directed_connection import DirectedConnection
from Trains.Other.interfaces.i_strategy import IStrategy, MORE_CARDS_REQUEST
from Trains.Player.buy_now import BuyNowStrategy
from Trains.Other.undirected_connection import UndirectedConnection
from Trains.Player.player import Player
import Trains.Other.admin_utils as admin_utils


class HoldStrategy(IStrategy):
    @classmethod
    def select_destinations(cls, _: Map, possible_destinations: Set[Destination]) -> Set[Destination]:
        sorted_destinations = sorted(possible_destinations)
        return {sorted_destinations[0], sorted_destinations[1]}

    @classmethod
    def get_turn(cls, player_state: PlayerGameState) -> Union[UndirectedConnection, str]:
        return MORE_CARDS_REQUEST


class ExplodeStrategy(IStrategy):
    @classmethod
    def select_destinations(cls, _: Map, possible_destinations: Set[Destination]) -> Set[Destination]:
        sorted_destinations = sorted(possible_destinations)
        return {sorted_destinations[0], sorted_destinations[1]}

    @classmethod
    def get_turn(cls, player_state: PlayerGameState) -> Union[UndirectedConnection, str]:
        raise Exception("Oops")


class RefereeTests(unittest.TestCase):
    MOCK_TRAIN_MAP = MagicMock()

    MAP_WIDTH = 800
    MAP_HEIGHT = 800

    CITY_1 = City("city1", (0, 0))
    CITY_2 = City("city2", (1, 0))
    CITY_3 = City("city3", (2, 0))
    CITY_4 = City("city4", (3, 0))
    CITY_5 = City("city5", (4, 0))
    CITY_6 = City("city6", (6, 0))

    CITY_LIST = [CITY_1, CITY_2, CITY_3, CITY_4, CITY_5, CITY_6]

    DEST_1 = Destination(CITY_1, CITY_2)
    DEST_2 = Destination(CITY_1, CITY_3)
    DEST_3 = Destination(CITY_1, CITY_4)
    DEST_4 = Destination(CITY_1, CITY_5)
    DEST_5 = Destination(CITY_2, CITY_3)
    DEST_6 = Destination(CITY_2, CITY_4)
    DEST_7 = Destination(CITY_2, CITY_5)
    DEST_8 = Destination(CITY_3, CITY_4)
    DEST_9 = Destination(CITY_3, CITY_5)

    DIRECTED_CONNECTION_1_2 = DirectedConnection(CITY_1, CITY_2, 3, Color.RED)
    DIRECTED_CONNECTION_2_1 = DirectedConnection(CITY_2, CITY_1, 3, Color.RED)
    DIRECTED_CONNECTION_2_3_RED = DirectedConnection(CITY_2, CITY_3, 3, Color.WHITE)
    DIRECTED_CONNECTION_3_2_RED = DirectedConnection(CITY_3, CITY_2, 3, Color.WHITE)
    DIRECTED_CONNECTION_2_3_BLUE = DirectedConnection(CITY_2, CITY_3, 5, Color.BLUE)
    DIRECTED_CONNECTION_3_2_BLUE = DirectedConnection(CITY_3, CITY_2, 5, Color.BLUE)
    DIRECTED_CONNECTION_3_4 = DirectedConnection(CITY_3, CITY_4, 3, Color.WHITE)
    DIRECTED_CONNECTION_4_3 = DirectedConnection(CITY_4, CITY_3, 3, Color.WHITE)
    DIRECTED_CONNECTION_3_5_RED = DirectedConnection(CITY_3, CITY_5, 3, Color.WHITE)
    DIRECTED_CONNECTION_5_3_RED = DirectedConnection(CITY_5, CITY_3, 3, Color.WHITE)
    DIRECTED_CONNECTION_3_5_BLUE = DirectedConnection(CITY_3, CITY_5, 5, Color.BLUE)
    DIRECTED_CONNECTION_5_3_BLUE = DirectedConnection(CITY_5, CITY_3, 5, Color.BLUE)
    DIRECTED_CONNECTION_2_5_BLUE = DirectedConnection(CITY_2, CITY_5, 3, Color.BLUE)
    DIRECTED_CONNECTION_5_2_BLUE = DirectedConnection(CITY_5, CITY_2, 3, Color.BLUE)
    DIRECTED_CONNECTION_2_5_RED = DirectedConnection(CITY_2, CITY_5, 5, Color.WHITE)
    DIRECTED_CONNECTION_5_2_RED = DirectedConnection(CITY_5, CITY_2, 5, Color.WHITE)
    DIRECTED_CONNECTION_5_6 = DirectedConnection(CITY_5, CITY_6, 4, Color.WHITE)
    DIRECTED_CONNECTION_6_5 = DirectedConnection(CITY_6, CITY_5, 4, Color.WHITE)
    DIRECTED_CONNECTION_LIST = [DIRECTED_CONNECTION_1_2,
                                DIRECTED_CONNECTION_2_1,
                                DIRECTED_CONNECTION_2_3_RED,
                                DIRECTED_CONNECTION_3_2_RED,
                                DIRECTED_CONNECTION_2_3_BLUE,
                                DIRECTED_CONNECTION_3_2_BLUE,
                                DIRECTED_CONNECTION_3_4,
                                DIRECTED_CONNECTION_4_3,
                                DIRECTED_CONNECTION_3_5_RED,
                                DIRECTED_CONNECTION_5_3_RED,
                                DIRECTED_CONNECTION_3_5_BLUE,
                                DIRECTED_CONNECTION_5_3_BLUE,
                                DIRECTED_CONNECTION_2_5_BLUE,
                                DIRECTED_CONNECTION_5_2_BLUE,
                                DIRECTED_CONNECTION_2_5_RED,
                                DIRECTED_CONNECTION_5_2_RED,
                                DIRECTED_CONNECTION_5_6,
                                DIRECTED_CONNECTION_6_5]

    TRAIN_MAP = Map(MAP_WIDTH, MAP_HEIGHT, CITY_LIST, DIRECTED_CONNECTION_LIST)

    NUM_WINNERS = 2

    def test_referee_constructor_valid(self):
        mock_dest_strategy, mock_card_strategy = self.setup_strategy_mocks(MagicMock(), MagicMock())
        referee = Referee(self.MOCK_TRAIN_MAP, admin_utils.STARTING_NUM_RAILS, mock_card_strategy, mock_dest_strategy)
        self.assertEqual(admin_utils.STARTING_NUM_RAILS, referee._Referee__starting_rails_count)
        self.assertEqual(mock_dest_strategy, referee._Referee__destination_options_strategy)

    def test_referee_run_game_stale_end(self):
        card_strategy_mock = MagicMock()
        card_strategy_mock.create_deck.return_value = []
        player_1 = Player(HoldStrategy, "default")
        player_2 = Player(HoldStrategy, "default")
        player_3 = Player(HoldStrategy, "default")
        player_list = [player_1, player_2, player_3]
        game_result = Referee.run_game(self.TRAIN_MAP, player_list, deck_creation_strategy=card_strategy_mock)
        winners = game_result.get_winners()
        self.assertTrue(player_1 in winners)
        self.assertTrue(player_2 in winners)
        self.assertTrue(player_3 in winners)
        self.assertListEqual([], game_result.cheaters)

    def test_referee_run_game_cheaters_end(self):
        card_strategy_mock = MagicMock()
        card_strategy_mock.create_deck.return_value = []
        player_1 = Player(ExplodeStrategy, "default")
        player_2 = Player(ExplodeStrategy, "default")
        player_3 = Player(ExplodeStrategy, "default")
        player_list = [player_1, player_2, player_3]
        game_result = Referee.run_game(self.TRAIN_MAP, player_list, deck_creation_strategy=card_strategy_mock)
        cheaters = game_result.cheaters
        self.assertTrue(player_1 in cheaters)
        self.assertTrue(player_2 in cheaters)
        self.assertTrue(player_3 in cheaters)
        self.assertListEqual([], game_result.get_winners())

    def test_referee_run_game_termination_condition(self):
        card_strategy, dest_strategy = self.setup_strategy_mocks(MagicMock(), MagicMock())
        player_1 = Player(BuyNowStrategy, "default")
        player_2 = Player(BuyNowStrategy, "default2")
        player_3 = Player(BuyNowStrategy, "default3")
        player_list = [player_1, player_2, player_3]
        game_result = Referee.run_game(self.TRAIN_MAP, player_list, 3, card_strategy, dest_strategy)
        winners = game_result.get_winners()
        self.assertTrue(player_1 in winners)
        self.assertFalse(player_2 in winners)
        self.assertFalse(player_3 in winners)
        self.assertListEqual([], game_result.cheaters)

    def test_referee_run_game_invalid_board(self):
        self.MOCK_TRAIN_MAP.get_feasible_destinations.return_value = []
        players = self.setup_player_mocks()
        with self.assertRaises(ValueError):
            Referee.run_game(self.MOCK_TRAIN_MAP, players, admin_utils.STARTING_NUM_RAILS)

    def test_referee_run_game_invalid_board_one_less(self):
        self.MOCK_TRAIN_MAP.get_feasible_destinations.return_value = [MagicMock] * 8
        players = self.setup_player_mocks()
        with self.assertRaises(ValueError):
            Referee.run_game(self.MOCK_TRAIN_MAP, players, admin_utils.STARTING_NUM_RAILS)

    def test_referee_run_game_not_enough_players(self):
        player = MagicMock()
        with self.assertRaises(ValueError):
            Referee.run_game(self.MOCK_TRAIN_MAP, [player], admin_utils.STARTING_NUM_RAILS)

    @patch('Trains.Admin.referee.RefereeGameState')
    @patch('Trains.Admin.referee.PrivatePlayerState')
    @patch('Trains.Admin.referee.RandomDeckCreationStrategy')
    @patch('Trains.Admin.referee.RandomDestinationOptionsStrategy')
    def test_setup_game(self, mock_dest_strategy, mock_card_strategy, mock_private_player_state, mock_ref_game_state):
        players = self.setup_player_mocks()
        ps_1 = MagicMock()
        ps_2 = MagicMock()
        ps_3 = MagicMock()
        ps_list = [ps_1, ps_2, ps_3]
        mock_private_player_state.side_effect = ps_list

        for player in players:
            player.pick.side_effect = self.player_pick_mock_side_effect

        player_1_destinations = {self.DEST_1, self.DEST_2, self.DEST_3, self.DEST_4, self.DEST_5}
        player_2_destinations = {self.DEST_3, self.DEST_4, self.DEST_5, self.DEST_6, self.DEST_7}
        player_3_destinations = {self.DEST_5, self.DEST_6, self.DEST_7, self.DEST_8, self.DEST_9}

        mock_card_strategy_instance, mock_dest_strategy_instance = self.setup_strategy_mocks(mock_card_strategy,
                                                                                             mock_dest_strategy)
        mock_feasible_destinations = MagicMock()
        self.MOCK_TRAIN_MAP.get_feasible_destinations.return_value = mock_feasible_destinations
        ref = Referee(self.MOCK_TRAIN_MAP, deck_creation_strategy=mock_card_strategy_instance,
                      destination_options_strategy=mock_dest_strategy_instance)
        ref.setup_game(players)
        mock_card_strategy_instance.create_deck.assert_called_with(250)
        mock_ref_game_state.assert_called_with(self.MOCK_TRAIN_MAP, deque(zip(ps_list, players)), [Color.RED] * 238)
        for player, destinations in zip(players, [player_1_destinations, player_2_destinations, player_3_destinations]):
            player.setup.assert_called_with(self.MOCK_TRAIN_MAP, admin_utils.STARTING_NUM_RAILS, [Color.RED] * 4)
            player.pick.assert_called_with(destinations)
        self.MOCK_TRAIN_MAP.get_feasible_destinations.assert_called()
        mock_dest_strategy_instance.order_destinations.assert_called_with(mock_feasible_destinations)

    @patch('Trains.Admin.referee.RefereeGameState')
    @patch('Trains.Admin.referee.GameResult')
    def test_end_game(self, mock_game_result, mock_ref_game_state):
        players = self.setup_player_mocks()
        mock_ref_game_state_instance = mock_ref_game_state.return_value
        mock_ref_game_state_instance.get_players.return_value = players
        mock_game_result_instance = mock_game_result.return_value
        mock_game_result_instance.get_winners.return_value = players[:self.NUM_WINNERS]

        ref = Referee(self.MOCK_TRAIN_MAP, deck_creation_strategy=MagicMock(), destination_options_strategy=MagicMock())
        ref._Referee__game_state = mock_ref_game_state_instance
        self.assertEqual(mock_game_result_instance, ref.end_game())
        for i in range(len(players)):
            if i in range(self.NUM_WINNERS):
                players[i].win.assert_called_with(True)
            else:
                players[i].win.assert_called_with(False)

    def setup_strategy_mocks(self, mock_card_strategy, mock_dest_strategy):
        mock_card_strategy_instance = mock_card_strategy.return_value
        mock_dest_strategy_instance = mock_dest_strategy.return_value
        mock_card_strategy_instance.create_deck.return_value = [Color.RED for _ in range(250)]
        mock_dest_strategy_instance.order_destinations.return_value = [self.DEST_1, self.DEST_2, self.DEST_3,
                                                                       self.DEST_4,
                                                                       self.DEST_5, self.DEST_6, self.DEST_7,
                                                                       self.DEST_8,
                                                                       self.DEST_9]
        return mock_card_strategy_instance, mock_dest_strategy_instance

    def player_pick_mock_side_effect(self, destinations):
        sorted_destinations = sorted(destinations)
        return {sorted_destinations[2], sorted_destinations[3], sorted_destinations[4]}

    def setup_player_mocks(self):
        player_1 = MagicMock()
        player_2 = MagicMock()
        player_3 = MagicMock()
        return [player_1, player_2, player_3]

    def setup_cheating_player_mocks(self):
        def raise_error():
            raise Exception('error')

        player_1 = MagicMock()

        player_1.play.side_effect = raise_error
        player_2 = MagicMock()
        player_2.play.side_effect = raise_error
        player_3 = MagicMock()
        player_3.play.side_effect = raise_error
        return [player_1, player_2, player_3]
