from typing import FrozenSet, List

from trains.graph_elements import Destination, TrainConnection
from trains.game.constants import STARTING_DESTINATION_TAKE_COUNT
from trains.state.player import PlayerStateWrapper, PlayerState
from trains.state.action import ActionOption, WantCards, Acquire
from trains.strategy.strategy import (
    Strategy,
    choose_among_lexicographically_sorted,
)


class MyStrategy(Strategy):

    def choose_destinations(self, options: FrozenSet[Destination]) -> FrozenSet[Destination]:
        """
        :param options: the destinations offered to the player by the referee
        :returns: the first two offered destinations that come first in lexicographic order
        """
        return choose_among_lexicographically_sorted(
            options,
            lambda ordered_options: ordered_options[STARTING_DESTINATION_TAKE_COUNT:]
        )

    def take_turn(self, player: PlayerStateWrapper, all_connections: List[TrainConnection]) -> ActionOption:
        """
        Requests cards if the *player* has fewer than 10.
        Otherwise, attempts to acquire the first connection from the lexicographically sorted
        sequence which the *player* has enough rails and colored cards for. If there are none,
        this strategy falls back to asking for more cards.
        """
        if self._total_colored_cards(player.player_state) <= 10:
            return WantCards()
        return super().take_turn(player, all_connections)

    @staticmethod
    def _total_colored_cards(player: PlayerState) -> int:
        """
        Count the number of colored cards this *player* has.
        """
        return sum(player.cards.values())
