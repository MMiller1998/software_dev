import asyncio
import threading
import time

from typing import TextIO, Optional

from trains.parsing import StatefulSpacedJSONParser
from trains.json.deserializers import deserialize_map, deserialize_player_instances
from trains.game.player import PlayerActor
from trains.remote.client import server_proxy


def run_client(
    host: str, port: int, player_actor: PlayerActor,
    max_retries: int = 3, loop: Optional[asyncio.AbstractEventLoop] = None
) -> None:
    """
    Run a server proxy. Retry connection if connection fails. Intended to be run
    from a separate thread.
    """
    if not loop:
        loop = asyncio.new_event_loop()

    try:
        loop.run_until_complete(server_proxy(host, port, player_actor))
        loop.close()
    except ConnectionRefusedError:
        if max_retries > 0:
            time.sleep(3)
            run_client(host, port, player_actor, max_retries=max_retries - 1, loop=loop)


def xclients(infile: TextIO, _: TextIO, port: int, host: str):
    parser = StatefulSpacedJSONParser(infile.read())
    train_map = deserialize_map(parser.read_object())
    player_actors = deserialize_player_instances(train_map, parser.read_array())
    _ = parser.read_array()  # array of Colors

    for player_actor in player_actors:
        thread = threading.Thread(target=run_client, args=(host, port, player_actor))
        thread.start()
