import inspect
import json
import os
import sys
from typing import List, Dict, Union, Tuple
from Trains.Common.map import Map
from Trains.Other.game_result import GameResult
from Trains.Other.interfaces.i_player import IPlayer
from Trains.Other.player_state import PrivatePlayerState, PublicPlayerState
from Trains.Other.cards import Cards
from Trains.Other.city import City
from Trains.Other.destination import Destination
from Trains.Other.directed_connection import DirectedConnection
from Trains.Other.undirected_connection import UndirectedConnection
from Trains.Other.color import Color
from Trains.Player.player import Player


def get_next_json_value(json_str: str) -> (Union[str, Dict, List], str):
    """
    Gets the next JSON value from JSON value, returning a new string that has the extracted JSON value removed
    :param json_str: the string containing JSON values
    :return: the next JSON value and the json_str with the extracted JSON value removed
    """
    json_value, idx = json.JSONDecoder().raw_decode(json_str)
    return json_value, json_str[idx + 1:]


def dict_to_map(json_dict: Dict) -> Map:
    """
    :param json_dict: the dictionary containing all the information about the map
    :return: a Map constructed with the provided dimensions, cities, and connections
    """
    width = json_dict["width"]
    height = json_dict["height"]
    cities = [array_to_city(city_array) for city_array in json_dict["cities"]]
    directed_connections = _get_directed_connections(json_dict, cities)

    return Map(width, height, cities, directed_connections)


def dict_to_player_states(player_state_dict: Dict, cities: List[City]) -> \
        Tuple[PrivatePlayerState, List[PublicPlayerState]]:
    """
    :param player_state_dict: dictionary with field for "this" and "acquired" (see spec)
    :param cities: the list of cities in the map to verify all connections are valid
    :return: a PrivatePlayerState and a list of PublicPlayerState from a "PlayerState" (see spec)
    """
    other_player_states = [array_to_public_state(player_array, cities) for player_array in
                           player_state_dict["acquired"]]

    return dict_to_private_player_state(player_state_dict["this"], cities), other_player_states


def dict_to_private_player_state(private_player_state_dict: Dict, cities: List[City]) -> PrivatePlayerState:
    """
    :param private_player_state_dict: dict with fields for 2 destinations, rails, cards, and acquired connections
    :param cities: the list of cities in the map to verify all connections are valid
    :return: a PrivatePlayerState from a "ThisPlayer" (see spec)
    """
    destination_1 = array_to_destination(private_player_state_dict["destination1"], cities)
    destination_2 = array_to_destination(private_player_state_dict["destination2"], cities)
    rails = private_player_state_dict["rails"]
    cards = dict_to_cards(private_player_state_dict["cards"])
    public_player_state = array_to_public_state(private_player_state_dict["acquired"], cities)
    return PrivatePlayerState(cards, {destination_1, destination_2}, rails, public_player_state)


def array_to_destination(destination_array: List, cities: List[City]) -> Destination:
    """
    :param destination_array: array containing two names
    :param cities: the list of cities in the map to verify all connections are valid
    :return: a Destination from a "Destination" (see spec)
    """
    return Destination(find_city(cities, destination_array[0]), find_city(cities, destination_array[1]))


def array_to_city(city_array: List) -> City:
    """
    :param city_array: array containing name, and an array of coordinates
    :return: a City from a "City" (see spec)
    """
    return City(city_array[0], (city_array[1][0], city_array[1][1]))


def dict_to_cards(cards_dict: Dict) -> Cards:
    """
    :param cards_dict: a dict from a string representing color to the amount of cards of that color
    :return: a Cards from a "Card*" (see spec)
    """
    cards_dict_with_colors = {Color(color_str): card_count for color_str, card_count in cards_dict.items()}
    return Cards(cards_dict_with_colors)


