import json

from typing import TextIO

from trains.json.deserializers import deserialize_player_instances
from trains.json.serializers import serialize_rank
from trains.json_utils import (
    deserialize_colors, create_player_actors, build_visual_map, serialize_ranking
)
from trains.game.referee import RefereeActor
from trains.game.errors import NotEnoughDestinationsException
from trains.parsing import StatefulSpacedJSONParser


def xref(infile: TextIO, outfile: TextIO) -> None:
    """
    Testing task: https://www.ccs.neu.edu/home/matthias/4500-f21/8.html

    :param infile: input stream
    :param outfile: output stream
    """
    parser = StatefulSpacedJSONParser(infile.read())
    train_map = build_visual_map(parser.read_object()).get_map()
    player_actors = deserialize_player_instances(train_map, parser.read_array())
    colors = deserialize_colors(parser.read_array())

    try:
        ranking, cheaters = RefereeActor.run_game(player_actors, train_map, colors)
    except NotEnoughDestinationsException:
        outfile.write("error: not enough destinations")
        return

    out_data = [serialize_ranking(ranking), serialize_rank(cheaters)]

    json.dump(out_data, outfile)
