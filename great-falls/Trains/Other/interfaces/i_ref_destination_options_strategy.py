from typing import List, Set

from Trains.Other.destination import Destination


class IDestinationOptionsStrategy:
    """
    A player_strategies to order the feasible destinations for a map for usage in proposing destinations to players
    """

    def order_destinations(self, feasible_destinations: Set[Destination]) -> List[Destination]:
        """
        Order the given the destinations by some specified ordering.
        :param feasible_destinations: a set of destinations to order
        :return: a list of destination in the desired order
        """
        raise NotImplementedError()
