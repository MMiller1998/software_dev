import unittest
from Trains.Other.player_state import PublicPlayerState
from Trains.Other.undirected_connection import UndirectedConnection
from Trains.Other.city import City
from Trains.Other.color import Color


class PublicPlayerStateTests(unittest.TestCase):
    CITY_NAME_1 = "city1"
    CITY_NAME_2 = "city2"
    CITY_NAME_3 = "city3"
    POSITION_1 = (350, 350)
    POSITION_2 = (400, 400)
    POSITION_3 = (10, 750)
    CITY_1 = City(CITY_NAME_1, POSITION_1)
    CITY_2 = City(CITY_NAME_2, POSITION_2)
    CITY_3 = City(CITY_NAME_3, POSITION_3)

    UNDIRECTED_CONNECTION_1 = UndirectedConnection(CITY_1, CITY_2, 3, Color.GREEN)
    UNDIRECTED_CONNECTION_2 = UndirectedConnection(CITY_2, CITY_3, 3, Color.GREEN)

    CONNECTION_SET_1 = {UNDIRECTED_CONNECTION_1, UNDIRECTED_CONNECTION_2}

    def test_constructor_valid(self):
        actual_state = PublicPlayerState(self.CONNECTION_SET_1)

        self.assertTrue(self.UNDIRECTED_CONNECTION_1 in actual_state.acquired_connections)
        self.assertTrue(self.UNDIRECTED_CONNECTION_2 in actual_state.acquired_connections)

    def test_eq(self):
        player_state_1 = PublicPlayerState(self.CONNECTION_SET_1)
        player_state_2 = PublicPlayerState(self.CONNECTION_SET_1)
        self.assertTrue(player_state_1 == player_state_2)

    def test_not_eq(self):
        player_state_1 = PublicPlayerState(self.CONNECTION_SET_1)
        player_state_2 = PublicPlayerState({self.UNDIRECTED_CONNECTION_1})
        self.assertFalse(player_state_1 == player_state_2)

    def test_hash_eq(self):
        player_state_1 = PublicPlayerState(self.CONNECTION_SET_1)
        player_state_2 = PublicPlayerState(self.CONNECTION_SET_1)
        self.assertEqual(player_state_2.__hash__(), player_state_1.__hash__())

    def test_hash_not_eq(self):
        player_state_1 = PublicPlayerState(self.CONNECTION_SET_1)
        player_state_2 = PublicPlayerState({self.UNDIRECTED_CONNECTION_1})
        self.assertNotEqual(player_state_2.__hash__(), player_state_1.__hash__())

    def test_add_connection(self):
        player_state = PublicPlayerState({self.UNDIRECTED_CONNECTION_1})
        player_state_added_connection = player_state.add_connection(self.UNDIRECTED_CONNECTION_2)

        self.assertEqual(2, len(player_state_added_connection.acquired_connections))
        self.assertTrue(self.UNDIRECTED_CONNECTION_2 in player_state_added_connection.acquired_connections)

