import unittest
from unittest.mock import MagicMock
from Trains.Common.map import Map
from Trains.Other.player_state import *
from Trains.Other.city import City
from Trains.Other.color import Color
from Trains.Other.destination import Destination
from Trains.Other.strategy.buy_now import BuyNowStrategy
from Trains.Player.strategy import MORE_CARDS_REQUEST


class BuyNowStrategyTests(unittest.TestCase):
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
        self.assertSetEqual({self.DESTINATION_4, self.DESTINATION_5}, BuyNowStrategy.select_destinations(self.MAP, {
            self.DESTINATION_5, self.DESTINATION_2, self.DESTINATION_3, self.DESTINATION_4, self.DESTINATION_1}))

    def test_get_turn_no_acquirable_connections(self):
        mock_player_game_state = MagicMock()
        mock_player_game_state.get_acquirable_connections.return_value = set()
        self.assertEqual(MORE_CARDS_REQUEST, BuyNowStrategy.get_turn(mock_player_game_state))

    def test_get_turn_has_acquirable_connections(self):
        mock_player_game_state = MagicMock()
        mock_player_game_state.get_acquirable_connections.return_value = {
            UndirectedConnection(self.CITY_3, self.CITY_4, 4, Color.RED),
            UndirectedConnection(self.CITY_1, self.CITY_2, 4, Color.RED),
            UndirectedConnection(self.CITY_2, self.CITY_3, 4, Color.RED)}
        self.assertEqual(UndirectedConnection(self.CITY_1, self.CITY_2, 4, Color.RED),
                         BuyNowStrategy.get_turn(mock_player_game_state))

