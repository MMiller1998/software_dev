import unittest
from Trains.Other.color import Color
from Trains.Other.directed_connection import DirectedConnection
from Trains.Common.map import Map
from Trains.Other.city import City
from Trains.Other.destination import Destination


class MapTests(unittest.TestCase):
    MAP_WIDTH = 800
    MAP_HEIGHT = 800

    INVALID_MAP_SIZE_NEG = -25
    INVALID_MAP_SIZE_BIG = 1500
    LENGTH = 3

    STARTING_RAILS = 45

    CITY_NAME_1 = "city1"
    CITY_NAME_2 = "city2"
    CITY_NAME_3 = "city3"
    CITY_NAME_4 = "city4"
    CITY_NAME_5 = "city5"
    CITY_NAME_6 = "city6"

    POSITION_1 = (0, 0)
    POSITION_2 = (50, 50)
    POSITION_3 = (75, 50)
    POSITION_4 = (50, 250)
    POSITION_5 = (300, 300)
    POSITION_6 = (300, 301)
    INVALID_POSITION = (MAP_WIDTH + 1, MAP_HEIGHT + 1)

    CITY_1 = City(CITY_NAME_1, POSITION_1)
    CITY_2 = City(CITY_NAME_2, POSITION_2)
    CITY_3 = City(CITY_NAME_3, POSITION_3)
    CITY_4 = City(CITY_NAME_4, POSITION_4)
    CITY_5 = City(CITY_NAME_5, POSITION_5)
    CITY_6 = City(CITY_NAME_6, POSITION_6)
    CITY_LIST = [CITY_1, CITY_2, CITY_3, CITY_4, CITY_5, CITY_6]
    CITY_OUTSIDE_BOARD = City(CITY_NAME_5, INVALID_POSITION)

    DESTINATION_1 = Destination(CITY_1, CITY_2)
    DESTINATION_2 = Destination(CITY_1, CITY_3)
    DESTINATION_3 = Destination(CITY_4, CITY_5)
    DESTINATION_4 = Destination(CITY_2, CITY_3)

    DIRECTED_CONNECTION_1A = DirectedConnection(CITY_1, CITY_2, LENGTH, Color.RED)
    DIRECTED_CONNECTION_1B = DirectedConnection(CITY_2, CITY_1, LENGTH, Color.RED)
    DUPLICATE_DIRECTED_CONNECTION_1A = DirectedConnection(CITY_1, CITY_2, LENGTH, Color.RED)
    DIRECTED_CONNECTION_2A = DirectedConnection(CITY_1, CITY_3, LENGTH, Color.RED)
    DIRECTED_CONNECTION_2B = DirectedConnection(CITY_3, CITY_1, LENGTH, Color.RED)
    DIRECTED_CONNECTION_3A = DirectedConnection(CITY_4, CITY_5, LENGTH, Color.RED)
    DIRECTED_CONNECTION_3B = DirectedConnection(CITY_5, CITY_4, LENGTH, Color.RED)
    DIRECTED_CONNECTION_LIST_SIMPLE_GRAPH = [DIRECTED_CONNECTION_1A, DIRECTED_CONNECTION_1B,
                                             DIRECTED_CONNECTION_2A, DIRECTED_CONNECTION_2B,
                                             DIRECTED_CONNECTION_3A, DIRECTED_CONNECTION_3B]

    DIRECTED_CONNECTION_1_2 = DirectedConnection(CITY_1, CITY_2, LENGTH, Color.RED)
    DIRECTED_CONNECTION_2_1 = DirectedConnection(CITY_2, CITY_1, LENGTH, Color.RED)
    DIRECTED_CONNECTION_2_3_RED = DirectedConnection(CITY_2, CITY_3, LENGTH, Color.RED)
    DIRECTED_CONNECTION_3_2_RED = DirectedConnection(CITY_3, CITY_2, LENGTH, Color.RED)
    DIRECTED_CONNECTION_2_3_BLUE = DirectedConnection(CITY_2, CITY_3, 5, Color.BLUE)
    DIRECTED_CONNECTION_3_2_BLUE = DirectedConnection(CITY_3, CITY_2, 5, Color.BLUE)
    DIRECTED_CONNECTION_3_4 = DirectedConnection(CITY_3, CITY_4, LENGTH, Color.RED)
    DIRECTED_CONNECTION_4_3 = DirectedConnection(CITY_4, CITY_3, LENGTH, Color.RED)
    DIRECTED_CONNECTION_3_5_RED = DirectedConnection(CITY_3, CITY_5, LENGTH, Color.RED)
    DIRECTED_CONNECTION_5_3_RED = DirectedConnection(CITY_5, CITY_3, LENGTH, Color.RED)
    DIRECTED_CONNECTION_3_5_BLUE = DirectedConnection(CITY_3, CITY_5, 5, Color.BLUE)
    DIRECTED_CONNECTION_5_3_BLUE = DirectedConnection(CITY_5, CITY_3, 5, Color.BLUE)
    DIRECTED_CONNECTION_2_5_BLUE = DirectedConnection(CITY_2, CITY_5, LENGTH, Color.BLUE)
    DIRECTED_CONNECTION_5_2_BLUE = DirectedConnection(CITY_5, CITY_2, LENGTH, Color.BLUE)
    DIRECTED_CONNECTION_2_5_RED = DirectedConnection(CITY_2, CITY_5, 5, Color.RED)
    DIRECTED_CONNECTION_5_2_RED = DirectedConnection(CITY_5, CITY_2, 5, Color.RED)
    DIRECTED_CONNECTION_5_6 = DirectedConnection(CITY_5, CITY_6, 4, Color.RED)
    DIRECTED_CONNECTION_6_5 = DirectedConnection(CITY_6, CITY_5, 4, Color.RED)
    DIRECTED_CONNECTION_LIST_COMPLEX_GRAPH = [DIRECTED_CONNECTION_1_2,
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

    def test_map_constructor_valid(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, [self.CITY_1, self.CITY_2],
                        [self.DIRECTED_CONNECTION_1A, self.DIRECTED_CONNECTION_1B])
        self.assertEqual(self.MAP_WIDTH, train_map.width)
        self.assertEqual(self.MAP_HEIGHT, train_map.height)
        self.assertEqual([self.CITY_1, self.CITY_2], train_map.get_cities())

    def test_map_constructor_valid_no_connections(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, [self.CITY_1, self.CITY_2], [])
        self.assertEqual(self.MAP_WIDTH, train_map.width)
        self.assertEqual(self.MAP_HEIGHT, train_map.height)
        self.assertEqual([self.CITY_1, self.CITY_2], train_map.get_cities())

    def test_map_constructor_valid_empty(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, [], [])
        self.assertEqual(self.MAP_WIDTH, train_map.width)
        self.assertEqual(self.MAP_HEIGHT, train_map.height)
        self.assertEqual([], train_map.get_cities())

    def test_map_constructor_invalid_size(self):
        with self.assertRaises(ValueError):
            Map(self.INVALID_MAP_SIZE_NEG, self.INVALID_MAP_SIZE_NEG, [self.CITY_1, self.CITY_2],
                [self.DIRECTED_CONNECTION_1A, self.DIRECTED_CONNECTION_1B])

        with self.assertRaises(ValueError):
            Map(self.INVALID_MAP_SIZE_BIG, self.INVALID_MAP_SIZE_BIG, [self.CITY_1, self.CITY_2],
                [self.DIRECTED_CONNECTION_1A, self.DIRECTED_CONNECTION_1B])

    def test_map_constructor_invalid_duplicate_colors(self):
        with self.assertRaises(ValueError):
            Map(self.MAP_WIDTH, self.MAP_HEIGHT, [self.CITY_1, self.CITY_2],
                [self.DIRECTED_CONNECTION_1A, self.DIRECTED_CONNECTION_1B, self.DUPLICATE_DIRECTED_CONNECTION_1A])

    def test_map_constructor_invalid_city_position(self):
        with self.assertRaises(ValueError):
            Map(self.MAP_WIDTH, self.MAP_HEIGHT, [self.CITY_OUTSIDE_BOARD, self.CITY_2],
                [self.DIRECTED_CONNECTION_1A, self.DIRECTED_CONNECTION_1B])

    def test_map_constructor_invalid_connection_city(self):
        with self.assertRaises(ValueError):
            Map(self.MAP_WIDTH, self.MAP_HEIGHT, [self.CITY_1, self.CITY_2],
                [self.DIRECTED_CONNECTION_2A, self.DIRECTED_CONNECTION_2B])

    def test_map_constructor_invalid_asymmetric_connections(self):
        with self.assertRaises(ValueError):
            Map(self.MAP_WIDTH, self.MAP_HEIGHT, [self.CITY_1, self.CITY_2, self.CITY_3],
                [self.DIRECTED_CONNECTION_1A, self.DIRECTED_CONNECTION_1B,
                 self.DIRECTED_CONNECTION_2A])

    def test_map_get_cities(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, [self.CITY_1, self.CITY_2],
                        [self.DIRECTED_CONNECTION_1A, self.DIRECTED_CONNECTION_1B])
        self.assertEqual([self.CITY_1, self.CITY_2], train_map.get_cities())

    def test_map_get_city_names(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, [self.CITY_1, self.CITY_2],
                        [self.DIRECTED_CONNECTION_1A, self.DIRECTED_CONNECTION_1B])
        self.assertEqual([self.CITY_NAME_1, self.CITY_NAME_2], train_map.get_city_names())

    def test_map_get_outgoing_connections(self):
        city_1_outgoing = [self.DIRECTED_CONNECTION_1A,
                           self.DIRECTED_CONNECTION_2A]
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, self.CITY_LIST, self.DIRECTED_CONNECTION_LIST_SIMPLE_GRAPH)
        self.assertEqual(city_1_outgoing, train_map.get_outgoing_connections(self.CITY_1))

    def test_map_get_feasible_destinations(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, self.CITY_LIST, self.DIRECTED_CONNECTION_LIST_SIMPLE_GRAPH)
        self.assertEqual({self.DESTINATION_1, self.DESTINATION_2, self.DESTINATION_3, self.DESTINATION_4},
                         train_map.get_feasible_destinations(self.STARTING_RAILS))

    def test_map_get_feasible_destinations_empty_map(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, self.CITY_LIST, [])
        self.assertEqual(set(), train_map.get_feasible_destinations(self.STARTING_RAILS))

    def test_map_get_feasible_destinations_max_rails(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, self.CITY_LIST, self.DIRECTED_CONNECTION_LIST_SIMPLE_GRAPH)
        self.assertSetEqual({self.DESTINATION_1, self.DESTINATION_2, self.DESTINATION_3},
                            train_map.get_feasible_destinations(3))

    def test_map_get_all_directed_connections(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, self.CITY_LIST, self.DIRECTED_CONNECTION_LIST_SIMPLE_GRAPH)
        self.assertListEqual(
            sorted(self.DIRECTED_CONNECTION_LIST_SIMPLE_GRAPH, key=lambda conn: (conn.from_city, conn.color.value)),
            sorted(train_map.get_all_directed_connections(),
                   key=lambda conn: (conn.from_city, conn.color.value)))

    def test_map_are_cities_connected_same_component(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, self.CITY_LIST, self.DIRECTED_CONNECTION_LIST_SIMPLE_GRAPH)
        self.assertTrue(
            train_map.are_cities_connected(self.CITY_2, self.CITY_3, set(self.DIRECTED_CONNECTION_LIST_SIMPLE_GRAPH)))

    def test_map_are_cities_connected_different_component(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, self.CITY_LIST, self.DIRECTED_CONNECTION_LIST_SIMPLE_GRAPH)
        self.assertFalse(
            train_map.are_cities_connected(self.CITY_2, self.CITY_5, set(self.DIRECTED_CONNECTION_LIST_SIMPLE_GRAPH)))

    def test_map_are_cities_connected_no_acquireds(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, self.CITY_LIST, self.DIRECTED_CONNECTION_LIST_SIMPLE_GRAPH)
        self.assertFalse(train_map.are_cities_connected(self.CITY_2, self.CITY_1, set()))

    def test_map_are_cities_connected_missing_connection(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, self.CITY_LIST, self.DIRECTED_CONNECTION_LIST_SIMPLE_GRAPH)
        self.assertFalse(train_map.are_cities_connected(self.CITY_2, self.CITY_3, {self.DIRECTED_CONNECTION_1A,
                                                                                   self.DIRECTED_CONNECTION_1B}))

    def test_map_longest_continuous_path_separate_components(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, self.CITY_LIST, self.DIRECTED_CONNECTION_LIST_SIMPLE_GRAPH)
        self.assertEqual(6, train_map.longest_continuous_route(set(self.DIRECTED_CONNECTION_LIST_SIMPLE_GRAPH)))

    def test_map_longest_continuous_path_cyclic_map(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, self.CITY_LIST, self.DIRECTED_CONNECTION_LIST_COMPLEX_GRAPH)
        self.assertEqual(17, train_map.longest_continuous_route(set(self.DIRECTED_CONNECTION_LIST_COMPLEX_GRAPH)))

    def test_map_longest_continuous_path_cyclic_map_missing_connection(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, self.CITY_LIST, self.DIRECTED_CONNECTION_LIST_COMPLEX_GRAPH)
        self.assertEqual(16, train_map.longest_continuous_route(
            set(self.DIRECTED_CONNECTION_LIST_COMPLEX_GRAPH) - {self.DIRECTED_CONNECTION_5_6,
                                                                self.DIRECTED_CONNECTION_6_5}))

    def test_map_longest_continuous_path_cyclic_map_missing_connection_same_length(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, self.CITY_LIST, self.DIRECTED_CONNECTION_LIST_COMPLEX_GRAPH)
        self.assertEqual(17, train_map.longest_continuous_route(
            set(self.DIRECTED_CONNECTION_LIST_COMPLEX_GRAPH) - {self.DIRECTED_CONNECTION_5_3_BLUE,
                                                                self.DIRECTED_CONNECTION_3_5_BLUE}))

    def test_map_longest_continuous_path_cyclic_map_no_acquireds(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, self.CITY_LIST, self.DIRECTED_CONNECTION_LIST_COMPLEX_GRAPH)
        self.assertEqual(0, train_map.longest_continuous_route(set()))

    def test_map_longest_continuous_path_cyclic_map_separate_components(self):
        train_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT, self.CITY_LIST, self.DIRECTED_CONNECTION_LIST_COMPLEX_GRAPH)
        self.assertEqual(12, train_map.longest_continuous_route(
            set(self.DIRECTED_CONNECTION_LIST_COMPLEX_GRAPH) - {self.DIRECTED_CONNECTION_5_3_BLUE,
                                                                self.DIRECTED_CONNECTION_3_5_BLUE,
                                                                self.DIRECTED_CONNECTION_5_3_RED,
                                                                self.DIRECTED_CONNECTION_3_5_RED,
                                                                self.DIRECTED_CONNECTION_2_3_BLUE,
                                                                self.DIRECTED_CONNECTION_3_2_BLUE,
                                                                self.DIRECTED_CONNECTION_2_3_RED,
                                                                self.DIRECTED_CONNECTION_3_2_RED}))


if __name__ == '__main__':
    unittest.main()
