from typing import FrozenSet, Iterable

from trains.graph_elements import Destination, TrainConnection, RailColor
from trains.game.constants import STARTING_DESTINATION_RETURN_COUNT
from trains.state.player import PlayerStateWrapper
from trains.state.action import ActionOption, Acquire
from trains.strategy.strategy import (
    Strategy,
    choose_among_lexicographically_sorted
)


class MyStrategy(Strategy):
    def choose_destinations(self, options: FrozenSet[Destination]) -> FrozenSet[Destination]:
        return choose_among_lexicographically_sorted(
            options,
            lambda ordered_options: ordered_options[:STARTING_DESTINATION_RETURN_COUNT]
        )

    def take_turn(self, player: PlayerStateWrapper, connections: Iterable[TrainConnection]) -> ActionOption:
        """
        Attempts to acquire a non-existent connection.
        """
        dest1, _ = player.player_state.destinations
        place1, place2 = dest1
        conn = TrainConnection(RailColor.WHITE, 5, place1, place2, -1)
        return Acquire(conn)
