from typing import TextIO, List, Tuple

from trains.parsing import StatefulSpacedJSONParser
from trains.utils import build_visual_map
from trains.graph_elements import TrainConnection, Destination, RailColor
from trains.map import TrainMap
from trains.state.player import PlayerState
from trains.state.referee import RefereeState
from trains.errors import InvalidTrainConnectionException, TrainsBaseException
from trains.state.cardsholder import EMPTY_PILE
from trains.strategy.strategy import HoldTen


class DestinationNotFoundException(TrainsBaseException):
    pass


def find_destination(train_map: TrainMap, raw: List[str]) -> Destination:
    raw_names = {raw[0], raw[1]}
    for destination in train_map.get_destinations():
        place_names = {p.name for p in destination}
        if raw_names == place_names:
            return destination
    raise DestinationNotFoundException(str(raw))


# TODO abstraction between find_destination and find_connection


def find_connection(train_map: TrainMap, raw: Tuple[str, str, str, int]) -> TrainConnection:
    raw_names = {raw[0], raw[1]}
    raw_color = RailColor(raw[2])
    raw_length = raw[3]

    for connection in train_map.get_all_connections():
        place_names = {p.name for p in connection.get_places()}
        if raw_names == place_names and raw_color == connection.color and raw_length == connection.length:
            return connection

    raise InvalidTrainConnectionException(f'No connection found for {str(raw)}')


def deserialize_playerstate(train_map: TrainMap, data: dict) -> PlayerState:
    return PlayerState(
        destinations=frozenset((
            find_destination(train_map, raw=data['destination1']),
            find_destination(train_map, raw=data['destination2']),
        )),
        occupied=[find_connection(train_map, acquired) for acquired in data['acquired']],
        num_rails=data['rails'],
        cards={RailColor(color): count for color, count in data['cards'].items()}
    )


def construct_opponent_playerstate(train_map: TrainMap, acquireds: List[Tuple[str, str, str, int]]) -> PlayerState:
    return PlayerState(
        destinations=frozenset(),
        occupied=[find_connection(train_map, acquired) for acquired in acquireds]
    )


def xstrategy(infile: TextIO, outfile: TextIO) -> int:
    """
    Consumes a JSON *Map* and *PlayerState* from the given input stream. Prints out the move
    that the Hold-10 strategy would make, either "more cards" if cards are being requested or
    the connection that will be acquired.

    :param infile: input stream
    :param outfile: output stream
    :return: 0 if program was successful, 1 in case of any usage error
    """

    parser = StatefulSpacedJSONParser(infile.read())
    train_map = build_visual_map(parser.read_object()).get_map()
    player_json = parser.read_object()

    player = deserialize_playerstate(train_map, player_json['this'])
    opponents = tuple(construct_opponent_playerstate(train_map, acquireds) for acquireds in player_json['acquired'])

    referee = RefereeState(
        train_map=train_map,
        players=(player,) + opponents,
        cheaters=frozenset(),
        cards=EMPTY_PILE
    )

    strategy = HoldTen()
    action = strategy.take_turn(player=player, connections=referee.get_acquirable())
    outfile.write(action.to_output())

    return 0
