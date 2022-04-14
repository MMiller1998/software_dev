from typing import Set, Union

from Trains.Common.map import Map
from Trains.Common.player_game_state import PlayerGameState
from Trains.Other.destination import Destination
from Trains.Other.interfaces.i_strategy import IStrategy, MORE_CARDS_REQUEST
from Trains.Other.undirected_connection import UndirectedConnection


class DummyStrategy(IStrategy):
    @classmethod
    def select_destinations(cls, _: Map, possible_destinations: Set[Destination]) -> Set[Destination]:
        return set()

    @classmethod
    def get_turn(cls, player_state: PlayerGameState) -> Union[UndirectedConnection, str]:
        return MORE_CARDS_REQUEST
