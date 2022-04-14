import importlib.util as iu

from os import path
from pathlib import Path
from typing import FrozenSet, Optional, Callable, List, Iterable

from trains.graph_elements import Destination, TrainConnection
from trains.state.player import PlayerState, PlayerStateWrapper
from trains.state.action import ActionOption, Acquire, WantCards
from trains.strategy.lexico import LexicographicPairOfCities, LexicographicConnection


class Strategy:
    """
    A ``Strategy`` represents deterministic logic describing how a *player*
    makes decisions during setup of a game and on their turns during a game.
    """

    def choose_destinations(self, options: FrozenSet[Destination]) -> FrozenSet[Destination]:
        """
        Decide which 2 destinations will be chosen at the start of the game
        :param options: the destinations available to be picked
        """
        raise NotImplementedError()

    def take_turn(self, player: PlayerStateWrapper, all_connections: List[TrainConnection]) -> ActionOption:
        """
        Decides what a *player* should do on its turn.
        """
        unavailable_connections = player.get_unavailable_connections()
        unacquired_connections = set(all_connections) - unavailable_connections
        first_connection = choose_acquirable_lexicographically_first_connection(player.player_state,
                                                                                unacquired_connections)
        if first_connection:
            return Acquire(first_connection)
        return WantCards()

    def __eq__(self, other):
        return type(other) == type(self)


def choose_acquirable_lexicographically_first_connection(player_state: PlayerState,
                                                         all_connections: Iterable[TrainConnection]
                                                         ) -> Optional[TrainConnection]:
    """
    Select the first *connection* as ordered lexicographically, where the the given
    *player* may acquire with the rails and colored cards they have.

    If the given *player* cannot acquire anything, returns ``None``.
    """
    acquirable_connections = [
        LexicographicConnection(c) for c in player_state.acquirable_connections(all_connections)
    ]
    if not acquirable_connections:
        return None

    # a linear search (recursive helper) would take O(n), sorting takes O(nlogn)
    # but we don't care about efficiency.
    acquirable_connections.sort()
    return acquirable_connections[0].original


LexicographicSelector = Callable[[List[LexicographicPairOfCities]], List[LexicographicPairOfCities]]
"""
A ``LexicographicSelector`` is a function which picks some elements from a
lexicographically sorted :class:`list` of :class:`LexicographicPairOfCities`.

The returned list must have a length equal to :const:`STARTING_DESTINATION_TAKE_COUNT`.
"""


def choose_among_lexicographically_sorted(
        options: FrozenSet[Destination],
        chooser: LexicographicSelector
) -> FrozenSet[Destination]:
    """
    Sorts a given set of *destinations* lexicographically and allows for
    a selection to be made with respect to the lexicographic ordering.

    :param options: destinations offered from the referee to the player
    :param chooser: a function which slices the strategy's choice from the given list
    :return: the strategy's selected destinations
    """
    ordered_options = [LexicographicPairOfCities(a, b) for a, b in options]
    ordered_options.sort()
    selection = chooser(ordered_options)
    return frozenset(p.to_destination() for p in selection)


def strategy_name_to_file_name(strategy_name: str) -> str:
    return f"{strategy_name.replace('-', '_').lower()}.py"


def strategy_name_to_file_path(strategy_name: str) -> Path:
    strategy_file_name = strategy_name_to_file_name(strategy_name)
    return Path(f'{path.dirname(path.abspath(__file__))}/{strategy_file_name}')


def load_strategy(strategy_path: Path) -> Strategy:
    """
    Loads a *strategy* from a given path. The *strategy* must inherit from :class:`Strategy` and
    its class name must be ``MyStrategy``.
    """
    module_name = path.basename(strategy_path)[:-3]
    spec = iu.spec_from_file_location(module_name, strategy_path)
    mod = spec.loader.load_module(module_name)
    return mod.MyStrategy()
