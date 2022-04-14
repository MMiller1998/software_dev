from unittest import TestCase

from trains.graph_traversals import get_longest_path_from_place_length

import tests.examples.milestone2 as example


class TestGraphTraversals(TestCase):

    def test_get_longest_path_from_place_length(self):
        self.assertEqual(get_longest_path_from_place_length(example.bwi1, example.train_map.get_all_connections()), 9)
        self.assertEqual(get_longest_path_from_place_length(example.lax, example.train_map.get_all_connections()), 8)
        self.assertEqual(get_longest_path_from_place_length(example.rsw, example.train_map.get_all_connections()), 0)
