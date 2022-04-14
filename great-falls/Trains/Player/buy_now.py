from typing import Set

from Trains.Common.map import Map
from Trains.Other.destination import Destination
from Trains.Player.strategy import AStrategy


class BuyNowStrategy(AStrategy):
    """
    Represents a Buy-Now strategy for playing the Trains game. To perform a turn, a player will acquire the
    lexicographically least acquirable connection. If there is no acquirable connection, they will request cards.
    """

    @classmethod
    def select_destinations(cls, _: Map, possible_destinations: Set[Destination]) -> Set[Destination]:
        """
        Select the two lexicographically greatest destinations (as defined by __lt__ on CityPair). The Map is unused in
        implementation of select_destinations.
        :param possible_destinations: the 5 destinations to choose from
        :return: the two lexicographically greatest elements of the set
        """
        sorted_destinations = sorted(possible_destinations)
        return {sorted_destinations[-1], sorted_destinations[-2]}
