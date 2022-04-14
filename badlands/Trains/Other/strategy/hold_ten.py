from typing import Set, Union

from Trains.Common.map import Map
from Trains.Common.player_game_state import PlayerGameState
from Trains.Other.destination import Destination
from Trains.Other.undirected_connection import UndirectedConnection
from Trains.Other.interfaces.i_strategy import MORE_CARDS_REQUEST
from Trains.Player.strategy import AStrategy


class HoldTenStrategy(AStrategy):
    """
    Represents a Hold-10 strategy for playing the Trains game. To perform a turn, a player will request cards if its
    total card count is less than or equal to 10 (or if there are no more acquirable connections), otherwise it will
    acquire the lexicographically least acquirable connection.
    """

    @classmethod
    def select_destinations(cls, _: Map, possible_destinations: Set[Destination]) -> Set[Destination]:
        """
        Select the two lexicographically least destinations (as defined by __lt__ on CityPair). The Map is unused in
        implementation of select_destinations.
        :param possible_destinations: the 5 destinations to choose from
        :return: the two lexicographically least elements of the set
        """
        sorted_destinations = sorted(possible_destinations)
        return {sorted_destinations[0], sorted_destinations[1]}

    @classmethod
    def get_turn(cls, player_state: PlayerGameState) -> Union[UndirectedConnection, str]:
        """
        Performs a turn according to Hold-10 (as described in the class docs)
        :param player_state: the knowledge the player has for the game
        :return: None if the player wants to receive cards or an UndirectedConnection representing the connection
        the player wants to acquire
        """
        card_count = player_state.own_state.cards.get_total_count()
        if card_count <= 10:
            return MORE_CARDS_REQUEST

        return super(HoldTenStrategy, cls).get_turn(player_state)