import unittest
from Trains.Common.map import Map
from Trains.Common.player_game_state import PlayerGameState
from Trains.Other.color import Color
from Trains.Other.directed_connection import DirectedConnection
from Trains.Other.undirected_connection import UndirectedConnection
from Trains.Other.city import City
from Trains.Other.player_state import PrivatePlayerState, PublicPlayerState
from Trains.Other.cards import Cards
from Trains.Other.destination import Destination


class PlayerGameStateTests(unittest.TestCase):
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
    DESTINATION_SET = {DESTINATION_1, DESTINATION_2}

    DIRECTED_CONNECTION_1A = DirectedConnection(CITY_1, CITY_2, 3, Color.RED)
    DIRECTED_CONNECTION_1B = DirectedConnection(CITY_2, CITY_1, 3, Color.RED)
    DIRECTED_CONNECTION_2A = DirectedConnection(CITY_1, CITY_2, 5, Color.BLUE)
    DIRECTED_CONNECTION_2B = DirectedConnection(CITY_2, CITY_1, 5, Color.BLUE)
    DIRECTED_CONNECTION_3A = DirectedConnection(CITY_1, CITY_2, 4, Color.WHITE)
    DIRECTED_CONNECTION_3B = DirectedConnection(CITY_2, CITY_1, 4, Color.WHITE)
    DIRECTED_CONNECTION_4A = DirectedConnection(CITY_1, CITY_2, 4, Color.GREEN)
    DIRECTED_CONNECTION_4B = DirectedConnection(CITY_2, CITY_1, 4, Color.GREEN)
    DIRECTED_CONNECTION_5A = DirectedConnection(CITY_1, CITY_3, 5, Color.WHITE)
    DIRECTED_CONNECTION_5B = DirectedConnection(CITY_3, CITY_1, 5, Color.WHITE)
    DIRECTED_CONNECTION_6A = DirectedConnection(CITY_1, CITY_3, 4, Color.GREEN)
    DIRECTED_CONNECTION_6B = DirectedConnection(CITY_3, CITY_1, 4, Color.GREEN)

    UNDIRECTED_CONNECTION_1 = DIRECTED_CONNECTION_1A.make_undirected()
    UNDIRECTED_CONNECTION_2 = DIRECTED_CONNECTION_2A.make_undirected()
    UNDIRECTED_CONNECTION_3 = DIRECTED_CONNECTION_3A.make_undirected()
    UNDIRECTED_CONNECTION_4 = DIRECTED_CONNECTION_4A.make_undirected()
    UNDIRECTED_CONNECTION_5 = DIRECTED_CONNECTION_5A.make_undirected()
    UNDIRECTED_CONNECTION_6 = DIRECTED_CONNECTION_6A.make_undirected()

    TRAINS_MAP = Map(800, 800, [CITY_1, CITY_2, CITY_3],
                     [DIRECTED_CONNECTION_1A, DIRECTED_CONNECTION_1B,
                      DIRECTED_CONNECTION_2A, DIRECTED_CONNECTION_2B,
                      DIRECTED_CONNECTION_3A, DIRECTED_CONNECTION_3B,
                      DIRECTED_CONNECTION_4A, DIRECTED_CONNECTION_4B,
                      DIRECTED_CONNECTION_5A, DIRECTED_CONNECTION_5B,
                      DIRECTED_CONNECTION_6A, DIRECTED_CONNECTION_6B])

    PUBLIC_STATE_1 = PublicPlayerState({UNDIRECTED_CONNECTION_1})
    PUBLIC_STATE_2 = PublicPlayerState(set())
    PUBLIC_STATE_3 = PublicPlayerState({UNDIRECTED_CONNECTION_2, UNDIRECTED_CONNECTION_3, UNDIRECTED_CONNECTION_4})

    NUM_GREEN_CARDS = 10
    NUM_RED_CARDS = 11
    NUM_BLUE_CARDS = 12
    NUM_WHITE_CARDS = 4
    CARDS_1 = Cards({
        Color.GREEN: NUM_GREEN_CARDS,
        Color.RED: NUM_RED_CARDS,
        Color.BLUE: NUM_BLUE_CARDS,
        Color.WHITE: NUM_WHITE_CARDS,
    })
    NUM_RAILS = 45
    NUM_RAILS_NOT_ENOUGH = 1

    PRIVATE_STATE_1 = PrivatePlayerState(CARDS_1, DESTINATION_SET, NUM_RAILS, PUBLIC_STATE_1)
    PRIVATE_STATE_NOT_ENOUGH_RAILS = PrivatePlayerState(CARDS_1, DESTINATION_SET, NUM_RAILS_NOT_ENOUGH, PUBLIC_STATE_1)

    def test_player_game_state_constructor(self):
        actual_player_state = PlayerGameState(self.TRAINS_MAP, self.PRIVATE_STATE_1,
                                              [self.PUBLIC_STATE_2, self.PUBLIC_STATE_3])

        self.assertEqual(self.PRIVATE_STATE_1, actual_player_state.own_state)
        self.assertListEqual([self.PUBLIC_STATE_2, self.PUBLIC_STATE_3], actual_player_state.other_player_states)

    def test_get_acquirable_connections(self):
        actual_player_state = PlayerGameState(self.TRAINS_MAP, self.PRIVATE_STATE_1,
                                              [self.PUBLIC_STATE_2, self.PUBLIC_STATE_3])

        self.assertSetEqual({self.UNDIRECTED_CONNECTION_6},
                            actual_player_state.get_acquirable_connections())

    def test_get_acquirable_connections_not_enough_rails(self):
        actual_player_state = PlayerGameState(self.TRAINS_MAP, self.PRIVATE_STATE_NOT_ENOUGH_RAILS,
                                              [self.PUBLIC_STATE_2, self.PUBLIC_STATE_3])

        self.assertSetEqual(set(), actual_player_state.get_acquirable_connections())
