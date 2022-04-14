import json
import sys
from Trains.Other.json_utils import dict_to_map
from Trains.Editor.map_editor import display_map

TIMEOUT = 10000 # ms


def main():
    json_str = sys.stdin.read()
    json_dict = json.loads(json_str)
    train_map = dict_to_map(json_dict)
    display_map(train_map, TIMEOUT)


if __name__ == "__main__":
    main()
