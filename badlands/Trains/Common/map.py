from typing import List, Dict, Set
import heapq

from collections import defaultdict
from Trains.Other.destination import Destination
from Trains.Other.city import City
from Trains.Other.directed_connection import DirectedConnection


class Map:
    """
    Represents the game board of our Trains game

    Args:
        width (int): the width of the map in pixels
        height (int): the height of the map in pixels
        cities (List[City]): List of cities contained in our map
        connections (List[DirectedConnection]): The connections between cities on our map

    Attributes:
        width (int): the width of the map in pixels
        height (int): the height of the map in pixels
        __adj_list (Dict[City, List[DirectedConnection]]): The graph of cities and connections as an adjacency list. As
        the actual Trains map has no notion of direction, for each edge A -> B, there should be an edge B -> A.
    """

    MIN_WIDTH = 10
    MIN_HEIGHT = 10
    MAX_WIDTH = 800
    MAX_HEIGHT = 800

    width = int
    height = int
    __adj_list: Dict[City, List[DirectedConnection]]

    def __init__(self, width: int, height: int, cities: List[City], connections: List[DirectedConnection]):
        """
        Construct a Trains game board
        :param width: the width of the map in pixels
        :param height: the height of the map in pixels
        :param cities: the list of cities on the board
        :param connections: the connections between the listed cities
        :raises ValueError: if width or height are invalid, a city's position is invalid,
                            or a city's outgoing connections are invalid
        """
        if width < self.MIN_WIDTH or width > self.MAX_WIDTH:
            raise ValueError(f"Width must be between {self.MIN_WIDTH} and {self.MAX_WIDTH}")

        if height < self.MIN_HEIGHT or height > self.MAX_HEIGHT:
            raise ValueError(f"Height must be between {self.MIN_HEIGHT} and {self.MAX_HEIGHT}")

        self.width = width
        self.height = height

        self.__adj_list = {}

        if not Map.__connections_are_mirrored(connections):
            raise ValueError("The list of directed connections must be symmetric")

        for city in cities:
            if not Map.__city_in_bounds(city, width, height):
                raise ValueError("City outside of board")

            self.__adj_list[city] = list(filter(lambda connection: connection.from_city == city, connections))

            if not Map.__has_unique_color_connections(self.__adj_list[city]):
                raise ValueError("A city's outgoing connections to the same city must have distinct colors")

        if not all(map(lambda connection: self.__verify_cities_in_connection(cities, connection), connections)):
            raise ValueError("Connections must use cities in the given list of cities")

    def get_cities(self) -> List[City]:
        """
        :return: a list of all the cities in the map
        """
        return list(self.__adj_list.keys())

    def get_city_names(self) -> List[str]:
        """
        :return: the names of all the cities in the map
        """
        return list(map(lambda city: city.name, self.get_cities()))

    def get_outgoing_connections(self, city: City) -> List[DirectedConnection]:
        """
        :param city: the city to get the outgoing connections for
        :return: the outgoing connections for a given city
        """
        return self.__adj_list[city]

    def get_all_directed_connections(self) -> List[DirectedConnection]:
        """
        :return: all of the map's connections
        """
        return [connection for connections in self.__adj_list.values() for connection in connections]

    def get_feasible_destinations(self, max_player_rails: int) -> Set[Destination]:
        """
        Finds all pairs of cities that could be connected to each other by acquiring connections.
        :param max_player_rails: the max number of segments the player can acquire
        :return: set of Destination
        """
        feasible_destinations = set()
        cities = self.get_cities()
        for i in range(len(cities)):
            origin_city = cities[i]
            distances = self.__get_min_distances(origin_city)

            for j in range(i + 1, len(cities)):
                dest_city = cities[j]
                if distances[dest_city] == float("inf") or distances[dest_city] > max_player_rails:
                    continue

                feasible_destinations.add(Destination(origin_city, dest_city))

        return feasible_destinations

    def are_cities_connected(self, city_1: City, city_2: City, acquired: Set[DirectedConnection]) -> bool:
        """
        Uses recursive DFS to determine whether two cities are connected using only the set of acquired connections
        :param city_1: one city
        :param city_2: the other city
        :param acquired: acquired connections available for traversal
        :return: whether the two given cities are connected using the connections that have been acquired
        """
        return self.__are_cities_connected_helper(city_1, city_2, acquired, set())

    def __are_cities_connected_helper(self, city_1: City, city_2: City, acquired: Set[DirectedConnection],
                                      visited_cities: Set[City]):
        """
        A helper method for are_cities_connected that keeps an accumulated set of visited cities to avoid cycles
        :param city_1: one city
        :param city_2: the other city
        :param acquired: acquired connections available for traversal
        :param visited_cities: cities that have already been visited by the graph search
        :return: whether the two given cities are connected using the connections that have been acquired and
                 visited cities
        """
        if city_1 == city_2:
            return True

        reachable_neighbor_cities = self.__get_reachable_neighbor_cities(city_1, acquired)
        for city in reachable_neighbor_cities:
            visited_cities = visited_cities.union({city_1})
            if city not in visited_cities and self.__are_cities_connected_helper(city, city_2, acquired, visited_cities):
                return True

        return False

    def longest_continuous_route(self, acquired_connections: Set[DirectedConnection]) -> int:
        """
        Computes the longest continuous route using the connections that have been acquired.
        Longest continuous route is defined as a simple, acyclic path whose length is the value of all the segments in
        the path added together
        :param acquired_connections: acquired connections available for traversal
        :return: the length of the longest continuous route
        """
        reachable_cities = {connection.from_city for connection in acquired_connections}
        longest_path = 0
        for city in reachable_cities:
            city_longest_path = self.__longest_path_from_city(city, acquired_connections, set())
            longest_path = max(longest_path, city_longest_path)

        return longest_path

    def __longest_path_from_city(self, city: City, acquired_connections: Set[DirectedConnection],
                                 visited_cities: Set[City]) -> int:
        """
        Uses recursive DFS to determine the length of the longest continuous path starting from the given city, keeping
        an accumulated set of all visited cities to avoid cycles
        :param city: the city to start from
        :param acquired_connections: acquired connections available for traversal
        :param visited_cities: cities that have already been visited by the graph search
        :return: the length of the longest continuous path starting from the given city
        """
        usable_connections = self.__get_usable_outgoing_connections(city, acquired_connections)
        longest_path = 0
        for connection in usable_connections:
            if connection.to_city not in visited_cities:
                visited_cities = visited_cities.union({connection.from_city})
                longest_path = max(longest_path, connection.length + self.__longest_path_from_city(connection.to_city,
                                                                                                   acquired_connections,
                                                                                                   visited_cities))

        return longest_path

    def __get_reachable_neighbor_cities(self, starting_city: City, acquired: Set[DirectedConnection]) -> Set[City]:
        """
        Gets the neighboring cities of the given city, only considering the connections that have been acquired.
        :param starting_city: the starting city
        :param acquired: acquired connections available for traversal
        :return: the set of reachable cities from the given city
        """
        usable_connections = self.__get_usable_outgoing_connections(starting_city, acquired)
        return {owned_connection.to_city for owned_connection in usable_connections}

    def __get_usable_outgoing_connections(self, city: City, acquired_connections: Set[DirectedConnection]) -> Set[
        DirectedConnection]:
        """
        :param city: city to get outgoing connections for
        :param acquired_connections: acquired connections available for traversal
        :return: the outgoing connections from the given city, filtering out connections that have not been acquired
        """
        outgoing_connections = set(self.__adj_list[city])
        return outgoing_connections.intersection(acquired_connections)

    @staticmethod
    def __connections_are_mirrored(connections: List[DirectedConnection]) -> bool:
        """
        :param connections: the list of connections to check
        :return: whether each connection in the list has a mirrored connection in the list, where a
        "mirrored connection" is a connection with the same length and color, but with from_city and to_city switched
        """
        return all(map(lambda connection: Map.__connection_has_mirror(connection, connections), connections))

    @staticmethod
    def __connection_has_mirror(connection: DirectedConnection, connections: List[DirectedConnection]) -> bool:
        """
        :param connection: the connection to look for a mirror of
        :param connections: the connections to find a mirror in
        :return: whether the given connection has a mirror connection in the given list of connections
        """
        return any(map(lambda connection_to_search: Map.__is_mirror(connection, connection_to_search), connections))

    @staticmethod
    def __is_mirror(connection_1: DirectedConnection, connection_2: DirectedConnection) -> bool:
        """
        :param connection_1: the first connection
        :param connection_2: the second connection
        :return: whether the given connections are mirrors of each other
        """
        return connection_1.to_city == connection_2.from_city \
               and connection_1.from_city == connection_2.to_city \
               and connection_1.color == connection_2.color \
               and connection_1.length == connection_2.length

    @staticmethod
    def __has_unique_color_connections(connections: List[DirectedConnection]) -> bool:
        """
        :param connections: list of connections to check the colors of
        :return: whether all the connections to any outgoing city have unique colors
        """
        occurred_colors = defaultdict(set)
        for connection in connections:
            if connection.color in occurred_colors[connection.to_city]:
                return False
            else:
                occurred_colors[connection.to_city].add(connection.color)
        return True

    @staticmethod
    def __verify_cities_in_connection(possible_cities: List[City], connection: DirectedConnection) -> bool:
        """
        :param possible_cities: the cities that can be used in the connection
        :param connection: the connection to check the cities of
        :return: whether the
        """
        return connection.from_city in possible_cities and connection.to_city in possible_cities

    @staticmethod
    def __city_in_bounds(city: City, width: int, height: int) -> bool:
        """
        :param city: city to check if in bounds
        :param width: the width of the map
        :param height: the height of the map
        :return: whether the city is in bounds
        """
        x_coordinate = city.position[0]
        y_coordinate = city.position[1]
        return 0 <= x_coordinate <= width and 0 <= y_coordinate <= height

    def __get_min_distances(self, origin_city: City) -> Dict[City, float]:
        """
        Uses Dijkstra's and a priority queue to determine min paths from the origin city to all other cities
        :param origin_city: the city to get the paths for
        :return: a mapping from city to their distance from the origin city, with float('inf') representing no path
        """
        distances = {city: float("inf") for city in self.get_cities()}
        completed = set()
        distances[origin_city] = 0

        priority_queue = [(0, origin_city)]
        while priority_queue:
            shortest_distance, current_city = heapq.heappop(priority_queue)

            if current_city not in completed:
                for connection in self.__adj_list[current_city]:
                    distance = shortest_distance + connection.length

                    if distance < distances[connection.to_city]:
                        distances[connection.to_city] = distance
                        heapq.heappush(priority_queue, (distance, connection.to_city))

            completed.add(current_city)

        return distances
