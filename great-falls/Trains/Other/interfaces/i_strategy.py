from typing import Set, Union

from Trains.Common.map import Map
from Trains.Common.player_game_state import PlayerGameState
from Trains.Other.destination import Destination
from Trains.Other.undirected_connection import UndirectedConnection

MORE_CARDS_REQUEST = "more cards"


class IStrategy:
    """
    Represents a strategy a player uses to determine how to select destinations and what to do on their turn
    """

    @classmethod
    def select_destinations(cls, _: Map, possible_destinations: Set[Destination]) -> Set[Destination]:
        """
        Select 2 destinations from the given 5 possible destinations
        :param possible_destinations: the 5 destinations to choose from
        :return: the set of 2 Destinations the strategy decides on
        """
        raise NotImplementedError()


    # TODO: convert turn results into an interface
    @classmethod
    def get_turn(cls, player_state: PlayerGameState) -> Union[UndirectedConnection, str]:
        """
        Choose how to play a turn based on the given game state. The strategy should either choose to acquire a
        connection or request more cards
        :param player_state: the knowledge the player has for the game
        :return: The string "more cards" if the player wants to receive cards or an UndirectedConnection representing
        the connection the player wants to acquire
        """
        raise NotImplementedError()