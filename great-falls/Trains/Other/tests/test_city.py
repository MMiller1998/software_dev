import unittest
from Trains.Other.city import City
import importlib.util
import inspect
import pyclbr

class CityTests(unittest.TestCase):
    CITY_NAME_1 = "city1"
    CITY_NAME_2 = "city2"
    POSITION_1 = (0, 0)
    INVALID_POSITION = (-1, 50)

    def test_city_constructor_valid(self):
        city = City(self.CITY_NAME_1, (0, 0))

        self.assertEqual(self.CITY_NAME_1, city.name)
        self.assertEqual(self.POSITION_1, city.position)

    def test_city_constructor_invalid_coordinate(self):
        with self.assertRaises(ValueError):
            City(self.CITY_NAME_2, self.INVALID_POSITION)

    def test_city_constructor_name_too_long(self):
        with self.assertRaises(ValueError):
            City("areallylongnamethatismorethantwentysixcharacters", self.POSITION_1)

    def test_city_constructor_name_invalid_characters(self):
        with self.assertRaises(ValueError):
            City("washington; d!c!", self.POSITION_1)

    def test_city_equality(self):
        city_1 = City(self.CITY_NAME_1, (0, 0))
        city_2 = City(self.CITY_NAME_1, (0, 0))
        city_3 = City(self.CITY_NAME_1, (5, 5))

        self.assertTrue(city_1 == city_2)
        self.assertFalse(city_1 == city_3)