def array_to_public_state(public_state_array: List, cities: List[City]) -> PublicPlayerState:
    """
    :param public_state_array: an array containing a player's acquired connections
    :param cities: the list of cities in the map to verify all connections are valid
    :return: a PublicPlayerState from a "Player" (see spec)
    """
    return PublicPlayerState({array_to_undirected_connection(connection, cities) for connection in public_state_array})


def array_to_undirected_connection(connection_array: List, cities: List[City]) -> UndirectedConnection:
    """
    :param connection_array: an array containing two city names, a length, and a color
    :param cities: the list of cities in the map to verify all connections are valid
    :return: an UndirectedConnection from an "Acquired" (see spec)
    """
    return UndirectedConnection(find_city(cities, connection_array[0]),
                                find_city(cities, connection_array[1]),
                                connection_array[3],
                                Color(connection_array[2]))


def array_to_players(player_array: List[List]) -> List[IPlayer]:
    """
    :param player_array: an array containing arrays of name and desired strategy
    :return: a list of players from a list of "PlayerInstance" (see spec)
    """
    return [array_to_player(player_instance) for player_instance in player_array]


def array_to_player(player_instance: List) -> IPlayer:
    """
    :param player_instance: an array containing a name and strategy
    :return: a Player from a "PlayerInstance" (see spec)
    """
    strategy_file_path = _get_strategy_file_path(player_instance[1])
    return Player.player_from_strategy_file(strategy_file_path, player_instance[0])


def find_city(cities: List[City], city_name: str):
    """
    :param cities: list of City's in the map
    :param city_name: name of the city that is being looked up
    :return: the City in the list with the matching city name
    """
    return [city for city in cities if city.name == city_name][0]


def _get_strategy_file_path(strategy_to_use: str):
    """
    :param strategy_to_use: the string representing the desired strategy
    :return: an absolute path to the desired strategy
    """
    rel_path_to_strategy = '../Player/'
    if strategy_to_use == "Hold-10":
        rel_path_to_strategy += 'hold_ten.py'
    elif strategy_to_use == "Buy-Now":
        rel_path_to_strategy += '../Player/buy_now.py'
    elif strategy_to_use == "Cheat":
        rel_path_to_strategy += '../Player/cheat.py'
    return _abs_path_to_file(rel_path_to_strategy)

def _abs_path_to_file(filename):
    """
    :param filename: a path to a file relative to the parent directory of this file
    :return: the absolute path to the given file
    """
    return os.path.abspath(os.path.join(os.path.dirname(inspect.getfile(sys._getframe(1))), filename))


def _get_directed_connections(json_dict: Dict, cities: List[City]) -> List[DirectedConnection]:
    """
    :param json_dict: a dict representing a map
    :param cities: the list of cities in the map to verify all connections are valid
    :return: a list of DirectedConnection from "Connections" (see spec)
    """
    directed_connections = []
    for origin_name, target in json_dict["connections"].items():
        for destination_name, segment in target.items():
            for color, length in segment.items():
                origin_city = find_city(cities, origin_name)
                destination_city = find_city(cities, destination_name)
                directed_connections.append(DirectedConnection(origin_city, destination_city,
                                                               int(length), Color(color)))
                directed_connections.append(DirectedConnection(destination_city, origin_city,
                                                               int(length), Color(color)))

    return directed_connections


def serialize_undirected_connection(connection: UndirectedConnection) -> List:
    """
    :param connection: the undirected connection to serialize
    :return: a json array representing an Acquired (see spec)
    """
    return [connection.get_city_1().name, connection.get_city_2().name, connection.color.value, connection.length]


def serialize_game_result(game_result: GameResult) -> List:
    """
    :param game_result: the game result to serialize
    :return: a json array containing a Ranking and a Rank (see spec)
    """
    rankings = game_result.get_rankings()
    internally_sorted_rankings = []
    for players_with_ranking in rankings:
        internally_sorted_rankings.append(sorted([player.name for player in players_with_ranking]))
    cheaters_list = sorted([cheater.name for cheater in game_result.get_cheaters()])
    return [internally_sorted_rankings, cheaters_list]
