from enum import Enum
from typing import NewType, FrozenSet, Set, Optional
from trains.constants import TRAIN_CONNECTION_LENGTHS
from trains.errors import TrainConnectionLengthException, TrainConnectionToSelfException


class RailColor(Enum):
    """
    ``RailColor`` is an enum for the possible colors a :class:`TrainConnection`
    may be.
    """
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
    WHITE = 'white'


TrainPlaceId = NewType('TrainPlaceId', int)
"""
A ``TrainPlaceId`` is a natural number which uniquely identifies a *place*
on the :class:`TrainMap` which the *place* is associated with.
"""


TrainConnectionId = NewType('TrainConnectionId', int)
"""
A ``TrainConnectionId`` is a natural number which uniquely identifies a *connection*
on the :class:`TrainMap` which the *connection* is associated with.
"""


class TrainPlace:
    """
    A ``TrainPlace`` is a *place* which belongs on a :class:`TrainMap`.

    It is connected to other ``TrainPlace`` by :class:`TrainConnection`.
    """

    def __init__(self, name: str, x_coord: int, y_coord: int, place_id: TrainPlaceId):
        """
        Constructor for ``TrainPlace``.

        A client of :module:`trains.map` should not construct ``TrainPlace``
        directly. Only :class:`TrainMap` should call this constructor.

        :param name: name of the place
        :param place_id: UID of the place
        """
        self._connections: Set['TrainConnection'] = set()
        self.name: str = name
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.id: TrainPlaceId = place_id

    def _add_connection(self, connection: 'TrainConnection'):
        """
        Link this place to a *connection* which connects with it.
        You should not call this method. It should only be called internally.

        :param connection: connection to be linked with
        """
        self._connections.add(connection)

    def get_connections(self) -> FrozenSet['TrainConnection']:
        """
        Get the *connections* which connect to this place.

        :return: a set of connections which connect with this place
        """
        return frozenset(self._connections)

    def get_neighbors(self, connection_filter: Optional[Set['TrainConnection']] = None) -> FrozenSet['TrainPlace']:
        """
        :param connection_filter: if given, only consider connections in this set
        :return: all ``TrainPlace`` which this ``TrainPlace`` is directly connected with
        """
        self_connections = self.get_connections()
        if connection_filter is not None:
            self_connections = self_connections.intersection(connection_filter)

        return frozenset(c.get_other(self) for c in self_connections)

    def get_connections_between(self, other: 'TrainPlace', connection_filter: Optional[Set['TrainConnection']] = None) -> FrozenSet['TrainConnection']:
        """
        :param connection_filter: if given, only consider connections in this set
        :return: all connections between between this ``TrainPlace`` and another.
        """
        self_connections = self.get_connections()
        other_connections = other.get_connections()
        if connection_filter is not None:
            self_connections = self_connections.intersection(connection_filter)
            other_connections = other_connections.intersection(connection_filter)
            # TODO: Just fixed what I think is a typo here where "other_connections" was
            #   other_connection...make sure that was a typo and didn't introduce a bug

        return frozenset(self_connections.intersection(other_connections))

    def __hash__(self):
        return hash((self.id, self.name, self.x_coord, self.y_coord))

    def __eq__(self, other):
        if other is self:
            return True
        if not isinstance(other, self.__class__):
            return False
        return (
            self.id == other.id and
            self.name == other.name and
            self.x_coord == other.x_coord and
            self.y_coord == other.y_coord
        )

    def __repr__(self):
        return f'TrainPlace[{self.id},"{self.name}"]'


class TrainConnection:
    """
    A ``TrainConnection`` is a *connection* which belongs on a :class:`TrainMap`.

    It represents a direct connection between two :class:`TrainPlace`.
    """

    # noinspection PyProtectedMember
    def __init__(self, color: RailColor, length: int,
                 place1: TrainPlace, place2: TrainPlace,
                 connection_id: TrainConnectionId):
        """
        Constructor for ``TrainConnection``.

        It sets up doubly-links between itself and the two *places* it connects.

        A client of :mod:`trains.map` should not construct ``TrainConnection``
        directly. Only :class:`TrainMap` should call this constructor.

        :param color: color of this connection
        :param length: length of this connection, must be one of: 3, 4, 5
        :param place1: one of the places which this connection is directly connected to
        :param place2: the other place which this connection is directly connected to
        :param connection_id: the unique identifying number that will be used to identify the connection
        :raises TrainConnectionLengthException: if given length is not allowed
        :raises TrainConnectionToSelfException: if place1 and place2 are the same
        """
        if not isinstance(length, int) or length not in TRAIN_CONNECTION_LENGTHS:
            raise TrainConnectionLengthException('Length must be one of: ' + str(TRAIN_CONNECTION_LENGTHS))

        if place1 == place2:
            raise TrainConnectionToSelfException(
                'Cannot have a TrainConnection which connects the same place to itself.')

        self.id: TrainConnectionId = connection_id

        self.color = color
        self.length = length

        self._place1 = place1
        self._place2 = place2
        place1._add_connection(self)
        place2._add_connection(self)

    def get_places(self) -> FrozenSet[TrainPlace]:
        """
        :return: a set with length 2 of the places which are connected by this connection
        """
        return frozenset((self._place1, self._place2))

    def get_other(self, place: TrainPlace) -> TrainPlace:
        """
        :param place: one of the places which connect with this connection
        :return: the place which was not given as a parameter
        :raises ValueError: if given place is not connected with this connection
        """
        if place == self._place1:
            return self._place2
        if place == self._place2:
            return self._place1
        raise ValueError(f'place_id={place.id} is not connected by connection_id={self.id}')

    def __str__(self):
        return f'Connection[from={self._place1},to={self._place2},{self.color},{self.length}]'

    def __hash__(self):
        return hash((self.id, self.color, self.length, self._place1.name, self._place2.name))

    def __eq__(self, other):
        if other is self:
            return True
        if not isinstance(other, self.__class__):
            return False
        return (
                self.id == other.id and
                self.color == other.color and
                self.length == other.length and
                set(self.get_places()) == set(self.get_places())
        )

    def __repr__(self):
        return f'TrainConnection id {self.id} {self.color} {self.length} ({self._place1}, {self._place2})'


Destination = FrozenSet[TrainPlace]
"""
A ``Destination`` is a pair of :class:`TrainPlace` which are connected
by one or more :class:`TrainConnection`.
Since it is representing a pair, Destination must have a length of 2.
"""
