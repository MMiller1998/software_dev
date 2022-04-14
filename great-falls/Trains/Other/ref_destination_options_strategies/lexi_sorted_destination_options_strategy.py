from typing import List, Set

from Trains.Other.destination import Destination
from Trains.Other.interfaces.i_ref_destination_options_strategy import IDestinationOptionsStrategy


class LexiSortedDestinationOptionsStrategy(IDestinationOptionsStrategy):
    """
    A player_strategies for putting destinations in lexicographical order
    """
    def __init__(self):
        pass

    def order_destinations(self, feasible_destinations: Set[Destination]) -> List[Destination]:
        """
        :param feasible_destinations: a set of destinations to order
        :return: a list of destinations in lexicographical order
        """
        return list(sorted(feasible_destinations))
