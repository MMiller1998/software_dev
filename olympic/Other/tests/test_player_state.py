import unittest

from trains.graph_elements import RailColor
from trains.game.constants import (
    POINTS_PER_ACQUIRED_SEGMENT, POINTS_FOR_DISCONNECTED_DESTINATION,
    POINTS_FOR_CONNECTED_DESTINATION
)
from trains.state.player import PlayerState
from trains.state.cardsholder import create_hand, EMPTY_HAND

import tests.examples.milestone2 as example


class TestPlayerState(unittest.TestCase):

    def test_acquirable_connections_no_cards(self):
        player = PlayerState(
            destinations=frozenset(),
            occupied=None,
            cards=EMPTY_HAND,
            num_rails=40
        )
        self.assertEqual(0, len(list(player.acquirable_connections(example.all_connections))),
                         msg='Number of acquirable connections should be 0 because '
                             'the player does not have any colored cards.')

    def test_acquirable_connections_not_enough_rails(self):
        player = PlayerState(
            destinations=frozenset(),
            occupied=None,
            cards=create_hand(500),
            num_rails=2
        )
        self.assertEqual(len(list(player.acquirable_connections(example.all_connections))), 0,
                         msg='Number of acquirable connections should be 0 because'
                             'the player less <3 rails.')

    def test_can_acquire(self):
        player = PlayerState(
            destinations=frozenset(),
            occupied=None,
            cards=create_hand(3),
            num_rails=50
        )
        self.assertTrue(player.can_acquire(example.c_bwi_lax),
                        msg=f'Should be able to acquire {example.c_bwi_lax} after given 3 red cards')

    def test_acquirable_connections(self):
        pile = EMPTY_HAND.copy()
        pile[RailColor.BLUE] = 4
        player = PlayerState(
            destinations=frozenset(),
            occupied=None,
            cards=pile,
            num_rails=50
        )
        self.assertSetEqual(set(player.acquirable_connections(example.all_connections)),
                            {example.c_bwi_bos2})
        pile[RailColor.BLUE] = 5
        player = PlayerState(
            destinations=frozenset(),
            occupied=None,
            cards=pile,
            num_rails=50
        )
        self.assertSetEqual(set(player.acquirable_connections(example.all_connections)),
                            {example.c_bwi_bos2, example.c_mrtl_iad})

        pile[RailColor.RED] = 2
        player = PlayerState(
            destinations=frozenset(),
            occupied=None,
            cards=pile,
            num_rails=50
        )
        self.assertSetEqual(set(player.acquirable_connections(example.all_connections)),
                            {example.c_bwi_bos2, example.c_mrtl_iad})

        pile[RailColor.GREEN] = 4
        player = PlayerState(
            destinations=frozenset(),
            occupied=None,
            cards=pile,
            num_rails=50
        )
        self.assertSetEqual(set(player.acquirable_connections(example.all_connections)),
                            {example.c_bwi_bos2, example.c_mrtl_iad, example.c_bwi_bwi})

        player = PlayerState(
            destinations=frozenset(),
            occupied=None,
            cards=pile,
            num_rails=4
        )
        self.assertSetEqual(set(player.acquirable_connections(example.all_connections)),
                            {example.c_bwi_bos2, example.c_bwi_bwi})

        pile[RailColor.RED] = 3
        player = PlayerState(
            destinations=frozenset(),
            occupied=None,
            cards=pile,
            num_rails=4
        )
        self.assertSetEqual(set(player.acquirable_connections(example.all_connections)),
                            {example.c_bwi_bos2, example.c_bwi_bwi, example.c_bwi_lax})

        player = PlayerState(
            destinations=frozenset(),
            occupied=None,
            cards=pile,
            num_rails=3
        )
        self.assertSetEqual(set(player.acquirable_connections(example.all_connections)),
                            {example.c_bwi_lax})

    def test_points_for_acquired_segments(self):
        player_state = PlayerState(
            destinations=frozenset((
                frozenset((example.bos, example.bwi2)),
                frozenset((example.lax, example.bwi1))
            ))
        )
        self.assertEqual(player_state.points_for_acquired_segments(), 0)

        player_state = player_state.update(
            occupied=[example.c_bwi_lax, example.c_mrtl_iad, example.c_bwi_bos1]
        )
        self.assertEqual(
            player_state.points_for_acquired_segments(),
            POINTS_PER_ACQUIRED_SEGMENT * (example.c_bwi_lax.length + example.c_mrtl_iad.length + example.c_bwi_bos1.length)
        )

    def test_points_for_destinations(self):
        player_state = PlayerState(
            destinations=frozenset((
                frozenset((example.bos, example.bwi2)),
                frozenset((example.lax, example.bwi1))
            )),
            occupied=[example.c_bwi_lax]
        )
        self.assertEqual(player_state.points_for_destinations(), 2 * POINTS_FOR_DISCONNECTED_DESTINATION)

        player_state = PlayerState(
            destinations=frozenset((
                frozenset((example.bos, example.bwi2)),
                frozenset((example.lax, example.bwi1))
            )),
            occupied=[example.c_bwi_lax, example.c_bwi_bos2]
        )
        self.assertEqual(player_state.points_for_destinations(), POINTS_FOR_CONNECTED_DESTINATION + POINTS_FOR_DISCONNECTED_DESTINATION)

        player_state = PlayerState(
            destinations=frozenset((
                frozenset((example.bos, example.bwi2)),
                frozenset((example.lax, example.bwi1))
            )),
            occupied=[example.c_bwi_lax, example.c_bwi_bos2, example.c_bwi_bwi]
        )
        self.assertEqual(player_state.points_for_destinations(), 2 * POINTS_FOR_CONNECTED_DESTINATION)

    def test_places_are_connected(self):
        player_state = PlayerState(
            destinations=frozenset(),
            occupied=[example.c_bwi_bos1, example.c_bwi_lax]
        )

        self.assertTrue(player_state.places_are_connected(example.bos, example.bwi2))
        self.assertTrue(player_state.places_are_connected(example.bwi2, example.bos))
        self.assertTrue(player_state.places_are_connected(example.bos, example.lax))
        self.assertTrue(player_state.places_are_connected(example.lax, example.bos))

        self.assertFalse(player_state.places_are_connected(example.bwi2, example.bwi1))
        self.assertFalse(player_state.places_are_connected(example.bwi1, example.bwi2))
        self.assertFalse(player_state.places_are_connected(example.mrtl, example.iad))
        self.assertFalse(player_state.places_are_connected(example.iad, example.mrtl))

    def test_hash_same(self):
        ps1 = self.setup_player_state()
        ps2 = self.setup_player_state()

        self.assertEqual(hash(ps1), hash(ps2))

    def test_hash_different(self):
        ps1 = self.setup_player_state()
        ps2 = ps1.update(destinations=frozenset((example.dest_lax_bos, example.dest_bwi1_lax)))
        self.assertNotEqual(hash(ps1), hash(ps2))

        ps2 = ps1.update(occupied=[example.c_bwi_bos1, example.c_mrtl_iad, example.c_bwi_lax])
        self.assertNotEqual(hash(ps1), hash(ps2))

        ps2 = ps1.update(num_rails=26)
        self.assertNotEqual(hash(ps1), hash(ps2))

    def test_eq_same(self):
        ps1 = self.setup_player_state()
        ps2 = self.setup_player_state()

        self.assertEqual(ps1, ps2)

    def test_eq_different(self):
        ps1 = self.setup_player_state()
        ps2 = ps1.update(destinations=frozenset((example.dest_lax_bos, example.dest_bwi1_lax)))
        self.assertNotEqual(ps1, ps2)

        ps2 = ps1.update(occupied=[example.c_bwi_bos1, example.c_mrtl_iad, example.c_bwi_lax])
        self.assertNotEqual(ps1, ps2)

        ps2 = ps1.update(num_rails=26)
        self.assertNotEqual(ps1, ps2)

    @staticmethod
    def setup_player_state() -> PlayerState:
        return PlayerState(
            destinations=frozenset((example.dest_lax_bos, example.dest_bwi1_bwi2)),
            occupied=[example.c_bwi_bos1, example.c_mrtl_iad],
            num_rails=27,
            cards=create_hand(3)
        )
