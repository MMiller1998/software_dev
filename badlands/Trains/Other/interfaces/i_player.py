from typing import Set, Union, Type, List

from Trains.Common.map import Map
from Trains.Common.player_game_state import PlayerGameState
from Trains.Other.cards import Cards
from Trains.Other.color import Color
from Trains.Other.destination import Destination
from Trains.Other.undirected_connection import UndirectedConnection


class IPlayer:
    """
    Represents an interface for a player in the Trains game
    """

    def setup(self, trains_map: Map, num_rails: int, starting_cards: List[Color]) -> None:
        """
        Setup the player with the starting pieces for the game
        :param trains_map: the map for the game
        :param num_rails: the starting number of rails
        :param starting_cards: the starting pile of cards
        """
        raise NotImplementedError()

    def pick(self, destinations: Set[Destination]) -> Set[Destination]:
        """
        Pick the 2 destinations that the player wants to play with
        :param destinations: a set of 5 destinations to choose from
        :return: the 3 destinations that were not chosen
        """
        raise NotImplementedError()

    def play(self, player_game_state: PlayerGameState) -> Union[UndirectedConnection, str]:
        """
        Play a turn with the given player game state
        :param player_game_state: the current state of the game from this player's perspective
        :return: an UndirectedConnection to acquire, or the string "more cards" to receive more cards
        """
        raise NotImplementedError()

    def more_cards(self, cards: Cards) -> None:
        """
        Receive the requested cards from the Referee
        """
        raise NotImplementedError()

    def win(self, did_win: bool) -> None:
        """
        Be informed by the referee whether this player won
        """
        raise NotImplementedError()