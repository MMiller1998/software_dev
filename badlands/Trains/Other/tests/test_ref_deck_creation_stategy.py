import unittest

from Trains.Other.color import Color
from Trains.Other.ref_deck_creation_strategy import RandomDeckCreationStrategy


class RandomDeckCreationStrategyTests(unittest.TestCase):
    def test_create_deck(self):
        random_deck = RandomDeckCreationStrategy(1).create_deck(20)
        self.assertEqual(20, len(random_deck))
        self.assertTrue(Color.RED in random_deck)
        self.assertTrue(Color.WHITE in random_deck)
        self.assertTrue(Color.BLUE in random_deck)
        self.assertTrue(Color.GREEN in random_deck)