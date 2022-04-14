import unittest

from trains.map import TrainMap
from trains.graph_elements import RailColor
from trains.json.serializers import (
    serialize_place, serialize_connections, serialize_train_map,
    serialize_destination, serialize_rail_color, serialize_card_deck,
    serialize_card_hand, serialize_other_player_acquireds, serialize_action,
    serialize_connection_to_acquired, serialize_connections_to_player,
    serialize_acquire, serialize_destinations, serialize_rank,
    serialize_tournament_result, serialize_player_state_wrapper, serialize_player_state
)
from trains.state.player import PlayerState, PlayerStateWrapper
from trains.state.action import WantCards, Acquire
from trains.state.cardsholder import create_hand
from trains.game.player import PlayerActor

from tests.examples import bigger_map

MAP_WIDTH = 500
MAP_HEIGHT = 600


class TestSerializers(unittest.TestCase):

    def setUp(self):
        self.train_map = TrainMap(MAP_WIDTH, MAP_HEIGHT)
        self.bos = self.train_map.add_place('BOS', 125, 125)
        self.lax = self.train_map.add_place('LAX', 10, 20)
        self.bwi = self.train_map.add_place('BWI', 68, 419)
        self.mrtl = self.train_map.add_place('MRTL', 110, 220)
        self.iad = self.train_map.add_place('IAD', 499, 12)
        self.rsw = self.train_map.add_place('RSW', 1, 1)

        self.c_bwi_lax = self.train_map.add_connection(
            self.bwi, self.lax, color=RailColor.RED, length=3)
        self.c_bwi_bos1 = self.train_map.add_connection(
            self.bwi, self.bos, color=RailColor.GREEN, length=5)
        self.c_bwi_bos2 = self.train_map.add_connection(
            self.bwi, self.bos, color=RailColor.BLUE, length=4)
        self.c_mrtl_iad = self.train_map.add_connection(
            self.mrtl, self.iad, color=RailColor.BLUE, length=5)

        self.all_cities = [self.bos, self.lax, self.bwi, self.mrtl, self.iad, self.rsw]

    def test_serialize_place(self):
        self.assertTupleEqual(serialize_place(self.bos), ("BOS", (125, 125)))
        self.assertTupleEqual(serialize_place(self.lax), ("LAX", (10, 20)))

    def test_serialize_connections(self):
        connections = self.train_map.get_all_connections()

        self.assertDictEqual(serialize_connections(connections), {
            "BOS": {
                "BWI": {
                    "green": 5,
                    "blue": 4
                }
            },
            "BWI": {
                "LAX": {
                    "red": 3
                }
            },
            "IAD": {
                "MRTL": {
                    "blue": 5
                }
            }
        })

    def test_serialize_connection_to_acquired(self):
        self.assertTupleEqual(serialize_connection_to_acquired(self.c_bwi_lax), ("BWI", "LAX", "red", 3))
        self.assertTupleEqual(serialize_connection_to_acquired(self.c_bwi_bos1), ("BOS", "BWI", "green", 5))

    def test_serialize_connections_to_player(self):
        self.assertListEqual(
            serialize_connections_to_player([self.c_bwi_lax, self.c_mrtl_iad]),
            [("BWI", "LAX", "red", 3), ("IAD", "MRTL", "blue", 5)]
        )

    def test_serialize_other_player_acquireds(self):
        connection_list_1 = [self.c_bwi_lax, self.c_bwi_bos1]
        connection_list_2 = [self.c_mrtl_iad, self.c_bwi_bos2]
        other_player_acquireds = [connection_list_1, connection_list_2]

        self.assertListEqual(serialize_other_player_acquireds(other_player_acquireds), [
            [serialize_connection_to_acquired(connection) for connection in connection_list_1],
            [serialize_connection_to_acquired(connection) for connection in connection_list_2]
        ])

    def test_serialize_train_map(self):
        self.assertDictEqual(serialize_train_map(self.train_map), {
            "width": MAP_WIDTH,
            "height": MAP_HEIGHT,
            "cities": [serialize_place(place) for place in self.train_map.get_all_places()],
            "connections": serialize_connections(self.train_map.get_all_connections())
        })

    def test_serialize_rail_color(self):
        self.assertEqual(serialize_rail_color(RailColor.BLUE), "blue")
        self.assertEqual(serialize_rail_color(RailColor.RED), "red")
        self.assertEqual(serialize_rail_color(RailColor.GREEN), "green")
        self.assertEqual(serialize_rail_color(RailColor.WHITE), "white")

    def test_serialize_card_deck(self):
        self.assertEqual(
            serialize_card_deck([RailColor.WHITE, RailColor.WHITE, RailColor.RED]),
            ["white", "white", "red"]
        )

    def test_serialize_card_hand(self):
        self.assertDictEqual(
            serialize_card_hand({RailColor.WHITE: 3, RailColor.RED: 6, RailColor.GREEN: 0, RailColor.BLUE: 1}),
            {"white": 3, "red": 6, "green": 0, "blue": 1}
        )

    def test_serialize_more_cards_action(self):
        more_cards = WantCards()
        self.assertEqual(serialize_action(more_cards), "more cards")

    def test_serialize_acquire_action(self):
        acquire = Acquire(self.c_bwi_lax)
        self.assertEqual(serialize_action(acquire), ("BWI", "LAX", "red", 3))

    def test_serialize_acquire(self):
        acquire = Acquire(self.c_bwi_lax)
        self.assertEqual(serialize_acquire(acquire), ("BWI", "LAX", "red", 3))

    def test_serialize_destination(self):
        self.assertTupleEqual(serialize_destination(bigger_map.dest_1_2), ('1', '2'))
        self.assertTupleEqual(serialize_destination(bigger_map.dest_3_10), ('10', '3'))

    def test_serialize_destinations(self):
        self.assertListEqual(
            serialize_destinations([bigger_map.dest_1_9, bigger_map.dest_3_4]),
            [('1', '9'), ('3', '4')]
        )

    def test_serialize_rank(self):
        p1 = PlayerActor('some strategy', name='randall')
        p2 = PlayerActor('some other strategy', name='fox mccloud')
        p3 = PlayerActor('last strategy', name='falco lombardi')
        self.assertListEqual(serialize_rank({p1, p2, p3}), ['falco lombardi', 'fox mccloud', 'randall'])

    def test_serialize_tournament_result(self):
        p1 = PlayerActor('some strategy', name='randall')
        p2 = PlayerActor('some other strategy', name='fox mccloud')
        p3 = PlayerActor('last strategy', name='falco lombardi')
        p4 = PlayerActor('some strategy', name='marth')
        p5 = PlayerActor('some other strategy', name='jigglypuff')
        self.assertTupleEqual(
            serialize_tournament_result(({p1, p2, p3}, {p4, p5})),
            (['falco lombardi', 'fox mccloud', 'randall'], ['jigglypuff', 'marth'])
        )

    def test_serialize_player_state(self):
        ps = PlayerState(
            {frozenset([self.bos, self.bwi]), frozenset([self.mrtl, self.iad])},
            occupied={self.c_bwi_lax},
            cards=create_hand(3),
            num_rails=42
        )

        self.assertDictEqual(serialize_player_state(ps), {
            "destination1": ("BOS", "BWI"),
            "destination2": ("IAD", "MRTL"),
            "rails": 42,
            "cards": {
                "red": 3,
                "blue": 3,
                "green": 3,
                "white": 3
            },
            "acquired": [("BWI", "LAX", "red", 3)]
        })

    def test_serialize_player_state_wrapper(self):
        ps = PlayerState(
            {frozenset([self.bos, self.bwi]), frozenset([self.mrtl, self.iad])},
            occupied={self.c_bwi_lax},
            cards=create_hand(3),
            num_rails=42
        )
        other_player_acquireds = [[self.c_bwi_bos1], [self.c_mrtl_iad, self.c_bwi_bos2], []]
        psw = PlayerStateWrapper(ps, other_player_acquireds)

        self.assertDictEqual(serialize_player_state_wrapper(psw), {
            "this": {
                "destination1": ("BOS", "BWI"),
                "destination2": ("IAD", "MRTL"),
                "rails": 42,
                "cards": {
                    "red": 3,
                    "blue": 3,
                    "green": 3,
                    "white": 3
                },
                "acquired": [("BWI", "LAX", "red", 3)]
            },
            "acquired": [
                [("BOS", "BWI", "green", 5)],
                [("IAD", "MRTL", "blue", 5), ("BOS", "BWI", "blue", 4)],
                []
            ]
        })
