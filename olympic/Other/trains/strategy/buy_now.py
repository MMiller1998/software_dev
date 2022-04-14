from typing import FrozenSet

from trains.graph_elements import Destination
from trains.game.constants import STARTING_DESTINATION_RETURN_COUNT
from trains.strategy.strategy import (
    Strategy,
    choose_among_lexicographically_sorted,
)


class MyStrategy(Strategy):
    def choose_destinations(self, options: FrozenSet[Destination]) -> FrozenSet[Destination]:
        """
        :param options: the destinations offered to the player by the referee
        :returns: the first two offered destinations that come last in lexicographic order
        """
        return choose_among_lexicographically_sorted(
            options,
            lambda ordered_options: ordered_options[:STARTING_DESTINATION_RETURN_COUNT]
        )

