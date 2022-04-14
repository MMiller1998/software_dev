import unittest
import os
import sys
from unittest.mock import MagicMock
from Trains.Player.strategy import AStrategy
from Trains.Player.strategy import MORE_CARDS_REQUEST

# hack to get this test passing from our unit test script - not very robust or comprehensive, but it works for now
cwd = os.path.basename(os.getcwd())
if cwd == 'Trains':
    os.chdir('Other/tests/strategy/')

class StrategyTests(unittest.TestCase):
    def test_from_file_valid(self):
        strategy = AStrategy.from_file("files/dummy_strategy_valid.py")
        self.assertSetEqual(set(), strategy.select_destinations(MagicMock(), set()))
        self.assertEqual(MORE_CARDS_REQUEST, strategy.get_turn(MagicMock()))

    def test_from_file_invalid(self):
        with self.assertRaises(ValueError):
            AStrategy.from_file("files/dummy_strategy_invalid.py")
