from pathlib import Path
from typing import FrozenSet, Optional

import tests.examples.bigger_map as example

from trains.strategy.strategy import strategy_name_to_file_path
from trains.graph_elements import Destination
from trains.map import TrainMap
from trains.state.player import PlayerStateWrapper
from trains.state.cardsholder import CardDeck
from trains.strategy.strategy import Strategy, ActionOption, load_strategy


class PlayerActor:

    def __init__(self, strategy: Strategy, train_map_for_start: TrainMap = example.train_map, name: str = ''):
        self.active_train_map: TrainMap = None
        self.strategy = strategy
        self.train_map_for_start = train_map_for_start
        self.name = name

    ### API for referee

    def setup(self, train_map: TrainMap, r: int, cards: CardDeck) -> None:
        self.active_train_map = train_map

    def play(self, state: PlayerStateWrapper) -> ActionOption:
        return self.strategy.take_turn(state, self.active_train_map.get_all_connections())

    def pick(self, destinations: FrozenSet[Destination]) -> FrozenSet[Destination]:
        return self.strategy.choose_destinations(destinations)

    def more(self, cards: CardDeck) -> None:
        pass

    def win(self, won: bool) -> None:
        pass

    # API for tournament manager

    def start(self, participating: bool) -> TrainMap:
        return self.train_map_for_start

    def end(self, won_tourney: bool) -> None:
        pass


def create_player_actor_from_strategy_path(name: str, strategy_filename: Path, train_map_for_start: Optional[TrainMap] = None):
    """
    :param train_map_for_start: `TrainMap` the `PlayerActor` should return when its `start` method is called
    """
    if train_map_for_start:
        return PlayerActor(load_strategy(strategy_filename), train_map_for_start=train_map_for_start, name=name)
    return PlayerActor(load_strategy(strategy_filename), name=name)


def create_player_actor_from_strategy_name_via_path(
    name: str, strategy_name: str, train_map_for_start: Optional[TrainMap] = None
) -> PlayerActor:
    strategy_file_path = strategy_name_to_file_path(strategy_name)
    return create_player_actor_from_strategy_path(name, strategy_file_path, train_map_for_start=train_map_for_start)
