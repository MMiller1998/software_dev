import itertools
from typing import Iterator, Iterable, Set, List, Optional, Any

from trains.graph_elements import TrainPlaceId, TrainConnectionId, TrainPlace, TrainConnection, RailColor, Destination
from trains.errors import DuplicateTrainConnectionException

# For more info see: ../docs/trainmap_defense.md


class TrainMap:
    """
    A ``TrainMap`` is a representation of the board in the game *Trains*.

    ``TrainMap`` itself is mutable. To be specific, :class:`TrainPlace` and
    :class:`TrainConnection` can be added to it anytime.

    ``TrainMap`` is a graph where nodes are :class:`TrainPlace` and edges are
    :class:`TrainConnection`. These two structs, :class:`TrainPlace` and
    :class:`TrainConnection`, are doubly-linked, and have unique identifiers
    (UID) which relate them to the ``TrainMap`` they exist on.
    """
    def __init__(self, width: int, height: int):
        """
        Constructor for ``TrainMap``.
        """
        self.width = width
        self.height = height
        self._places: List[TrainPlace] = []
        self._connections: List[TrainConnection] = []

    def add_place(self, place_name: str, x_coord: int, y_coord: int) -> TrainPlace:
        """
        Add a *place* to this map.

        :param place_name: name of the place to add
        :return: id number of the newly added place
        """
        node = TrainPlace(place_name, x_coord, y_coord, TrainPlaceId(len(self._places)))
        self._places.append(node)
        return node

    def add_connection(self, place1: TrainPlace, place2: TrainPlace,
                       color: RailColor, length: int) -> TrainConnection:
        """
        Add a *connection* between two existing places on this map.
        The two specified places must have been created first by
        :meth:`add_place` before you call ``add_connection``.

        :param place1: one of the places which this connection connects
        :param place2: the other place which this connection connects
        :param color: the color of this connection
        :param length: the length of the connection, must be either 3, 4, or 5
        :return: an struct representing the newly created connection
        :raises TrainConnectionLengthException: if given length is not allowed
        :raises TrainConnectionToSelfException: if place1 and place2 are the same
        :raises DuplicateTrainConnectionException: if there already exists a connection
                                         between place1 and place2 that
                                         has the same color as the argument
                                         color
        :raises ValueError: if given place does not belong to this map
        """
        self.__assert_place_exists(place1.id)
        self.__assert_place_exists(place2.id)

        # check if there already exists a connection with the same color
        # between place1 and place2.
        for existing_connection in place1.get_connections():
            if place2 in existing_connection.get_places():
                if existing_connection.color == color:
                    raise DuplicateTrainConnectionException(
                        'There already exists a connection between '
                        f'place_id={place1.id} and place_id={place2.id} '
                        f'with the color "{color}"'
                    )
                break

        connection = TrainConnection(color, length, place1, place2, TrainConnectionId(len(self._connections)))
        self._connections.append(connection)
        return connection

    def get_destinations(self) -> Iterator[Destination]:
        """
        :return: all ``Destination`` that exist on this map.
        """
        all_nodes = set(self.get_all_places())
        yield from self._find_destinations_among(all_nodes)

    def _find_destinations_among(self, nodes: Set[TrainPlace]) -> Iterator[Destination]:
        """
        Find *destinations* among a given subset of *places*.

        Our solution to finding all the possible destinations is to first
        identify all the separate connected graphs of the given nodes
        (a "disjoint union of graphs").
        Next, we simply compute a cartesian product (without self (n, n) pairs).

        :param nodes: a subset of *places* which exist on this *map*
        :return: all *destinations* among the given subset of *places*
        """
        if not nodes:
            return

        node = self.__set_peek(nodes)
        graph = frozenset(self._find_connected_graph(node))
        yield from self._cartesian_product(graph)
        yield from self._find_destinations_among(nodes - graph)

    @classmethod
    def _find_connected_graph(cls, origin: TrainPlace, visited: Optional[Set[TrainPlace]] = None) -> Iterator[TrainPlace]:
        """
        Find a connected graph within a forest using breadth-first search.

        :param origin: node to start from
        :param visited: an accumulator for nodes which have already been yielded
        :return: a set of nodes which belong to the same graph as origin
        """
        if not visited:
            visited = set()
        if origin in visited:
            return
        visited.add(origin)

        yield origin

        for neighbor in origin.get_neighbors():
            yield from cls._find_connected_graph(neighbor, visited)

    @staticmethod
    def _cartesian_product(nodes: Iterable[TrainPlace]) -> Iterator[Destination]:
        """
        Find every :ref:`Destination` in a set of :class:`TrainPlace` where
        the given set of :class:`TrainPlace` is a connected graph.

        It works by producing the cartesian product of a one-dimensional vector
        with itself, but without the cases where an element is crossed with itself.

        :param nodes: one-dimensional vector
        :return: pairings of the Cartesian product
        """
        # explicit unspecific type-hint to suppress incorrect warning
        pairs: Iterable[tuple] = itertools.combinations(nodes, 2)
        # wrap in frozen set to convert to Destination type
        return map(frozenset, pairs)

    def get_all_places(self) -> List[TrainPlace]:
        """
        :return: a shallow copy of the places on this map
        """
        return list(self._places)

    def get_all_connections(self) -> List[TrainConnection]:
        """
        :return: a shallow copy of the places on this map
        """
        return list(self._connections)

    def get_connection(self, connection_id: TrainConnectionId) -> TrainConnection:
        """
        :param connection_id: a connection ID number
        :return: the connection associated with the given ID number
        """
        if connection_id > len(self._connections) or connection_id < 0:
            raise ValueError(f'No connection exists for given connection_id={connection_id}')
        return self._connections[connection_id]

    def get_place(self, place_id: TrainPlaceId) -> TrainPlace:
        """
        :param place_id: the unique id number of the place being queried
        :return: the name of the place associated with place_id
        """
        self.__assert_place_exists(place_id)
        return self._places[place_id]

    def __assert_place_exists(self, place_id: TrainPlaceId):
        """
        :param place_id: id to check
        :raises ValueError: if no place exists on this map for the given id
        """
        if place_id > len(self._places) or place_id < 0:
            raise ValueError(f'No place exists for given place_id={place_id}')

    @staticmethod
    def __set_peek(s: Set[Any]) -> Any:
        """
        Get an arbitrary member from a given set.

        :param s: a non-empty set
        :return: an arbitrary member from the given set
        """
        for element in s:
            return element
