from typing import Iterable, Set

from Trains.Other.city import City
from Trains.Other.color import Color
from Trains.Other.undirected_connection import UndirectedConnection


class DirectedConnection:
    """
    Represents the connection between two cities. It's directed so there will be
    two DirectedConnections for every city connection you want to represent

    Args:
        from_city (City): the city this connection starts from
        to_city (City): the city this connection ends at
        length (int): how many segments the connection has
        color (Color): the color of the connection

    Attributes:
        from_city (City): the city this connection starts from
        to_city (City): the city this connection ends at
        length (int): how many segments the connection has
        color (Color): the color of the connection
    """
    from_city: City
    to_city: City
    length: int
    color: Color

    def __init__(self, from_city: City, to_city: City, length: int, color: Color):
        """
        Construct a DirectedConnection from from_city to to_city
        :param from_city: the city that the connection is originating from
        :param to_city: the city that the connection is going to
        :param length: the number of segments that the connection is composed of
        :param color: the color of the connection
        :raises ValueError: if length is not 3, 4, or 5 or if the two cities are the same
        """
        if length < 3 or length > 5:
            raise ValueError("Length must be 3, 4, or 5")

        if from_city == to_city:
            raise ValueError("from_city must differ from to_city")
        self.from_city = from_city
        self.to_city = to_city
        self.length = length
        self.color = color

    def make_undirected(self) -> UndirectedConnection:
        """
        Constructs an instance of an UndirectedConnection from this DirectedConnection
        :return: an UndirectedConnection with the same two cities, length, and color as the directed connection
        """
        return UndirectedConnection(self.from_city, self.to_city,
                                    self.length, self.color)

    @staticmethod
    def convert_undirected_connections(undirected_connections: Iterable[UndirectedConnection]) -> \
            Set['DirectedConnection']:
        directed_connections = set()
        for undirected_connection in undirected_connections:
            directed_connections.add(DirectedConnection(undirected_connection.get_city_1(),
                                                        undirected_connection.get_city_2(),
                                                        undirected_connection.length,
                                                        undirected_connection.color))
            directed_connections.add(DirectedConnection(undirected_connection.get_city_2(),
                                                        undirected_connection.get_city_1(),
                                                        undirected_connection.length,
                                                        undirected_connection.color))
        return directed_connections

    # Override
    def __eq__(self, other):
        return self.from_city == other.from_city and \
               self.to_city == other.to_city and \
               self.length == other.length and \
               self.color == other.color

    # Override
    def __hash__(self):
        return hash((self.from_city, self.to_city, self.length, self.color.value))
