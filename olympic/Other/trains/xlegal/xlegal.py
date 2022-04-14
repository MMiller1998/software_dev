# TODO broken since 0cf6f59e34ccfe3d32867fc8df1fc40a21b64050

from typing import TextIO, List, Tuple, Union

from trains.graph_elements import TrainConnection, RailColor
from trains.errors import TrainsBaseException
from trains.map import TrainMap
from trains.state.cardsholder import EMPTY_PILE
from trains.state.referee import RefereeState
from trains.state.player import PlayerState
from trains.parsing import StatefulSpacedJSONParser
from trains.utils import build_visual_map

Acquired = Union[list, Tuple[str, str, str, int]]
"""
``Acquired`` is defined here:

https://www.ccs.neu.edu/home/matthias/4500-f21/5.html

    Acquired is ``[Name, Name, Color, Length]``

Where ``Name`` is the name of a :class:`trains.graph_elements.TrainPlace`,
``Color`` is the value corresponding to a :class:`RailColor`, and ``Length``
is a length of a :class:`TrainConnection`.
"""


class TrainConnectionNotFoundException(TrainsBaseException):
    """
    Raised when a *connection* is given as a JSON via input,
    but is not part of the input *map*.
    """
    pass


def acquired_is_connection(acquired: Acquired, connection: TrainConnection) -> bool:
    """
    An equality check between an ``Acquired``, as defined by the assignment,
    and a :class:`TrainConnection`.

    :param acquired: a list of length 4 containing the names of two places, the name
                     of a rail color, and a connection length, in that order
    :param connection: the existing object to compare the Acquired with
    :return: true if the Acquired represents the connection
    """
    city1, city2, color, length = acquired
    these_place_names = {city1, city2}
    other_place_names = set(p.name for p in connection.get_places())

    return these_place_names == other_place_names \
        and connection.color.value == color \
        and connection.length == length


def acquired2connection(trainmap: TrainMap, acquired: Acquired) -> TrainConnection:
    """
    Finds the :class:`TrainConnection` inside the given :class:`TrainMap` which
    represents the same *connection* as represented by the given list.

    :param trainmap: the TrainMap to find the given acquired connection on
    :param acquired: the connection as a parsed list to resolve
    :return: the resolved TrainConnection
    """
    for connection in trainmap.get_all_connections():
        if acquired_is_connection(acquired, connection):
            return connection
    raise TrainConnectionNotFoundException(acquired)


def create_one_player(player_json: dict) -> PlayerState:
    """
    uses a *PlayerState* JSON and board to create a PlayerState

    :param player_json:
    :return:
    """
    destinations = frozenset((
        frozenset(player_json['this']['destination1']),
        frozenset(player_json['this']['destination2']),
    ))
    player = PlayerState(destinations=destinations,
                         occupied=None,
                         cards={RailColor(c): n for c, n in player_json['this']['cards'].items()},
                         num_rails=player_json['this']['rails'])
    return player


def add_existing_acquisitions(referee: RefereeState, train_map: TrainMap, acquisitions: List[List[Acquired]]):
    """
    Marks all acquired connections as acquired in the given BoardState

    :param referee:
    :param acquisitions:
    :param train_map:
    """
    for player in acquisitions:
        for acquired in player:
            connection = acquired2connection(train_map, acquired)
            referee.current_player.occupy(connection)


def answer_legal_acquisition(player: PlayerState, connection: TrainConnection) -> str:
    """
    A wrapper around :meth:`PlayerState.can_acquire` which produces the result
    as one of "true" or "false" instead of a :class:`bool`.
    """
    return 'true' if player.can_acquire(connection) else 'false'


def xlegal(infile: TextIO, outfile: TextIO) -> int:
    """
    Consumes a JSON *Map*, *PlayerState*, and *Acquired* from the given input stream. Prints true
    or false depending on whether or not the player represented by the *PlayerState* can acquire
    the connection represented by the *Acquired* given the *Map*

    :param infile: input stream
    :param outfile: output stream
    :return: 0 if program was successful, 1 in case of any usage error
    """

    parser = StatefulSpacedJSONParser(infile.read())
    train_map = build_visual_map(parser.read_object()).get_map()
    player_json = parser.read_object()
    acquired: Acquired = parser.read_array()

    player = create_one_player(player_json)

    referee = RefereeState(train_map=train_map,
                           players=(player, ),
                           cheaters=frozenset(),
                           cards=EMPTY_PILE)
    add_existing_acquisitions(referee, train_map, player_json['acquired'])

    connection = acquired2connection(train_map, acquired)
    answer = referee.is_acquisition_allowed(connection)

    outfile.write(f'{answer}\n')
    return 0
