import sys
import json
from Trains.Other.json_utils import  dict_to_map, find_city, get_next_json_value
from Trains.Other.destination import Destination

DEFAULT_NUM_STARTING_RAILS = 45


def main():
    json_str = sys.stdin.read()
    city_1_name, json_str = get_next_json_value(json_str)
    city_2_name, json_str = get_next_json_value(json_str)
    map_json, _ = get_next_json_value(json_str)
    map_obj = dict_to_map(map_json)
    cities = map_obj.get_cities()
    city_1 = find_city(cities, city_1_name)
    city_2 = find_city(cities, city_2_name)
    feasible_destinations = map_obj.get_feasible_destinations(DEFAULT_NUM_STARTING_RAILS)
    is_feasible = Destination(city_1, city_2) in feasible_destinations
    print(json.dumps(is_feasible))


if __name__ == "__main__":
    main()
