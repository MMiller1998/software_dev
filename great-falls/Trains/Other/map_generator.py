from Trains.Other.interfaces.i_map_generator import IMapGenerator
from Trains.Common.map import Map
from Trains.Other.city import City
from Trains.Other.directed_connection import DirectedConnection
from Trains.Other.color import Color

class MapGeneratorDefault(IMapGenerator):
    """
    Generates a default map with enough destinations for 8 players
    """

    MAP_WIDTH = 800
    MAP_HEIGHT = 800
    LENGTH = 3

    CITY_NAME_1 = "city1"
    CITY_NAME_2 = "city2"
    CITY_NAME_3 = "city3"
    CITY_NAME_4 = "city4"
    CITY_NAME_5 = "city5"
    CITY_NAME_6 = "city6"
    CITY_NAME_7 = "city7"

    POSITION_1 = (0, 0)
    POSITION_2 = (50, 50)
    POSITION_3 = (75, 50)
    POSITION_4 = (50, 250)
    POSITION_5 = (300, 300)
    POSITION_6 = (300, 301)
    POSITION_7 = (400, 301)

    CITY_1 = City(CITY_NAME_1, POSITION_1)
    CITY_2 = City(CITY_NAME_2, POSITION_2)
    CITY_3 = City(CITY_NAME_3, POSITION_3)
    CITY_4 = City(CITY_NAME_4, POSITION_4)
    CITY_5 = City(CITY_NAME_5, POSITION_5)
    CITY_6 = City(CITY_NAME_6, POSITION_6)
    CITY_7 = City(CITY_NAME_7, POSITION_7)
    CITY_LIST = [CITY_1, CITY_2, CITY_3, CITY_4, CITY_5, CITY_6, CITY_7]

    DIRECTED_CONNECTION_1A = DirectedConnection(CITY_1, CITY_2, LENGTH, Color.RED)
    DIRECTED_CONNECTION_1B = DirectedConnection(CITY_2, CITY_1, LENGTH, Color.RED)
    DIRECTED_CONNECTION_2A = DirectedConnection(CITY_1, CITY_3, LENGTH, Color.RED)
    DIRECTED_CONNECTION_2B = DirectedConnection(CITY_3, CITY_1, LENGTH, Color.RED)
    DIRECTED_CONNECTION_3A = DirectedConnection(CITY_1, CITY_4, LENGTH, Color.RED)
    DIRECTED_CONNECTION_3B = DirectedConnection(CITY_4, CITY_1, LENGTH, Color.RED)
    DIRECTED_CONNECTION_4A = DirectedConnection(CITY_1, CITY_5, LENGTH, Color.RED)
    DIRECTED_CONNECTION_4B = DirectedConnection(CITY_5, CITY_1, LENGTH, Color.RED)
    DIRECTED_CONNECTION_5A = DirectedConnection(CITY_1, CITY_6, LENGTH, Color.RED)
    DIRECTED_CONNECTION_5B = DirectedConnection(CITY_6, CITY_1, LENGTH, Color.RED)
    DIRECTED_CONNECTION_6A = DirectedConnection(CITY_1, CITY_7, LENGTH, Color.RED)
    DIRECTED_CONNECTION_6B = DirectedConnection(CITY_7, CITY_1, LENGTH, Color.RED)

    DIRECETED_CONNECTION_LIST = [DIRECTED_CONNECTION_1A, DIRECTED_CONNECTION_1B,
                                DIRECTED_CONNECTION_2A, DIRECTED_CONNECTION_2B,
                                DIRECTED_CONNECTION_3A, DIRECTED_CONNECTION_3B,
                                DIRECTED_CONNECTION_4A, DIRECTED_CONNECTION_4B,
                                DIRECTED_CONNECTION_5A, DIRECTED_CONNECTION_5B,
                                DIRECTED_CONNECTION_6A, DIRECTED_CONNECTION_6B]
    

    def generate_map(self) -> Map:
        """
        Generates default map
        :return: the generated map
        """
        return Map(self.MAP_WIDTH, self.MAP_HEIGHT, self.CITY_LIST, self.DIRECETED_CONNECTION_LIST)