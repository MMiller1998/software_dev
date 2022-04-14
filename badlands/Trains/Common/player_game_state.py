from typing import List, Set
from Trains.Common.map import Map
from Trains.Other.player_state import PrivatePlayerState, PublicPlayerState
from Trains.Other.undirected_connection import UndirectedConnection


class PlayerGameState:
    """
    Represents the knowledge a player has for a Trains game

    Args:
        map (Map): the map of the game
        own_state (PrivatePlayerState): the state of the player for which the game state is for
        other_player_states (List[PublicPlayerState]): the public state of the other players in the game

    Attributes:
        __map (Map): the map of the game
        own_state (PrivatePlayerState): the state of the player for which the game state is for
        other_player_states (List[PublicPlayerState]): the public state of the other players in the game
    """
    #todo: make ordering of other player_states explicit
    __map: Map
    own_state: PrivatePlayerState
    other_player_states: List[PublicPlayerState]

    def __init__(self, map: Map, own_state: PrivatePlayerState, other_player_states: List[PublicPlayerState]):
        """
        Constructs an instance of a PlayerGameState
        :param map: the map of the game
        :param own_state: the state of the player for which the game state is for
        :param other_player_states: the public state of the other players in the game
        """
        self.__map = map
        self.own_state = own_state
        self.other_player_states = other_player_states.copy()

    def get_acquirable_connections(self) -> Set[UndirectedConnection]:
        """
        Gets all acquirable connections.
        A connection is acquirable if:
         -- it is not already owned
         -- the player has:
          -- enough cards to acquire it
          -- enough rails to occupy it
        :return: all acquirable connections
        """
        unacquired_connections = self.__get_unacquired_connections()

        return self.__legally_acquirable_connections(unacquired_connections)

    def __get_unacquired_connections(self) -> Set[UndirectedConnection]:
        all_acquired_connections = self.__get_all_acquired_connections()
        possible_connections = self.__map.get_all_directed_connections()
        possible_undirected_connections = {con.make_undirected() for con in
                                           possible_connections}

        return possible_undirected_connections - all_acquired_connections

    def __legally_acquirable_connections(self, connections: Set[UndirectedConnection]) -> Set[UndirectedConnection]:
        return {connection for connection in connections if
                self.__has_sufficient_cards(connection) and self.__has_sufficient_rails(connection)}

    def __get_all_acquired_connections(self) -> Set[UndirectedConnection]:
        """
        Get all connections acquired by all the players in the game
        :return: a set of all acquired connections
        """
        other_player_acquired_connections = set().union(
            *[player_state.acquired_connections for player_state in self.other_player_states])

        return other_player_acquired_connections.union(self.own_state.public_state.acquired_connections)

    def __has_sufficient_cards(self, connection: UndirectedConnection) -> bool:
        return self.own_state.cards.get_card_count(connection.color) >= connection.length

    def __has_sufficient_rails(self, connection: UndirectedConnection) -> bool:
        return self.own_state.num_rails >= connection.length
