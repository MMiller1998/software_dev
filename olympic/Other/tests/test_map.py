from unittest import TestCase
from typing import Iterable, Set, Any

from trains.map import TrainMap, TrainPlace, TrainPlaceId, TrainConnectionId, RailColor
from trains.errors import TrainConnectionLengthException, \
    TrainConnectionToSelfException, DuplicateTrainConnectionException

import tests.examples.milestone2 as example


class TestTrainMap(TestCase):
    def test_add_bad_connection_length(self):
        with self.assertRaises(TrainConnectionLengthException):
            example.train_map.add_connection(
                example.bos, example.lax, color=RailColor.GREEN, length=-1)
        with self.assertRaises(TrainConnectionLengthException):
            example.train_map.add_connection(
                example.bos, example.lax, color=RailColor.GREEN, length=6)

    def test_add_connection_to_self(self):
        with self.assertRaises(TrainConnectionToSelfException):
            example.train_map.add_connection(
                example.rsw, example.rsw, color=RailColor.GREEN, length=3)

    def test_connection_dne(self):
        pek = TrainPlace('PEK', 1, 2, -99)
        with self.assertRaises(ValueError,
                               msg='Constructor should not accept connections which '
                                   'are to/from a place not from this map instance.'):
            example.train_map.add_connection(
                example.bos, pek, color=RailColor.RED, length=5)

    def test_connection_same_color(self):
        with self.assertRaises(DuplicateTrainConnectionException):
            example.train_map.add_connection(
                example.lax, example.bwi2, color=RailColor.RED, length=3)
        with self.assertRaises(DuplicateTrainConnectionException):
            example.train_map.add_connection(
                example.lax, example.bwi2, color=RailColor.RED, length=4)

    def test_empty_map(self):
        empty_map = TrainMap(100, 100)
        destination = empty_map.get_destinations()
        sentinel = None
        self.assertEqual(next(destination, sentinel), sentinel,
                         msg='Empty map should not have destinations.')

    def test_get_neighbors(self):
        self.assertFalse(list(example.rsw.get_neighbors()),
                         msg='RSW should not have any neighbors.')
        self.assertSetEqual(
            example.bwi2.get_neighbors(),
            {example.bwi1, example.lax, example.bos}
        )

    def test_find_connected_graph(self):
        graph = example.train_map._find_connected_graph(example.rsw)
        self.assertListEqual(list(graph), [example.rsw])
        self.assertUnorderedEqual(
            example.train_map._find_connected_graph(example.bos),
            {example.bos, example.bwi1, example.bwi2, example.lax}
        )

    def test_cartesian_product(self):
        graph = [example.rsw]
        self.assertFalse(
            list(TrainMap._cartesian_product(graph)),
            msg='The destinations for a graph of just RSW should be '
                'an empty list.'
        )

        graph = [example.bos, example.bwi1, example.bwi2, example.lax]
        expected = [
            (example.bos, example.bwi1),
            (example.bos, example.bwi2),
            (example.bos, example.lax),
            (example.bwi1, example.bwi2),
            (example.bwi1, example.lax),
            (example.bwi2, example.lax)
        ]
        self.assertUnorderedEqual(
            TrainMap._cartesian_product(graph),
            set(frozenset(pair) for pair in expected)
        )

    def test_get_destinations(self):
        result = list(example.train_map.get_destinations())
        expected = (
            {example.bwi1, example.bwi2},
            {example.bwi1, example.lax},
            {example.bwi1, example.bos},
            {example.bwi2, example.lax},
            {example.bwi2, example.bos},
            {example.mrtl, example.iad},
            {example.bos, example.lax}
        )
        for e in expected:
            self.assertIn(e, result)
        self.assertEqual(len(result), len(expected))

    def test_get_place(self):
        m = 'Trying to find a previously added place by its id returns '
        m += 'a different place. id is inconsistent i.e. being changed.'
        self.assertEqual(example.train_map.get_place(example.bos.id), example.bos, msg=m)
        self.assertEqual(example.train_map.get_place(example.lax.id), example.lax, msg=m)

        with self.assertRaises(ValueError):
            example.train_map.get_place(TrainPlaceId(-9))
        with self.assertRaises(ValueError):
            example.train_map.get_place(TrainPlaceId(999))

    def test_get_connection(self):
        m = 'Trying to find a previously added connection by its id returns '
        m += 'a different connection. id is inconsistent i.e. being changed.'
        self.assertSetEqual(example.train_map.get_connection(example.c_bwi_bwi.id).get_places(),
                            {example.bwi1, example.bwi2})
        self.assertSetEqual(example.train_map.get_connection(example.c_mrtl_iad.id).get_places(),
                            {example.mrtl, example.iad})

        with self.assertRaises(ValueError):
            example.train_map.get_connection(TrainConnectionId(-9))
        with self.assertRaises(ValueError):
            example.train_map.get_connection(TrainConnectionId(999))

    def test_get_all_connections(self):
        self.assertUnorderedEqual(
            example.train_map.get_all_connections(),
            {
                example.c_bwi_bos1,
                example.c_bwi_bos2,
                example.c_bwi_bwi,
                example.c_bwi_lax,
                example.c_mrtl_iad
            }
        )

    def test_get_other(self):
        self.assertEqual(example.c_mrtl_iad.get_other(example.mrtl), example.iad)
        self.assertEqual(example.c_mrtl_iad.get_other(example.iad), example.mrtl)
        with self.assertRaises(ValueError):
            example.c_mrtl_iad.get_other(example.bos)

    def test_get_connections_from_place(self):
        self.assertSetEqual(example.bwi1.get_connections(), {example.c_bwi_bwi})
        self.assertSetEqual(
            example.bwi2.get_connections(),
            {example.c_bwi_bwi, example.c_bwi_bos1, example.c_bwi_bos2, example.c_bwi_lax}
        )

    def assertUnorderedEqual(self, actual: Iterable[Any], expected: Set[Any], msg=None):
        """
        Asserts that the unordered collection does not contain duplicates and that
        it is equal to a given set.

        :param actual: unordered collection to check
        :param expected: set of members that actual should have
        :param msg: optional error message
        """
        actual_list = list(actual)
        actual_set = set(actual_list)
        self.assertEqual(len(actual_list), len(actual_set),
                         msg=f'Contains duplicates: {actual_list}')
        self.assertSetEqual(actual_set, expected, msg=msg)
