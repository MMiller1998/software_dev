import random
from typing import List, Set, Union

from Trains.Other.destination import Destination
from Trains.Other.interfaces.i_ref_destination_options_strategy import IDestinationOptionsStrategy


class RandomDestinationOptionsStrategy(IDestinationOptionsStrategy):
    """
    A player_strategies for ordering destination options randomly
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
