import unittest
from Trains.Other.player_state import PublicPlayerState, PrivatePlayerState
from Trains.Other.undirected_connection import UndirectedConnection
from Trains.Other.city import City
from Trains.Other.color import Color
from Trains.Other.cards import Cards
from Trains.Other.destination import Destination


class PrivatePlayerStateTests(unittest.TestCase):
    CITY_NAME_1 = "city1"
    CITY_NAME_2 = "city2"
    CITY_NAME_3 = "city3"
    POSITION_1 = (350, 350)
    POSITION_2 = (400, 400)
    POSITION_3 = (10, 750)
    CITY_1 = City(CITY_NAME_1, POSITION_1)
    CITY_2 = City(CITY_NAME_2, POSITION_2)
    CITY_3 = City(CITY_NAME_3, POSITION_3)

    DESTINATION_1 = Destination(CITY_1, CITY_2)
    DESTINATION_2 = Destination(CITY_2, CITY_3)
    DESTINATION_3 = Destination(CITY_1, CITY_3)
    DESTINATION_SET = {DESTINATION_1, DESTINATION_2}

    UNDIRECTED_CONNECTION_1 = UndirectedConnection(CITY_1, CITY_2, 3, Color.GREEN)
    UNDIRECTED_CONNECTION_2 = UndirectedConnection(CITY_2, CITY_3, 3, Color.GREEN)
    UNDIRECTED_CONNECTION_3 = UndirectedConnection(CITY_1, CITY_3, 3, Color.GREEN)

    CONNECTION_SET_1 = {UNDIRECTED_CONNECTION_1, UNDIRECTED_CONNECTION_2}
    CONNECTION_SET_2 = {UNDIRECTED_CONNECTION_3}

    PUBLIC_PLAYER_STATE_1 = PublicPlayerState(CONNECTION_SET_1)
    NUM_GREEN_CARDS = 10
    NUM_RED_CARDS = 11
    NUM_BLUE_CARDS = 12
    NUM_WHITE_CARDS = 13
    CARDS_1 = Cards({
        Color.GREEN: NUM_GREEN_CARDS,
        Color.RED: NUM_RED_CARDS,
        Color.BLUE: NUM_BLUE_CARDS,
        Color.WHITE: NUM_WHITE_CARDS,
    })
    NUM_RAILS = 45

    def test_constructor_valid(self):
        actual_private_state = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, self.NUM_RAILS,
                                                  self.PUBLIC_PLAYER_STATE_1)

        self.assertEqual(self.NUM_GREEN_CARDS, actual_private_state.cards.get_card_count(Color.GREEN))
        self.assertEqual(self.NUM_RED_CARDS, actual_private_state.cards.get_card_count(Color.RED))
        self.assertEqual(self.NUM_BLUE_CARDS, actual_private_state.cards.get_card_count(Color.BLUE))
        self.assertEqual(self.NUM_WHITE_CARDS, actual_private_state.cards.get_card_count(Color.WHITE))
        self.assertSetEqual(self.DESTINATION_SET, actual_private_state.destinations)
        self.assertEqual(self.NUM_RAILS, actual_private_state.num_rails)
        self.assertSetEqual(self.PUBLIC_PLAYER_STATE_1.acquired_connections,
                            actual_private_state.public_state.acquired_connections)

    def test_constructor_invalid_negative_rails(self):
        with self.assertRaises(ValueError):
            PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, -3,
                               self.PUBLIC_PLAYER_STATE_1)

    def test_constructor_invalid_no_destinations(self):
        with self.assertRaises(ValueError):
            PrivatePlayerState(self.CARDS_1, set(), self.NUM_RAILS,
                               self.PUBLIC_PLAYER_STATE_1)

    def test_constructor_invalid_too_many_destinations(self):
        with self.assertRaises(ValueError):
            PrivatePlayerState(self.CARDS_1,
                               {self.DESTINATION_1, self.DESTINATION_2, Destination(self.CITY_1, self.CITY_3)},
                               self.NUM_RAILS,
                               self.PUBLIC_PLAYER_STATE_1)

    def test_eq(self):
        private_state_1 = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, self.NUM_RAILS,
                                                  self.PUBLIC_PLAYER_STATE_1)
        private_state_2 = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, self.NUM_RAILS,
                                             self.PUBLIC_PLAYER_STATE_1)

        self.assertTrue(private_state_1 == private_state_2)

    def test_not_eq_cards(self):
        private_state_1 = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, self.NUM_RAILS,
                                             self.PUBLIC_PLAYER_STATE_1)
        private_state_2 = PrivatePlayerState(Cards({Color.RED: 2}), self.DESTINATION_SET, self.NUM_RAILS,
                                             self.PUBLIC_PLAYER_STATE_1)

        self.assertFalse(private_state_1 == private_state_2)

    def test_not_eq_destinations(self):
        private_state_1 = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, self.NUM_RAILS,
                                             self.PUBLIC_PLAYER_STATE_1)
        private_state_2 = PrivatePlayerState(self.CARDS_1, {self.DESTINATION_1, self.DESTINATION_3}, self.NUM_RAILS,
                                             self.PUBLIC_PLAYER_STATE_1)

        self.assertFalse(private_state_1 == private_state_2)

    def test_not_eq_num_rails(self):
        private_state_1 = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, self.NUM_RAILS,
                                             self.PUBLIC_PLAYER_STATE_1)
        private_state_2 = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, 10,
                                             self.PUBLIC_PLAYER_STATE_1)

        self.assertFalse(private_state_1 == private_state_2)

    def test_not_eq_public_state(self):
        private_state_1 = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, self.NUM_RAILS,
                                             self.PUBLIC_PLAYER_STATE_1)
        private_state_2 = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, 10,
                                             PublicPlayerState(self.CONNECTION_SET_2))

        self.assertFalse(private_state_1 == private_state_2)

    def test_hash_eq(self):
        private_state_1 = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, self.NUM_RAILS,
                                             self.PUBLIC_PLAYER_STATE_1)
        private_state_2 = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, self.NUM_RAILS,
                                             self.PUBLIC_PLAYER_STATE_1)

        self.assertTrue(private_state_1.__hash__() == private_state_2.__hash__())

    def test_hash_not_eq_cards(self):
        private_state_1 = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, self.NUM_RAILS,
                                             self.PUBLIC_PLAYER_STATE_1)
        private_state_2 = PrivatePlayerState(Cards({Color.RED: 2}), self.DESTINATION_SET, self.NUM_RAILS,
                                             self.PUBLIC_PLAYER_STATE_1)

        self.assertFalse(private_state_1.__hash__() == private_state_2.__hash__())

    def test_hash_not_eq_destinations(self):
        private_state_1 = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, self.NUM_RAILS,
                                             self.PUBLIC_PLAYER_STATE_1)
        private_state_2 = PrivatePlayerState(self.CARDS_1, {self.DESTINATION_1, self.DESTINATION_3}, self.NUM_RAILS,
                                             self.PUBLIC_PLAYER_STATE_1)

        self.assertFalse(private_state_1.__hash__() == private_state_2.__hash__())

    def test_hash_not_eq_num_rails(self):
        private_state_1 = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, self.NUM_RAILS,
                                             self.PUBLIC_PLAYER_STATE_1)
        private_state_2 = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, 10,
                                             self.PUBLIC_PLAYER_STATE_1)

        self.assertFalse(private_state_1.__hash__() == private_state_2.__hash__())

    def test_hash_not_eq_public_state(self):
        private_state_1 = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, self.NUM_RAILS,
                                             self.PUBLIC_PLAYER_STATE_1)
        private_state_2 = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, 10,
                                             PublicPlayerState(self.CONNECTION_SET_2))

        self.assertFalse(private_state_1.__hash__() == private_state_2.__hash__())

    def test_draw_cards(self):
        private_state = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, self.NUM_RAILS,
                                             self.PUBLIC_PLAYER_STATE_1)
        actual_private_state = private_state.draw_cards(Cards({Color.RED: 2, Color.WHITE: 1}))
        self.assertEqual(self.NUM_GREEN_CARDS, actual_private_state.cards.get_card_count(Color.GREEN))
        self.assertEqual(self.NUM_RED_CARDS + 2, actual_private_state.cards.get_card_count(Color.RED))
        self.assertEqual(self.NUM_BLUE_CARDS, actual_private_state.cards.get_card_count(Color.BLUE))
        self.assertEqual(self.NUM_WHITE_CARDS + 1, actual_private_state.cards.get_card_count(Color.WHITE))
        self.assertSetEqual(self.DESTINATION_SET, actual_private_state.destinations)
        self.assertEqual(self.NUM_RAILS, actual_private_state.num_rails)
        self.assertSetEqual(self.PUBLIC_PLAYER_STATE_1.acquired_connections,
                            actual_private_state.public_state.acquired_connections)

    def test_buy_connection(self):
        private_state = PrivatePlayerState(self.CARDS_1, self.DESTINATION_SET, self.NUM_RAILS,
                                           self.PUBLIC_PLAYER_STATE_1)
        actual_private_state = private_state.buy_connection(self.UNDIRECTED_CONNECTION_3)
        self.assertEqual(self.NUM_GREEN_CARDS - 3, actual_private_state.cards.get_card_count(Color.GREEN))
        self.assertEqual(self.NUM_RED_CARDS, actual_private_state.cards.get_card_count(Color.RED))
        self.assertEqual(self.NUM_BLUE_CARDS, actual_private_state.cards.get_card_count(Color.BLUE))
        self.assertEqual(self.NUM_WHITE_CARDS, actual_private_state.cards.get_card_count(Color.WHITE))
        self.assertSetEqual(self.DESTINATION_SET, actual_private_state.destinations)
        self.assertEqual(self.NUM_RAILS - 3, actual_private_state.num_rails)
        self.assertSetEqual(self.PUBLIC_PLAYER_STATE_1.acquired_connections.union({self.UNDIRECTED_CONNECTION_3}),
                            actual_private_state.public_state.acquired_connections)
