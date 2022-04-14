import json
import sys
from Trains.Other.json_utils import dict_to_map, get_next_json_value, dict_to_player_states, \
    serialize_undirected_connection
from Trains.Common.player_game_state import PlayerGameState
from Trains.Player.hold_ten import HoldTenStrategy
from Trains.Other.undirected_connection import UndirectedConnection


def main():
    json_str = sys.stdin.read()
    map_dict, json_str = get_next_json_value(json_str)
    player_state_dict, json_str = get_next_json_value(json_str)
    map_obj = dict_to_map(map_dict)
    cities = map_obj.get_cities()
    private_player_state, public_states = dict_to_player_states(player_state_dict, cities)
    player_game_state = PlayerGameState(map_obj, private_player_state, public_states)
    turn_result = HoldTenStrategy.get_turn(player_game_state)
    if isinstance(turn_result, UndirectedConnection):
        print(json.dumps(serialize_undirected_connection(turn_result)))
    else:
        print(json.dumps("more cards"))


if __name__ == "__main__":
    main()
