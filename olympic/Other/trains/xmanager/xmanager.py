import json

from typing import TextIO

from trains.game.errors import NotEnoughDestinationsException
from trains.tournament.manager import TournamentManager
from trains.parsing import StatefulSpacedJSONParser

from trains.json.serializers import serialize_rank
from trains.json.deserializers import (
    deserialize_map, deserialize_player_instances, deserialize_colors
)


def xmanager(infile: TextIO, outfile: TextIO) -> None:
    """
    Testing task: https://www.ccs.neu.edu/home/matthias/4500-f21/9.html

    :param infile: input stream
    :param outfile: output stream
    """
    parser = StatefulSpacedJSONParser(infile.read())
    train_map = deserialize_map(parser.read_object())
    player_actors = deserialize_player_instances(train_map, parser.read_array())
    card_deck = deserialize_colors(parser.read_array())

    tm = TournamentManager(player_actors, card_deck)

    try:
        winners, cheaters = tm.run_tournament()
    except NotEnoughDestinationsException:
        outfile.write("error: not enough destinations")
        return

    out_data = [serialize_rank(winners), serialize_rank(cheaters)]

    json.dump(out_data, outfile)
