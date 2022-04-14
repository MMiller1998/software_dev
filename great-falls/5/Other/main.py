import json
import sys
from Trains.Other.json_utils import  dict_to_map, get_next_json_value, dict_to_player_states, array_to_undirected_connection
from Trains.Common.player_game_state import PlayerGameState

DEFAULT_NUM_STARTING_RAILS = 45


def main():
    json_str = sys.stdin.read()
    map_dict, json_str = get_next_json_value(json_str)
    player_state_dict, json_str = get_next_json_value(json_str)
    acquired_array, _ = get_next_json_value(json_str)
    map_obj = dict_to_map(map_dict)
    cities = map_obj.get_cities()
    private_player_state, public_states = dict_to_player_states(player_state_dict, cities)
    connection_to_acquire = array_to_undirected_connection(acquired_array, cities)
    player_game_state = PlayerGameState(map_obj, private_player_state, public_states)
    can_acquire_connection = connection_to_acquire in player_game_state.get_acquirable_connections()
    print(json.dumps(can_acquire_connection))


if __name__ == "__main__":
    main()
