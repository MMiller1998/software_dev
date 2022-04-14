import unittest
from Trains.Other.color import Color
from Trains.Other.directed_connection import DirectedConnection
from Trains.Other.undirected_connection import UndirectedConnection
from Trains.Other.city import City


class UndirectedConnectionTests(unittest.TestCase):
    CITY_NAME1 = "city1"
    CITY_NAME2 = "city2"
    CITY_NAME3 = "city3"
    POSITION1 = (0, 0)
    POSITION2 = (50, 50)
    POSITION3 = (100, 100)
    LENGTH = 3
    INVALID_LENGTH = 2

    CITY1 = City(CITY_NAME1, POSITION1)
    CITY2 = City(CITY_NAME2, POSITION2)
    CITY3 = City(CITY_NAME3, POSITION3)

    def test_undirected_connection_constructor_valid(self):
        connection = UndirectedConnection(self.CITY1, self.CITY2, self.LENGTH, Color.RED)
        self.assertEqual(self.CITY1, connection.get_city_1())
        self.assertEqual(self.CITY2, connection.get_city_2())
        self.assertEqual(self.LENGTH, connection.length)
        self.assertEqual(Color.RED, connection.color)

    def test_undirected_connection_constructor_invalid_length(self):
        with self.assertRaises(ValueError):
            UndirectedConnection(self.CITY1, self.CITY2, self.INVALID_LENGTH, Color.RED)

    def test_undirected_connection_constructor_origin_same_as_destination(self):
        with self.assertRaises(ValueError):
            UndirectedConnection(self.CITY1, self.CITY1, self.LENGTH, Color.RED)

    def test_undirected_connection_hash(self):
        connection_1 = UndirectedConnection(self.CITY1, self.CITY2, self.LENGTH, Color.RED)
        connection_2 = UndirectedConnection(self.CITY2, self.CITY1, self.LENGTH, Color.RED)
        self.assertTrue(connection_1.__hash__() == connection_2.__hash__())

    def test_undirected_connection_lt_city_pair(self):
        connection_1 = UndirectedConnection(self.CITY1, self.CITY2, self.LENGTH, Color.RED)
        connection_2 = UndirectedConnection(self.CITY2, self.CITY3, self.LENGTH, Color.RED)
        self.assertTrue(connection_1 < connection_2)

    def test_undirected_connection_lt_length(self):
        connection_1 = UndirectedConnection(self.CITY1, self.CITY2, self.LENGTH, Color.RED)
        connection_2 = UndirectedConnection(self.CITY2, self.CITY1, self.LENGTH + 1, Color.RED)
        self.assertTrue(connection_1 < connection_2)

    def test_undirected_connection_lt_color(self):
        connection_1 = UndirectedConnection(self.CITY1, self.CITY2, self.LENGTH, Color.BLUE)
        connection_2 = UndirectedConnection(self.CITY2, self.CITY1, self.LENGTH, Color.RED)
        self.assertTrue(connection_1 < connection_2)

