import unittest
from collections import deque
from unittest.mock import patch, MagicMock
from Trains.Admin.referee_game_state import RefereeGameState
from Trains.Common.map import Map
from Trains.Other.cards import Cards
from Trains.Other.color import Color
from Trains.Other.directed_connection import DirectedConnection
from Trains.Other.undirected_connection import UndirectedConnection
from Trains.Other.city import City
from Trains.Other.city_pair import CityPair
from Trains.Other.player_state import PrivatePlayerState, PublicPlayerState


class RefereeGameStateTests(unittest.TestCase):
    CITY_NAME_1 = "city1"
    CITY_NAME_2 = "city2"
    CITY_NAME_3 = "city3"
    POSITION_1 = (350, 350)
    POSITION_2 = (400, 400)
    POSITION_3 = (400, 401)
    CITY_1 = City(CITY_NAME_1, POSITION_1)
    CITY_2 = City(CITY_NAME_2, POSITION_2)
    CITY_3 = City(CITY_NAME_3, POSITION_3)
    DIRECTED_CONNECTION_1A = DirectedConnection(CITY_1, CITY_2, 3, Color.RED)
    DIRECTED_CONNECTION_1B = DirectedConnection(CITY_2, CITY_1, 3, Color.RED)
    DIRECTED_CONNECTION_2A = DirectedConnection(CITY_1, CITY_2, 5, Color.BLUE)
    DIRECTED_CONNECTION_2B = DirectedConnection(CITY_2, CITY_1, 5, Color.BLUE)
    UNDIRECTED_CONNECTION_1 = DIRECTED_CONNECTION_1A.make_undirected()
    UNDIRECTED_CONNECTION_2 = DIRECTED_CONNECTION_2A.make_undirected()
    UNDIRECTED_CONNECTION_3 = UndirectedConnection(CITY_1, CITY_3, 4, Color.WHITE)
    CITY_PAIR_1 = CityPair(CITY_1, CITY_2)
    CITY_PAIR_2 = CityPair(CITY_2, CITY_3)

    MAP = Map(800, 800, [CITY_1, CITY_2],
              [DIRECTED_CONNECTION_1A, DIRECTED_CONNECTION_1B, DIRECTED_CONNECTION_2A, DIRECTED_CONNECTION_2B])

    CARDS = Cards({Color.RED: 3, Color.BLUE: 4, Color.WHITE: 0, Color.GREEN: 10})

    PRIVATE_PLAYER_STATE_1 = PrivatePlayerState(CARDS, {CITY_PAIR_1, CITY_PAIR_2}, 30, PublicPlayerState(set()))
    PRIVATE_PLAYER_STATE_2 = PrivatePlayerState(CARDS, {CITY_PAIR_1, CITY_PAIR_2}, 31, PublicPlayerState(set()))
    PRIVATE_PLAYER_STATE_3 = PrivatePlayerState(CARDS, {CITY_PAIR_1, CITY_PAIR_2}, 32, PublicPlayerState(set()))
    PRIVATE_PLAYER_STATE_LOW_RAILS = PrivatePlayerState(CARDS, {CITY_PAIR_1, CITY_PAIR_2}, 2, PublicPlayerState(set()))

    PLAYER_1 = MagicMock()
    PLAYER_2 = MagicMock()
    PLAYER_3 = MagicMock()
    ALL_PLAYERS = [PLAYER_1, PLAYER_2, PLAYER_3]

    EMPTY_CARD_DECK = []
    ONE_CARD_DECK = [Color.WHITE]
    RED_CARD_DECK = [Color.RED, Color.RED]
    GREEN_CARD_DECK = [Color.GREEN, Color.GREEN]

    STATE_PLAYER_DEQUE_1 = deque(zip([PRIVATE_PLAYER_STATE_1, PRIVATE_PLAYER_STATE_2],
                                     [PLAYER_1, PLAYER_2]))
    STATE_PLAYER_DEQUE_2 = deque(zip([PRIVATE_PLAYER_STATE_2, PRIVATE_PLAYER_STATE_3],
                                     [PLAYER_2, PLAYER_3]))
    STATE_PLAYER_DEQUE_ALL_PLAYERS = deque(zip([PRIVATE_PLAYER_STATE_1, PRIVATE_PLAYER_STATE_2, PRIVATE_PLAYER_STATE_3],
                                               [PLAYER_1, PLAYER_2, PLAYER_3]))

    def test_ref_game_state_valid_constructor(self):
        ref_game_state = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_1, self.EMPTY_CARD_DECK)
        self.assertListEqual([self.PRIVATE_PLAYER_STATE_1, self.PRIVATE_PLAYER_STATE_2],
                             ref_game_state._RefereeGameState__get_player_states())
        self.assertEqual([self.PLAYER_1, self.PLAYER_2], ref_game_state.get_players())

    def test_eq(self):
        ref_game_state_1 = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_1, self.RED_CARD_DECK)
        ref_game_state_2 = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_1, self.RED_CARD_DECK)
        self.assertTrue(ref_game_state_2 == ref_game_state_1)

    def test_not_eq(self):
        ref_game_state_1 = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_1, self.EMPTY_CARD_DECK)
        ref_game_state_2 = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_2, self.EMPTY_CARD_DECK)
        self.assertFalse(ref_game_state_2 == ref_game_state_1)

        ref_game_state_1 = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_1, self.RED_CARD_DECK)
        ref_game_state_2 = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_1, self.EMPTY_CARD_DECK)
        self.assertFalse(ref_game_state_2 == ref_game_state_1)

    def test_hash_eq(self):
        ref_game_state_1 = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_1, self.EMPTY_CARD_DECK)
        ref_game_state_2 = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_1, self.EMPTY_CARD_DECK)
        self.assertTrue(ref_game_state_2.__hash__() == ref_game_state_1.__hash__())

    def test_hash_not_eq(self):
        ref_game_state_1 = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_1, self.EMPTY_CARD_DECK)
        ref_game_state_2 = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_2, self.EMPTY_CARD_DECK)
        self.assertFalse(ref_game_state_2.__hash__() == ref_game_state_1.__hash__())

        ref_game_state_1 = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_1, self.GREEN_CARD_DECK)
        ref_game_state_2 = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_2, self.GREEN_CARD_DECK)
        self.assertFalse(ref_game_state_2.__hash__() == ref_game_state_1.__hash__())

    def test_ref_game_state_create_player_game_state(self):
        ref_game_state = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_ALL_PLAYERS, self.EMPTY_CARD_DECK)
        first_player_game_state = ref_game_state.create_player_game_state()
        self.assertEqual(self.PRIVATE_PLAYER_STATE_1, first_player_game_state.own_state)
        self.assertEqual(2, len(first_player_game_state.other_player_states))
        self.assertEqual(self.PRIVATE_PLAYER_STATE_2.public_state, first_player_game_state.other_player_states[0])
        self.assertEqual(self.PRIVATE_PLAYER_STATE_3.public_state, first_player_game_state.other_player_states[1])

        ref_game_state = RefereeGameState(self.MAP, deque(
            zip([self.PRIVATE_PLAYER_STATE_2, self.PRIVATE_PLAYER_STATE_1], [self.PLAYER_1, self.PLAYER_2])),
                                          self.EMPTY_CARD_DECK)
        second_player_game_state = ref_game_state.create_player_game_state()
        self.assertEqual(self.PRIVATE_PLAYER_STATE_2, second_player_game_state.own_state)
        self.assertEqual(1, len(second_player_game_state.other_player_states))
        self.assertEqual(self.PRIVATE_PLAYER_STATE_1.public_state, second_player_game_state.other_player_states[0])

    @patch('Trains.Admin.referee_game_state.PlayerGameState')
    def test_ref_game_state_can_acquire_connection_true(self, mock_player_game_state):
        player_game_state_instance = mock_player_game_state.return_value
        player_game_state_instance.get_acquirable_connections.return_value = {self.UNDIRECTED_CONNECTION_1}
        ref_game_state = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_1, self.EMPTY_CARD_DECK)
        self.assertTrue(ref_game_state.can_acquire_connection(self.UNDIRECTED_CONNECTION_1))

    @patch('Trains.Admin.referee_game_state.PlayerGameState')
    def test_ref_game_state_can_acquire_connection_false(self, mock_player_game_state):
        player_game_state_instance = mock_player_game_state.return_value
        player_game_state_instance.get_acquirable_connections.return_value = {self.UNDIRECTED_CONNECTION_2}
        ref_game_state = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_1, self.EMPTY_CARD_DECK)
        self.assertFalse(ref_game_state.can_acquire_connection(self.UNDIRECTED_CONNECTION_1))

    @patch('Trains.Admin.referee_game_state.PrivatePlayerState')
    def test_acquire_connection(self, mock_private_player_state):
        player_state_instance = mock_private_player_state.return_value
        player_state_instance.buy_connection.return_value = self.PRIVATE_PLAYER_STATE_3
        ref_game_state = RefereeGameState(self.MAP, deque(zip([player_state_instance, self.PRIVATE_PLAYER_STATE_2],
                                                              [self.PLAYER_1, self.PLAYER_2])),
                                          self.EMPTY_CARD_DECK)
        new_game_state = ref_game_state.acquire_connection(self.UNDIRECTED_CONNECTION_2)
        self.assertEqual(self.PRIVATE_PLAYER_STATE_3, new_game_state._RefereeGameState__get_player_states()[0])

    def test_reached_termination_condition_true(self):
        ref_game_state = RefereeGameState(self.MAP, deque(
            zip([self.PRIVATE_PLAYER_STATE_1, self.PRIVATE_PLAYER_STATE_LOW_RAILS], [self.PLAYER_1, self.PLAYER_2])),
                                          self.EMPTY_CARD_DECK)
        self.assertTrue(ref_game_state.reached_termination_condition())

    def test_reached_termination_condition_false(self):
        ref_game_state = RefereeGameState(self.MAP, deque(
            zip([self.PRIVATE_PLAYER_STATE_1, self.PRIVATE_PLAYER_STATE_2], [self.PLAYER_1, self.PLAYER_2])),
                                          self.EMPTY_CARD_DECK)
        self.assertFalse(ref_game_state.reached_termination_condition())

    def test_progress_turn(self):
        ref_game_state = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_ALL_PLAYERS, self.EMPTY_CARD_DECK)
        expected_ref_state = RefereeGameState(self.MAP,
                                              deque(zip([self.PRIVATE_PLAYER_STATE_2, self.PRIVATE_PLAYER_STATE_3,
                                                         self.PRIVATE_PLAYER_STATE_1],
                                                        [self.PLAYER_2, self.PLAYER_3, self.PLAYER_1])),
                                              self.EMPTY_CARD_DECK)
        self.assertEqual(expected_ref_state, ref_game_state.progress_turn())

    def test_remove_cheater(self):
        ref_game_state = RefereeGameState(self.MAP, self.STATE_PLAYER_DEQUE_ALL_PLAYERS, self.EMPTY_CARD_DECK)
        expected_ref_state = RefereeGameState(self.MAP,
                                              deque(zip([self.PRIVATE_PLAYER_STATE_2, self.PRIVATE_PLAYER_STATE_3],
                                                        [self.PLAYER_2, self.PLAYER_3])), self.EMPTY_CARD_DECK)
        self.assertEqual(expected_ref_state, ref_game_state.remove_cheater())

    def test_get_cards_to_draw(self):
        ref_game_state = RefereeGameState(self.MAP, deque(zip([MagicMock(), MagicMock()],
                                                              [self.PLAYER_1, self.PLAYER_2])), [Color.BLUE] * 3)
        actual_cards_to_draw = ref_game_state.get_cards_to_draw()
        self.assertListEqual([Color.BLUE] * 2, actual_cards_to_draw)

    def test_get_cards_to_draw_one_card(self):
        ref_game_state = RefereeGameState(self.MAP, deque(zip([MagicMock(), MagicMock()],
                                                              [self.PLAYER_1, self.PLAYER_2])), self.ONE_CARD_DECK)
        actual_cards_to_draw = ref_game_state.get_cards_to_draw()
        self.assertListEqual(self.ONE_CARD_DECK, actual_cards_to_draw)

    def test_get_cards_to_draw_no_cards(self):
        ref_game_state = RefereeGameState(self.MAP, deque(zip([MagicMock(), MagicMock()],
                                                              [self.PLAYER_1, self.PLAYER_2])), self.EMPTY_CARD_DECK)
        actual_cards_to_draw = ref_game_state.get_cards_to_draw()
        self.assertListEqual([], actual_cards_to_draw)

    @patch('Trains.Admin.referee_game_state.PrivatePlayerState')
    def test_draw_cards(self, mock_private_player_state):
        player_state_instance = mock_private_player_state.return_value
        player_state_instance.draw_cards.return_value = self.PRIVATE_PLAYER_STATE_3
        ref_game_state = RefereeGameState(self.MAP, deque(zip([player_state_instance, self.PRIVATE_PLAYER_STATE_2],
                                                              [self.PLAYER_1, self.PLAYER_2])), self.GREEN_CARD_DECK)
        cards_to_draw = ref_game_state.get_cards_to_draw()
        new_game_state = ref_game_state.draw_cards(cards_to_draw)
        self.assertListEqual(self.EMPTY_CARD_DECK, new_game_state._RefereeGameState__cards)
        self.assertEqual(self.PRIVATE_PLAYER_STATE_3, new_game_state._RefereeGameState__get_player_states()[0])

    @patch('Trains.Admin.referee_game_state.Map')
    def test_count_scores(self, mock_map):
        map_instance = mock_map.return_value
        map_instance.are_cities_connected.return_value = True
        map_instance.longest_continuous_route.return_value = 0
        ps_1 = PrivatePlayerState(self.CARDS, {self.CITY_PAIR_1, self.CITY_PAIR_2}, 30, PublicPlayerState(set()))
        ps_2 = PrivatePlayerState(self.CARDS, {self.CITY_PAIR_1, self.CITY_PAIR_2}, 30,
                                  PublicPlayerState({self.UNDIRECTED_CONNECTION_1}))
        ps_3 = PrivatePlayerState(self.CARDS, {self.CITY_PAIR_1, self.CITY_PAIR_2}, 30,
                                  PublicPlayerState({self.UNDIRECTED_CONNECTION_2, self.UNDIRECTED_CONNECTION_3}))

        ref_game_state = RefereeGameState(map_instance, deque(zip([ps_1, ps_2, ps_3], self.ALL_PLAYERS)),
                                          self.EMPTY_CARD_DECK)
        self.assertEqual([40, 43, 49], ref_game_state.count_scores())

    @patch('Trains.Admin.referee_game_state.Map')
    def test_count_scores_unconnected_destinations(self, mock_map):
        map_instance = mock_map.return_value
        map_instance.are_cities_connected.return_value = False
        map_instance.longest_continuous_route.return_value = 0
        ps_1 = PrivatePlayerState(self.CARDS, {self.CITY_PAIR_1, self.CITY_PAIR_2}, 30, PublicPlayerState(set()))
        ps_2 = PrivatePlayerState(self.CARDS, {self.CITY_PAIR_1, self.CITY_PAIR_2}, 30,
                                  PublicPlayerState({self.UNDIRECTED_CONNECTION_1}))
        ps_3 = PrivatePlayerState(self.CARDS, {self.CITY_PAIR_1, self.CITY_PAIR_2}, 30,
                                  PublicPlayerState({self.UNDIRECTED_CONNECTION_2, self.UNDIRECTED_CONNECTION_3}))

        ref_game_state = RefereeGameState(map_instance, deque(zip([ps_1, ps_2, ps_3], self.ALL_PLAYERS)),
                                          self.EMPTY_CARD_DECK)
        self.assertEqual([0, 3, 9], ref_game_state.count_scores())

    @patch('Trains.Admin.referee_game_state.Map')
    def test_count_scores_longest_continuous_path_non_tie(self, mock_map):
        def longest_continuous_route_side_effect(connections):
            return len(connections)

        map_instance = mock_map.return_value
        map_instance.are_cities_connected.return_value = True
        map_instance.longest_continuous_route.side_effect = longest_continuous_route_side_effect
        ps_1 = PrivatePlayerState(self.CARDS, {self.CITY_PAIR_1, self.CITY_PAIR_2}, 30, PublicPlayerState(set()))
        ps_2 = PrivatePlayerState(self.CARDS, {self.CITY_PAIR_1, self.CITY_PAIR_2}, 30,
                                  PublicPlayerState({self.UNDIRECTED_CONNECTION_1}))
        ps_3 = PrivatePlayerState(self.CARDS, {self.CITY_PAIR_1, self.CITY_PAIR_2}, 30,
                                  PublicPlayerState({self.UNDIRECTED_CONNECTION_2, self.UNDIRECTED_CONNECTION_3}))

        ref_game_state = RefereeGameState(map_instance, deque(zip([ps_1, ps_2, ps_3], self.ALL_PLAYERS)),
                                          self.EMPTY_CARD_DECK)
        self.assertEqual([20, 23, 49], ref_game_state.count_scores())
