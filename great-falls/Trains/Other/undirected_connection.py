from Trains.Other.city import City
from Trains.Other.color import Color
from Trains.Other.city_pair import CityPair


class UndirectedConnection:
    """
    Represents an undirected connection between two cities. city_1 is always lexicographically less than city_2

    Args:
        city_1 (City): the city this connection starts from
        city_2 (City): the city this connection ends at
        length (int): how many segments the connection has
        color (Color): the color of the connection

    Attributes:
        _city_pair (CityPair): the pair of cities that make up the connection
        length (int): how many segments the connection has
        color (Color): the color of the connection
    """
    __city_pair: CityPair
    length: int
    color: Color

    def __init__(self, city_1: City, city_2: City, length: int, color: Color):
        """
        Construct an UndirectedConnection for the two cities
        :param city_1: one city in the connection
        :param city_2: the other city in the connection
        :param length: the number of segments that the connection is composed of
        :param color: the color of the connection
        :raises ValueError: if length is not 3, 4, or 5 or if the two cities are the same
        """
        if length < 3 or length > 5:
            raise ValueError("Length must be 3, 4, or 5")

        if city_1 == city_2:
            raise ValueError("city_1 must differ from city_2")

        self.__city_pair = CityPair(city_1, city_2)
        self.length = length
        self.color = color

    # Override
    def __eq__(self, other):
        return self.__city_pair == other.__city_pair and self.length == other.length and self.color == other.color

    # Override
    def __hash__(self):
        return hash((self.__city_pair, self.length, self.color.value))

    # Override
    def __lt__(self, other):
        """
        Determines if a connection is less than another by comparing the city pair. If those are equal, then the length
        is compared. If those are equal, then the color is used as a tiebreaker.
        :param other: the other connection being compared against
        :return: true if this connection is less than the other, false otherwise
        """
        if self.__city_pair == other.__city_pair:
            if self.length == other.length:
                return self.color.value < other.color.value
            return self.length < other.length

        return self.__city_pair < other.__city_pair

    def get_city_1(self) -> City:
        return self.__city_pair.city_1

    def get_city_2(self) -> City:
        return self.__city_pair.city_2
