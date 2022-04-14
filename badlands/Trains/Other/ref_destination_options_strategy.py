import random
from typing import List, Set, Union

from Trains.Other.destination import Destination


# TODO: docs and tests
class DestinationOptionsStrategy:
    """
    A strategy to order the feasible destinations for a map for usage in proposing destinations to players
    """
    def order_destinations(self, feasible_destinations: Set[Destination]) -> List[Destination]:
        """
        Order the given the destinations by some specified ordering.
        :param feasible_destinations: a set of destinations to order
        :return: a list of destination in the desired order
        """
        raise NotImplementedError()


class RandomDestinationOptionsStrategy(DestinationOptionsStrategy):
    """
    A strategy for ordering destination options randomly
    """
    def __init__(self, seed: Union[int, None] = None):
        if seed:
            random.seed(seed)

    def order_destinations(self, feasible_destinations: Set[Destination]) -> List[Destination]:
        """
        Order the given destinations in a random order
        :param feasible_destinations: a set of destinations to order
        :return: a list of destinations in a random order
        """
        random_destinations = list(feasible_destinations)
        random.shuffle(random_destinations)
        return random_destinations
