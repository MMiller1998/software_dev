import json
import sys

from Trains.Admin.referee import Referee
from Trains.Other import admin_utils
from Trains.Other.color import Color
from Trains.Other.json_utils import dict_to_map, get_next_json_value, array_to_players, serialize_game_result
from Trains.Other.ref_deck_strategies.given_deck_creation_strategy import GivenDeckCreationStrategy
from Trains.Other.ref_destination_options_strategies.lexi_sorted_destination_options_strategy import \
    LexiSortedDestinationOptionsStrategy


def main():
    json_str = sys.stdin.read()
    map_dict, json_str = get_next_json_value(json_str)
    player_instance_array, json_str = get_next_json_value(json_str)
    starting_deck_array, _ = get_next_json_value(json_str)
    map_obj = dict_to_map(map_dict)
    player_instances = array_to_players(player_instance_array)
    starting_deck = [Color(c) for c in starting_deck_array]
    deck_creation_strategy = GivenDeckCreationStrategy(starting_deck)
    destination_options_strategy = LexiSortedDestinationOptionsStrategy()
    try:
        game_result = Referee.run_game(map_obj, player_instances, admin_utils.STARTING_NUM_RAILS, deck_creation_strategy,
                                       destination_options_strategy)
        print(json.dumps(serialize_game_result(game_result)))
    except:
        print(json.dumps("error: not enough destinations"))


if __name__ == "__main__":
    main()
