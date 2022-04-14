import json

from typing import TextIO

from trains.parsing import StatefulSpacedJSONParser
from trains.remote.server import TrainsServer
from trains.json.serializers import serialize_tournament_result
from trains.json.deserializers import deserialize_colors
from trains.game.errors import NotEnoughDestinationsException


def xserver(infile: TextIO, outfile: TextIO, port: int) -> None:
    """
    Runnables task: https://www.ccs.neu.edu/home/matthias/4500-f21/10.html

    :param infile: input stream
    :param outfile: output stream
    :param port: the port to listen for TCP connections on
    """
    parser = StatefulSpacedJSONParser(infile.read())
    _ = parser.read_object()  # Map
    _ = parser.read_array()  # array of PlayerInstance
    colors = deserialize_colors(parser.read_array())

    try:
        tournament_result = TrainsServer.run_tournament_server(port, colors)
    except NotEnoughDestinationsException:
        json.dump('error: not enough destinations', outfile)
        return

    out_data = serialize_tournament_result(tournament_result)
    json.dump(out_data, outfile)
