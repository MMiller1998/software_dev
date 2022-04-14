import unittest
from unittest.mock import MagicMock

from Trains.Other.interfaces.i_strategy import IStrategy
from Trains.Other.json_utils import *
from Trains.Common.map import Map
from Trains.Other.color import Color
from Trains.Other.directed_connection import DirectedConnection
from Trains.Other.undirected_connection import UndirectedConnection
from Trains.Other.city import City


class JsonUtilsTest(unittest.TestCase):
    LENGTH = 4
    CITY_NAME_1 = "city1"
    CITY_NAME_2 = "city2"
    CITY_NAME_3 = "city3"
    POSITION_1 = (350, 350)
    POSITION_2 = (400, 400)
    POSITION_3 = (400, 401)
    CITY_1 = City(CITY_NAME_1, POSITION_1)
    CITY_2 = City(CITY_NAME_2, POSITION_2)
    CITY_3 = City(CITY_NAME_3, POSITION_3)
    CITY_LIST = [CITY_1, CITY_2, CITY_3]

    DIRECTED_CONNECTION_1A = DirectedConnection(CITY_1, CITY_2, LENGTH, Color.RED)
    DIRECTED_CONNECTION_1B = DirectedConnection(CITY_2, CITY_1, LENGTH, Color.RED)

    def test_get_next_json_value(self):
        json_str = "\"city1\"\n\"city2\"\n{\"cities\": []}"
        city_1_name, json_str_1 = get_next_json_value(json_str)
        city_2_name, json_str_2 = get_next_json_value(json_str_1)
        map_dict, json_str_3 = get_next_json_value(json_str_2)
        self.assertEqual((city_1_name, json_str_1), ("city1", "\"city2\"\n{\"cities\": []}"))
        self.assertEqual((city_2_name, json_str_2), ("city2", "{\"cities\": []}"))
        self.assertEqual((map_dict, json_str_3), ({"cities": []}, ""))

    def test_find_city(self):
        self.assertEqual(find_city([self.CITY_1, self.CITY_2], self.CITY_NAME_1), self.CITY_1)

    def test_dict_to_map(self):
        map_dict = {
            "width": 500,
            "height": 800,
            "cities": [
                ["city1", [350, 350]],
                ["city2", [400, 400]]
            ],
            "connections": {
                "city1": {
                    "city2": {
                        "red": 4
                    }
                }
            }
        }

        expected_map = Map(500, 800,
                           [self.CITY_1, self.CITY_2],
                           [self.DIRECTED_CONNECTION_1A, self.DIRECTED_CONNECTION_1B])
        actual_map = dict_to_map(map_dict)
        self.assertEqual(actual_map.width, expected_map.width)
        self.assertEqual(actual_map.height, expected_map.height)
        self.assertEqual(actual_map.get_cities(), expected_map.get_cities())
        self.assertEqual(len(actual_map.get_outgoing_connections(self.CITY_1)), 1)
        self.assertEqual(len(actual_map.get_outgoing_connections(self.CITY_2)), 1)

    def test_array_to_undirected_connection(self):
        connection_arr = ["city1", "city2", "red", 5]
        actual_connection = array_to_undirected_connection(connection_arr, self.CITY_LIST)
        expected_connection = UndirectedConnection(self.CITY_1, self.CITY_2, 5, Color.RED)
        self.assertEqual(expected_connection, actual_connection)

    def test_array_to_public_state(self):
        connection_arr_1 = ["city1", "city2", "red", 5]
        connection_arr_2 = ["city1", "city2", "blue", 3]
        connection_arr_3 = ["city2", "city3", "white", 4]
        actual_public_state = array_to_public_state([connection_arr_1, connection_arr_2, connection_arr_3],
                                                    self.CITY_LIST)
        expected_acquired_connections = {UndirectedConnection(self.CITY_1, self.CITY_2, 5, Color.RED),
                                         UndirectedConnection(self.CITY_1, self.CITY_2, 3, Color.BLUE),
                                         UndirectedConnection(self.CITY_2, self.CITY_3, 4, Color.WHITE)}
        self.assertSetEqual(expected_acquired_connections, actual_public_state.acquired_connections)

    def test_dict_to_cards(self):
        cards_dict = {"red": 10, "blue": 0, "white": 4, "green": 20}
        actual_cards = dict_to_cards(cards_dict)
        self.assertEqual(10, actual_cards.get_card_count(Color.RED))
        self.assertEqual(0, actual_cards.get_card_count(Color.BLUE))
        self.assertEqual(4, actual_cards.get_card_count(Color.WHITE))
        self.assertEqual(20, actual_cards.get_card_count(Color.GREEN))

    def test_array_to_city(self):
        city_array = ["city1", [100, 100]]
        actual_city = array_to_city(city_array)
        self.assertEqual("city1", actual_city.name)
        self.assertTupleEqual((100, 100), actual_city.position)

    def test_array_to_destination(self):
        destination_array = ["city1", "city2"]
        actual_destination = array_to_destination(destination_array, self.CITY_LIST)
        self.assertEqual(Destination(self.CITY_1, self.CITY_2), actual_destination)

    def test_dict_to_private_player_state(self):
        private_player_state_dict = {
            "destination1": ["city1", "city2"],
            "destination2": ["city2", "city3"],
            "rails": 10,
            "cards": {},
            "acquired": [["city1", "city2", "red", 5]]
        }
        actual_private_player = dict_to_private_player_state(private_player_state_dict, self.CITY_LIST)
        self.assertSetEqual({Destination(self.CITY_1, self.CITY_2), Destination(self.CITY_2, self.CITY_3)},
                            actual_private_player.destinations)
        self.assertEqual(10, actual_private_player.num_rails)
        self.assertEqual(0, actual_private_player.cards.get_card_count(Color.RED))
        self.assertEqual(0, actual_private_player.cards.get_card_count(Color.BLUE))
        self.assertEqual(0, actual_private_player.cards.get_card_count(Color.WHITE))
        self.assertEqual(0, actual_private_player.cards.get_card_count(Color.GREEN))
        self.assertSetEqual({UndirectedConnection(self.CITY_1, self.CITY_2, 5, Color.RED)},
                            actual_private_player.public_state.acquired_connections)

    def test_dict_to_player_states(self):
        player_states_dict = {
            "this": {
                "destination1": ["city1", "city2"],
                "destination2": ["city2", "city3"],
                "rails": 10,
                "cards": {},
                "acquired": [["city1", "city2", "red", 5]]
            },
            "acquired": [[["city1", "city2", "red", 5]], [["city1", "city2", "blue", 3]]]
        }
        actual_private_player, actual_public_players = dict_to_player_states(player_states_dict,
                                                                                         self.CITY_LIST)
        self.assertSetEqual({Destination(self.CITY_1, self.CITY_2), Destination(self.CITY_2, self.CITY_3)},
                            actual_private_player.destinations)
        self.assertEqual(10, actual_private_player.num_rails)
        self.assertEqual(0, actual_private_player.cards.get_card_count(Color.RED))
        self.assertEqual(0, actual_private_player.cards.get_card_count(Color.BLUE))
        self.assertEqual(0, actual_private_player.cards.get_card_count(Color.WHITE))
        self.assertEqual(0, actual_private_player.cards.get_card_count(Color.GREEN))
        self.assertSetEqual({UndirectedConnection(self.CITY_1, self.CITY_2, 5, Color.RED)},
                            actual_private_player.public_state.acquired_connections)

        public_player_acquireds = [state.acquired_connections for state in actual_public_players]
        self.assertListEqual([{UndirectedConnection(self.CITY_1, self.CITY_2, 5, Color.RED)},
                              {UndirectedConnection(self.CITY_1, self.CITY_2, 3, Color.BLUE)}],
                             public_player_acquireds)

    def test_array_to_players(self):
        players_array = [["Name1", "Hold-10"], ["Name2", "Buy-Now"], ["Name3", "Cheat"]]
        players = array_to_players(players_array)
        self.assertTrue(issubclass(players[0].strategy, IStrategy))
        self.assertTrue(issubclass(players[1].strategy, IStrategy))
        self.assertTrue(issubclass(players[2].strategy, IStrategy))
        self.assertEqual("Name1", players[0].name)
        self.assertEqual("Name2", players[1].name)
        self.assertEqual("Name3", players[2].name)

    def test_array_to_player(self):
        player_array = ["Name1", "Hold-10"]
        player = array_to_player(player_array)
        self.assertTrue(issubclass(player.strategy, IStrategy))
        self.assertEqual("Name1", player.name)

    def test_serialize_undirected_connection(self):
        undirected_connection = UndirectedConnection(self.CITY_1, self.CITY_2, 5, Color.RED)
        serialized_undirected_connection = ["city1", "city2", "red", 5]

        self.assertListEqual(serialized_undirected_connection, serialize_undirected_connection(undirected_connection))

    def test_serialize_game_result(self):
        mock_game_result = MagicMock()
        mock_player_1 = MagicMock()
        mock_player_2 = MagicMock()
        mock_player_3 = MagicMock()
        mock_player_4 = MagicMock()
        mock_player_1.name = "Name1"
        mock_player_2.name = "Name2"
        mock_player_3.name = "Name3"
        mock_player_4.name = "Name4"
        mock_game_result.get_rankings.return_value = [[mock_player_3, mock_player_2], [mock_player_1]]
        mock_game_result.get_cheaters.return_value = [mock_player_4]

        self.assertListEqual([[["Name2", "Name3"], ["Name1"]], ["Name4"]], serialize_game_result(mock_game_result))
