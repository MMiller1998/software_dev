import importlib.util
import inspect
from typing import Set, Union, Type
from Trains.Common.map import Map
from Trains.Common.player_game_state import PlayerGameState
from Trains.Other.destination import Destination
from Trains.Other.interfaces.i_strategy import IStrategy, MORE_CARDS_REQUEST
from Trains.Other.undirected_connection import UndirectedConnection


class AStrategy(IStrategy):
    """
    Represents an abstract strategy a player uses to determine how to select destinations and what to do on their turn
    """

    @classmethod
    def select_destinations(cls, _: Map, possible_destinations: Set[Destination]) -> Set[Destination]:
        """
        This method should be overridden by any extending class
        :param possible_destinations: the 5 destinations to choose from
        :return: the set of 2 Destinations the strategy decides on
        """
        raise NotImplementedError()

    @classmethod
    def get_turn(cls, player_state: PlayerGameState) -> Union[UndirectedConnection, str]:
        """
        Attempt to acquire the lexicographically least acquirable connection. If there is no acquirable connection,
        request cards. If an implementing strategy wants different turn logic, this method must be overridden
        :param player_state: the knowledge the player has for the game
        :return: The string "more cards" if the player wants to receive cards or an UndirectedConnection representing
        the connection the player wants to acquire
        """
        acquirable_connections = player_state.get_acquirable_connections()
        if acquirable_connections:
            return sorted(acquirable_connections)[0]
        else:
            return MORE_CARDS_REQUEST

    @staticmethod
    def from_file(file_path: str) -> Type[IStrategy]:
        """
        Create a strategy from a filepath. This filepath must be a Linux path to a python file
        containing a single strategy.
        :param file_path: a valid filepath to a python file defining a strategy
        :return: a strategy object extending from IStrategy
        """
        module_name = 'strategy'
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if inspect.isclass(obj) and obj.__module__ == module_name and issubclass(obj, IStrategy):
                return obj

        raise ValueError("Could not find a strategy class in the file")
