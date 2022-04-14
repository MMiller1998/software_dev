from Trains.Common.map import Map

NUM_DESTINATION_OPTIONS = 5
NUM_DESTINATIONS_RETURNED = 3
STARTING_DECK_SIZE = 250
STARTING_NUM_RAILS = 45
STARTING_NUM_CARDS = 4
MIN_NUM_PLAYERS = 2
MAX_NUM_PLAYERS = 8

def check_valid_map(trains_map: Map, num_players: int) -> bool:
    """
    :param trains_map: the map to check
    :param num_players: number of players that would play a game with this map
    :return: whether the map contains enough destinations to offer all players the same amount
    """
    num_feasible_destinations = len(trains_map.get_feasible_destinations(STARTING_NUM_RAILS))
    return num_feasible_destinations >= _get_min_num_destinations(num_players)

def _get_min_num_destinations(num_players):
    num_destinations_selected = NUM_DESTINATION_OPTIONS - NUM_DESTINATIONS_RETURNED
    return num_destinations_selected * num_players + NUM_DESTINATIONS_RETURNED

def check_enough_players(num_players: int) -> bool:
    """
    :param num_players: number of players
    :return: whether there are enough players to play a single game
    """
    return MIN_NUM_PLAYERS <= num_players <= MAX_NUM_PLAYERS