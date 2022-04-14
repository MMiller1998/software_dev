import unittest

from Trains.Other.city import City
from Trains.Other.destination import Destination
from Trains.Other.ref_destination_options_strategy import RandomDestinationOptionsStrategy


class RandomDestinationOptionsStrategyTests(unittest.TestCase):
    CITY_1 = City("city1", (0, 0))
    CITY_2 = City("city2", (1, 0))
    CITY_3 = City("city3", (2, 0))
    CITY_4 = City("city4", (3, 0))
    CITY_5 = City("city5", (4, 0))

    CITY_LIST = [CITY_1, CITY_2, CITY_3, CITY_4, CITY_5]

    DEST_1 = Destination(CITY_1, CITY_2)
    DEST_2 = Destination(CITY_1, CITY_3)
    DEST_3 = Destination(CITY_1, CITY_4)
    DEST_4 = Destination(CITY_1, CITY_5)
    DEST_5 = Destination(CITY_2, CITY_3)

    def test_order_destinations(self):
        destinations = RandomDestinationOptionsStrategy(1).order_destinations(
            {self.DEST_1, self.DEST_2, self.DEST_3, self.DEST_4, self.DEST_5})

        self.assertEqual(5, len(destinations))
        self.assertTrue(self.DEST_1, destinations)
        self.assertTrue(self.DEST_2, destinations)
        self.assertTrue(self.DEST_3, destinations)
        self.assertTrue(self.DEST_4, destinations)
        self.assertTrue(self.DEST_5, destinations)

