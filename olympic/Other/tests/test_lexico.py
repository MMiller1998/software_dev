import unittest
from trains.strategy.lexico import LexicographicPairOfCities, LexicographicConnection
from trains.map import TrainMap, RailColor
from tests.examples.milestone2 import bos, lax, bwi1 as bwi, mrtl


class PairOfCitiesTestCase(unittest.TestCase):
    def test_lexicographic_cities_basic(self):
        a = LexicographicPairOfCities(bos, lax)
        b = LexicographicPairOfCities(bwi, mrtl)
        self.assertTrue(a < b)
        self.assertTrue(b > a)

    def test_lexicographic_cities_city_order_flipped(self):
        a = LexicographicPairOfCities(lax, bos)
        b = LexicographicPairOfCities(bwi, mrtl)
        self.assertTrue(a < b)
        self.assertTrue(b > a)

    def test_lexicographic_cities_equal(self):
        a = LexicographicPairOfCities(lax, bos)
        b = LexicographicPairOfCities(lax, bos)
        self.assertTrue(a == b)


class ConnectionTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        tm = TrainMap(100, 200)
        cls.a = tm.add_place('a', 10, 20)
        cls.b = tm.add_place('b', 30, 40)
        cls.c = tm.add_place('c', 50, 60)
        cls.d = tm.add_place('d', 70, 80)
        cls.ab_3_green = LexicographicConnection(tm.add_connection(cls.a, cls.b, RailColor.GREEN, 3))
        cls.ab_3_red = LexicographicConnection(tm.add_connection(cls.a, cls.b, RailColor.RED, 3))
        cls.cd = LexicographicConnection(tm.add_connection(cls.c, cls.d, RailColor.BLUE, 4))
        cls.bd = LexicographicConnection(tm.add_connection(cls.b, cls.d, RailColor.BLUE, 4))
        cls.bc_4 = LexicographicConnection(tm.add_connection(cls.c, cls.b, RailColor.RED, 4))
        cls.bc_5 = LexicographicConnection(tm.add_connection(cls.b, cls.c, RailColor.BLUE, 5))

    def test_colors(self):
        self.assertTrue(self.ab_3_green < self.ab_3_red)
        self.assertTrue(self.ab_3_red > self.ab_3_green)

    def test_names(self):
        self.assertTrue(self.bd < self.cd)
        self.assertTrue(self.cd > self.bd)

    def test_segments(self):
        self.assertTrue(self.bc_4 < self.bc_5)
        self.assertTrue(self.bc_5 > self.bc_4)


if __name__ == '__main__':
    unittest.main()
