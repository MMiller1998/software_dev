import unittest
from trains.utils import build_visual_map, safe_player_call, MethodStatus

from tests.examples.milestone3 import EMPTY, AIRPORTS


class TestUtils(unittest.TestCase):
    def test_parse_input_empty(self):
        train_map = build_visual_map(EMPTY)
        self.assertEqual(0, len(train_map.get_positions()))

    def test_parse_input(self):
        train_map = build_visual_map(AIRPORTS)
        self.assertEqual(train_map.width, 300)
        self.assertEqual(train_map.height, 700)
        posns = train_map.get_positions()
        self.assertEqual(posns['SAN'], (150, 100))
        self.assertEqual(posns['LAX'], (75, 200))
        self.assertEqual(posns['LAS'], (225, 250))
        self.assertEqual(posns['SFO, SJC'], (75, 300))
        self.assertEqual(posns['PDX'], (150, 400))
        self.assertEqual(posns['SEA'], (150, 500))
        self.assertEqual(6, len(posns))

    def test_safe_player_call_ok(self):
        self.assertEqual(safe_player_call(lambda: 2 + 2), (MethodStatus.OK, 4))

    def test_safe_player_call_error(self):
        self.assertEqual(safe_player_call(lambda: 1 / 0), MethodStatus.ERROR)


if __name__ == '__main__':
    unittest.main()
