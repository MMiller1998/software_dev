import unittest
from Trains.Other.city import City
from Trains.Other.city_pair import CityPair

class CityPairTests(unittest.TestCase):
    CITY_NAME_1 = "city1"
    CITY_NAME_2 = "city2"
    CITY_NAME_3 = "city3"
    POSITION_1 = (0, 0)
    POSITION_2 = (50, 50)
    POSITION_3 = (100, 100)
    CITY_1 = City(CITY_NAME_1, POSITION_1)
    CITY_2 = City(CITY_NAME_2, POSITION_2)
    CITY_3 = City(CITY_NAME_3, POSITION_3)


    def test_city_pair_constructor_first_city_less(self):
        city_pair = CityPair(self.CITY_1, self.CITY_2)

        self.assertEqual(self.CITY_1, city_pair.city_1)
        self.assertEqual(self.CITY_2, city_pair.city_2)

    def test_city_pair_constructor_second_city_less(self):
        city_pair = CityPair(self.CITY_2, self.CITY_1)

        self.assertEqual(self.CITY_1, city_pair.city_1)
        self.assertEqual(self.CITY_2, city_pair.city_2)

    def test_city_pair_equality(self):
        city_pair_1 = CityPair(self.CITY_1, self.CITY_2)
        city_pair_2 = CityPair(self.CITY_2, self.CITY_1)
        city_pair_3 = CityPair(self.CITY_1, City("foo", (1,2)))

        self.assertTrue(city_pair_1 == city_pair_2)
        self.assertFalse(city_pair_1 == city_pair_3)

    def test_city_pair_lt_first_city(self):
        city_pair_1 = CityPair(self.CITY_1, self.CITY_2)
        city_pair_2 = CityPair(self.CITY_2, self.CITY_3)

        self.assertTrue(city_pair_1 < city_pair_2)

    def test_city_pair_lt_second_city(self):
        city_pair_1 = CityPair(self.CITY_1, self.CITY_2)
        city_pair_2 = CityPair(self.CITY_1, self.CITY_3)

        self.assertTrue(city_pair_1 < city_pair_2)