from typing import Set, Union, Type, List

from Trains.Common.map import Map
from Trains.Common.player_game_state import PlayerGameState
from Trains.Other.cards import Cards
from Trains.Other.color import Color
from Trains.Other.destination import Destination
from Trains.Other.interfaces.i_player import IPlayer
from Trains.Other.interfaces.i_strategy import IStrategy
from Trains.Other.undirected_connection import UndirectedConnection
from Trains.Player.strategy import AStrategy
from Trains.Other.map_generator import MapGeneratorDefault


class Player(IPlayer):
    """
    Represents a player in the Trains game. We assume names are unique.

    Args:
        strategy (): the strategy that the player will use to play the game (type is Type[Strategy])
        name (str): a string representing this player's name

    Attributes:
        strategy (Type[AStrategy]): the strategy that the player will use to play the game
        map (Union[None, Map]): the map for the game. It is initialized to None before the game starts
        initial_rails (Union[None, int]): the starting number of rails. It is initialized to None before the game starts
        initial_cards (Union[None, Cards]): the starting pile of cards. It is initialized to None before the game starts
        name (str): a string representing this player's name
    """
    def __init__(self, strategy: Type[IStrategy], name: str):
        self.strategy = strategy
        self.trains_map = None
        self.initial_rails = None
        self.initial_cards = None
        self.name = name


    @staticmethod
    def player_from_strategy_file(strategy_file: str, name: str) -> 'Player':
        """
        Constructs a player from a given strategy filepath. This filepath must be a Linux path to a python file
        containing a single strategy.
        :param strategy_file: an absolute path to a python file containing a single Strategy implementation
        :param name: the name of the player to be created
        :return: a Player using the given strategy
        """
        return Player(AStrategy.from_file(strategy_file), name)

    def setup(self, trains_map: Map, num_rails: int, starting_cards: List[Color]) -> None:
        self.trains_map = trains_map
        self.initial_rails = num_rails
        self.initial_cards = Cards.from_list(starting_cards)

    def pick(self, destinations: Set[Destination]) -> Set[Destination]:
        return destinations - self.strategy.select_destinations(self.trains_map, destinations)

    def play(self, player_game_state: PlayerGameState) -> Union[UndirectedConnection, str]:
        return self.strategy.get_turn(player_game_state)

    def more_cards(self, cards: Cards) -> None:
        """
        This implementation does not need to do anything with this information, so it is passed.
        """
        pass

    def win(self, did_win: bool) -> None:
        """
        This implementation does not need to do anything with this information, so it is passed.
        """
        pass

    def start(self, is_starting: bool) -> Map:
        return MapGeneratorDefault().generate_map()

    def end(self, has_won: bool) -> None:
        """
        This implementation does not need to do anything with this information, so it is passed.
        """
        pass

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Player):
            return self.name == other.name
        return False