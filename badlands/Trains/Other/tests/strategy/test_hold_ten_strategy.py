import unittest
from unittest.mock import MagicMock
from Trains.Common.map import Map
from Trains.Other.player_state import *
from Trains.Other.city import City
from Trains.Other.color import Color
from Trains.Other.destination import Destination
from Trains.Other.strategy.hold_ten import HoldTenStrategy
from Trains.Player.strategy import MORE_CARDS_REQUEST


class HoldTenStrategyTests(unittest.TestCase):
    CITY_1 = City("city1", (0, 0))
    CITY_2 = City("city2", (1, 1))
    CITY_3 = City("city3", (2, 2))
    CITY_4 = City("city4", (3, 3))

    DESTINATION_1 = Destination(CITY_1, CITY_2)
    DESTINATION_2 = Destination(CITY_1, CITY_3)
    DESTINATION_3 = Destination(CITY_1, CITY_4)
    DESTINATION_4 = Destination(CITY_2, CITY_3)
    DESTINATION_5 = Destination(CITY_2, CITY_4)

    MAP = Map(400, 400, [], [])

    def test_select_destinations(self):
        self.assertSetEqual({self.DESTINATION_1, self.DESTINATION_2}, HoldTenStrategy.select_destinations(self.MAP, {
            self.DESTINATION_5, self.DESTINATION_2, self.DESTINATION_3, self.DESTINATION_4, self.DESTINATION_1}))

    def test_get_turn_less_than_ten_cards(self):
        mock_player_game_state = self.__setup_mock_player_state(9)
        self.assertEqual(MORE_CARDS_REQUEST, HoldTenStrategy.get_turn(mock_player_game_state))

    def test_get_turn_ten_cards(self):
        mock_player_game_state = self.__setup_mock_player_state(10)
        self.assertEqual(MORE_CARDS_REQUEST, HoldTenStrategy.get_turn(mock_player_game_state))

    def test_get_turn_greater_than_ten_cards(self):
        mock_player_game_state = self.__setup_mock_player_state(11)
        mock_player_game_state.get_acquirable_connections.return_value = {
            UndirectedConnection(self.CITY_3, self.CITY_4, 4, Color.RED),
            UndirectedConnection(self.CITY_1, self.CITY_2, 4, Color.RED),
            UndirectedConnection(self.CITY_2, self.CITY_3, 4, Color.RED)}
        self.assertEqual(UndirectedConnection(self.CITY_1, self.CITY_2, 4, Color.RED),
                         HoldTenStrategy.get_turn(mock_player_game_state))

    def test_get_turn_greater_than_ten_cards_no_more_connections(self):
        mock_player_game_state = self.__setup_mock_player_state(11)
        mock_player_game_state.get_acquirable_connections.return_value = {}
        self.assertEqual(MORE_CARDS_REQUEST, HoldTenStrategy.get_turn(mock_player_game_state))

    def __setup_mock_player_state(self, card_count: int) -> MagicMock:
        mock_player_game_state = MagicMock()
        mock_private_state = MagicMock()
        mock_cards = MagicMock()
        mock_player_game_state.own_state = mock_private_state
        mock_private_state.cards = mock_cards
        mock_cards.get_total_count.return_value = card_count
        return mock_player_game_state
