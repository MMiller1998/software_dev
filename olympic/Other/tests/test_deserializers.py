import unittest

from trains.state.action import WantCards, Acquire
from trains.json.deserializers import (
    deserialize_map, deserialize_destination, deserialize_destinations,
    deserialize_player_instance, deserialize_player_instances, deserialize_color, deserialize_colors,
    deserialize_card_star, deserialize_action_option, deserialize_acquired, deserialize_player,
    deserialize_this_player, deserialize_other_players, deserialize_player_state
)
from trains.map import TrainMap
from trains.graph_elements import RailColor

MAP_WIDTH = 500
MAP_HEIGHT = 600


class TestDeserializers(unittest.TestCase):

    def setUp(self):
        self.train_map = TrainMap(MAP_WIDTH, MAP_HEIGHT)
        self.bos = self.train_map.add_place('BOS', 276, 34)
        self.bwi = self.train_map.add_place('BWI', 114, 324)
        self.iad = self.train_map.add_place('IAD', 372, 319)
        self.jfk = self.train_map.add_place('JFK', 226, 216)

        self.c_bos_bwi = self.train_map.add_connection(
            self.bos, self.bwi, color=RailColor.RED, length=4)
        self.c_bos_jfk = self.train_map.add_connection(
            self.bos, self.jfk, color=RailColor.RED, length=4)
        self.c_bwi_iad1 = self.train_map.add_connection(
            self.bwi, self.iad, color=RailColor.BLUE, length=4)
        self.c_bwi_iad2 = self.train_map.add_connection(
            self.bwi, self.iad, color=RailColor.GREEN, length=4)

        self.all_cities = [self.bos, self.bwi, self.iad, self.jfk]

    def test_deserialize_map(self):
        train_map_data = {
            "width": MAP_WIDTH,
            "height": MAP_HEIGHT,
            "cities": [
                ["BOS", [276, 34]],
                ["BWI", [114, 324]],
                ["IAD", [372, 319]],
                ["JFK", [226, 216]]
            ],
            "connections": {
                "BOS": {
                    "BWI": {
                        "red": 4
                    },
                    "JFK": {
                        "red": 4
                    }
                },
                "BWI": {
                    "IAD": {
                        "blue": 4,
                        "green": 4
                    }
                }
            }
        }
        expected_train_map = self.train_map
        actual_train_map = deserialize_map(train_map_data)
        self.assertSetEqual(set(actual_train_map.get_all_places()), set(expected_train_map.get_all_places()))
        self.assertSetEqual(set(actual_train_map.get_all_connections()), set(expected_train_map.get_all_connections()))

    def test_deserialize_destination(self):
        destination_data = ["BOS", "BWI"]
        expected_destination = {self.bos, self.bwi}
        actual_destination = deserialize_destination(self.train_map, destination_data)
        self.assertSetEqual(actual_destination, expected_destination)

    def test_deserialize_destinations(self):
        destinations_data = [["BOS", "BWI"], ["BWI", "IAD"]]
        expected_destinations = {frozenset([self.bos, self.bwi]), frozenset([self.bwi, self.iad])}
        actual_destinations = deserialize_destinations(self.train_map, destinations_data)
        self.assertSetEqual(actual_destinations, expected_destinations)

    def test_deserialize_player_instance(self):
        # note: This does not test that the player is constructed with the correct strategy
        player_instance_data = ["Name1", "Buy-Now"]
        actual_player = deserialize_player_instance(self.train_map, player_instance_data)
        self.assertEqual(actual_player.name, "Name1")
        self.assertIs(actual_player.train_map_for_start, self.train_map)

    def test_deserialize_player_instances(self):
        # note: This does not test that the players are constructed with the correct strategies
        player_instances_data = [["Name1", "Buy-Now"], ["Name2", "Buy-Now"], ["Name3", "Hold-10"]]
        player1, player2, player3 = deserialize_player_instances(self.train_map, player_instances_data)
        self.assertEqual(player1.name, "Name1")
        self.assertIs(player1.train_map_for_start, self.train_map)
        self.assertEqual(player2.name, "Name2")
        self.assertIs(player2.train_map_for_start, self.train_map)
        self.assertEqual(player3.name, "Name3")
        self.assertIs(player3.train_map_for_start, self.train_map)

    def test_deserialize_color(self):
        color_data = "blue"
        actual_color = deserialize_color(color_data)
        self.assertEqual(actual_color, RailColor.BLUE)

    def test_deserialize_colors(self):
        colors_data = ["blue", "red", "green", "white"]
        actual_colors = deserialize_colors(colors_data)
        self.assertListEqual(actual_colors, [RailColor.BLUE, RailColor.RED, RailColor.GREEN, RailColor.WHITE])

    def test_deserialize_card_star(self):
        card_star_data = {
            "blue": 2,
            "green": 3,
            "white": 4,
        }
        actual_card_hand = deserialize_card_star(card_star_data)
        expected_card_hand = {
            RailColor.RED: 0,
            RailColor.BLUE: 2,
            RailColor.GREEN: 3,
            RailColor.WHITE: 4,
        }
        self.assertDictEqual(actual_card_hand, expected_card_hand)

    def test_deserialize_acquired(self):
        acquired_data = ("BOS", "BWI", "red", 4)
        actual_acquired = deserialize_acquired(self.train_map, acquired_data)
        self.assertIs(actual_acquired, self.c_bos_bwi)

    def test_deserialize_action_option_more_cards(self):
        action_option_data = "more cards"
        actual_action_option = deserialize_action_option(self.train_map, action_option_data)
        self.assertIsInstance(actual_action_option, WantCards)

    def test_deserialize_action_option_acquire(self):
        action_option_data = ("BOS", "BWI", "red", 4)
        actual_action_option = deserialize_action_option(self.train_map, action_option_data)
        self.assertIsInstance(actual_action_option, Acquire)
        self.assertIs(actual_action_option.connection, self.c_bos_bwi)

    def test_deserialize_player(self):
        player_data = [("BOS", "BWI", "red", 4), ("BWI", "IAD", "blue", 4)]
        actual_player = deserialize_player(self.train_map, player_data)
        self.assertListEqual(actual_player, [self.c_bos_bwi, self.c_bwi_iad1])

    def test_deserialize_this_player(self):
        this_player_data = {
            "destination1": ["BOS", "BWI"],
            "destination2": ["BWI", "IAD"],
            "rails": 42,
            "cards": {
                "red": 5,
                "blue": 3
            },
            "acquired": [("BOS", "BWI", "red", 4), ("BWI", "IAD", "blue", 4)]
        }
        actual_player_state = deserialize_this_player(self.train_map, this_player_data)

        self.assertSetEqual(actual_player_state.destinations, {frozenset([self.bos, self.bwi]), frozenset([self.bwi, self.iad])})
        self.assertEqual(actual_player_state.num_rails, 42)
        self.assertDictEqual(actual_player_state.cards, {RailColor.RED: 5, RailColor.BLUE: 3, RailColor.GREEN: 0, RailColor.WHITE: 0})
        self.assertSetEqual(actual_player_state.occupied, frozenset([self.c_bos_bwi, self.c_bwi_iad1]))

    def test_deserialize_other_players(self):
        other_players_data = [
            [("BOS", "BWI", "red", 4), ("BWI", "IAD", "blue", 4)],
            [("BOS", "JFK", "red", 4), ("BWI", "IAD", "green", 4)],
            []
        ]
        actual_other_players_acquired = deserialize_other_players(self.train_map, other_players_data)

        self.assertEqual(len(actual_other_players_acquired), 3)
        self.assertListEqual(actual_other_players_acquired[0], [self.c_bos_bwi, self.c_bwi_iad1])
        self.assertListEqual(actual_other_players_acquired[1], [self.c_bos_jfk, self.c_bwi_iad2])
        self.assertListEqual(actual_other_players_acquired[2], [])

    def test_deserialize_player_state(self):
        player_state_data = {
            "this": {
                "destination1": ["BOS", "BWI"],
                "destination2": ["BWI", "IAD"],
                "rails": 42,
                "cards": {
                    "red": 5,
                    "blue": 3
                },
                "acquired": [("BOS", "BWI", "red", 4), ("BWI", "IAD", "blue", 4)]
            },
            "acquired": [
                [("BOS", "BWI", "red", 4), ("BWI", "IAD", "blue", 4)],
                [("BOS", "JFK", "red", 4), ("BWI", "IAD", "green", 4)],
                []
            ]
        }
        actual_player_state_wrapper = deserialize_player_state(self.train_map, player_state_data)
        actual_player_state = actual_player_state_wrapper.player_state
        actual_other_player_acquireds = actual_player_state_wrapper.other_player_acquireds

        self.assertSetEqual(actual_player_state.destinations, {frozenset([self.bos, self.bwi]), frozenset([self.bwi, self.iad])})
        self.assertEqual(actual_player_state.num_rails, 42)
        self.assertDictEqual(actual_player_state.cards, {RailColor.RED: 5, RailColor.BLUE: 3, RailColor.GREEN: 0, RailColor.WHITE: 0})
        self.assertSetEqual(actual_player_state.occupied, frozenset([self.c_bos_bwi, self.c_bwi_iad1]))

        self.assertEqual(len(actual_other_player_acquireds), 3)
        self.assertListEqual(actual_other_player_acquireds[0], [self.c_bos_bwi, self.c_bwi_iad1])
        self.assertListEqual(actual_other_player_acquireds[1], [self.c_bos_jfk, self.c_bwi_iad2])
        self.assertListEqual(actual_other_player_acquireds[2], [])
