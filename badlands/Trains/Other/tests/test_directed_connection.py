import unittest
from Trains.Other.color import Color
from Trains.Other.directed_connection import DirectedConnection
from Trains.Other.city import City


class DirectedConnectionTests(unittest.TestCase):
    MAP_SIZE1 = 300
    CITY_NAME1 = "city1"
    CITY_NAME2 = "city2"
    POSITION1 = (0, 0)
    POSITION2 = (50, 50)
    LENGTH = 3
    INVALID_LENGTH = 2

    CITY1 = City(CITY_NAME1, POSITION1)
    CITY2 = City(CITY_NAME2, POSITION2)

    def test_directed_connection_constructor_valid(self):
        connection = DirectedConnection(self.CITY1, self.CITY2, self.LENGTH, Color.RED)
        self.assertEqual(self.CITY1, connection.from_city)
        self.assertEqual(self.CITY2, connection.to_city)
        self.assertEqual(self.LENGTH, connection.length)
        self.assertEqual(Color.RED, connection.color)

    def test_directed_connection_constructor_invalid_length(self):
        with self.assertRaises(ValueError):
            DirectedConnection(self.CITY1, self.CITY2, self.INVALID_LENGTH, Color.RED)

    def test_directed_connection_constructor_origin_same_as_destination(self):
        with self.assertRaises(ValueError):
            DirectedConnection(self.CITY1, self.CITY1, self.LENGTH, Color.RED)

    def test_make_undirected(self):
        directed_connection = DirectedConnection(self.CITY2, self.CITY1, self.LENGTH, Color.RED)
        undirected_connection = directed_connection.make_undirected()
        self.assertEqual(self.CITY1, undirected_connection.get_city_1())
        self.assertEqual(self.CITY2, undirected_connection.get_city_2())
        self.assertEqual(self.LENGTH, undirected_connection.length)
        self.assertEqual(Color.RED, undirected_connection.color)

    def test_directed_connection_hash(self):
        original_connection = DirectedConnection(self.CITY1, self.CITY2, self.LENGTH, Color.RED)
        same_connection = DirectedConnection(self.CITY1, self.CITY2, self.LENGTH, Color.RED)
        diff_cities_connection = DirectedConnection(self.CITY2, self.CITY1, self.LENGTH, Color.RED)
        diff_length_connection = DirectedConnection(self.CITY2, self.CITY1, self.LENGTH + 1, Color.RED)
        diff_color_connection = DirectedConnection(self.CITY1, self.CITY2, self.LENGTH, Color.BLUE)
        self.assertTrue(original_connection.__hash__() == same_connection.__hash__())
        self.assertFalse(original_connection.__hash__() == diff_cities_connection.__hash__())
        self.assertFalse(original_connection.__hash__() == diff_length_connection.__hash__())
        self.assertFalse(original_connection.__hash__() == diff_color_connection.__hash__())

    def test_directed_connection_equal(self):
        original_connection = DirectedConnection(self.CITY1, self.CITY2, self.LENGTH, Color.RED)
        same_connection = DirectedConnection(self.CITY1, self.CITY2, self.LENGTH, Color.RED)
        diff_cities_connection = DirectedConnection(self.CITY2, self.CITY1, self.LENGTH, Color.RED)
        diff_length_connection = DirectedConnection(self.CITY2, self.CITY1, self.LENGTH + 1, Color.RED)
        diff_color_connection = DirectedConnection(self.CITY1, self.CITY2, self.LENGTH, Color.BLUE)
        self.assertTrue(original_connection == same_connection)
        self.assertFalse(original_connection == diff_cities_connection)
        self.assertFalse(original_connection == diff_length_connection)
        self.assertFalse(original_connection == diff_color_connection)

