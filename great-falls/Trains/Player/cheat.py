from typing import Union

from Trains.Common.player_game_state import PlayerGameState
from Trains.Other.city import City
from Trains.Other.color import Color
from Trains.Other.undirected_connection import UndirectedConnection
from Trains.Player.buy_now import BuyNowStrategy


class CheatStrategy(BuyNowStrategy):
    """
    Represents a strategy for playing the Trains game that tries to cheat. It will always attempt to acquire
    a connection that does not exist
    """

    @classmethod
    def get_turn(cls, player_state: PlayerGameState) -> Union[UndirectedConnection, str]:
        city_1 = City("testtesttesttest", [0, 0])
        city_2 = City("not a real city", [15, 15])
        return UndirectedConnection(city_1, city_2, 3, Color.BLUE)
