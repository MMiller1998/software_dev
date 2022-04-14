import asyncio

from typing import Iterable, Callable, Tuple
from trains.remote.remote_types import T

from trains.parsing import JSONStreamParser
from trains.json.types import JSONValue
from trains.json.serializers import serialize_train_map, serialize_destinations, serialize_action
from trains.json.deserializers import (
    deserialize_map, deserialize_colors, deserialize_destinations,
    deserialize_player_state
)
from trains.game.player import PlayerActor
from trains.remote.utils import identity, dump_encode_and_write_data


async def server_proxy(host: str, port: int, player_actor: PlayerActor) -> None:
    """
    Connect to a Trains server. Wait for remote proxy calls, upon which call the
    real method on the given `player_actor`, and send back its result, serialized
    and encoded.
    """
    reader, writer = await asyncio.open_connection(host, port)
    dump_encode_and_write_data(writer, player_actor.name)
    await writer.drain()

    parser = JSONStreamParser(reader)

    # Due to the way certain data is structured, being able to deserialize
    # these structures requires a TrainMap to be passed as well. For this reason,
    # the TrainMap passed to the start method gets stored here and passed to
    # deserializers as needed
    train_map = None

    while True:
        msg = await parser.decode_next_value()

        if msg is None:
            break

        fn_name, args = msg
        serialized_result: JSONValue = None

        if fn_name == 'start':
            train_map = deserialize_and_execute(player_actor.start, zip(args, [identity]))
            serialized_result = serialize_train_map(train_map)

        elif fn_name == 'end':
            serialized_result = deserialize_and_execute(player_actor.end, zip(args, [identity]))

        elif fn_name == 'setup':
            serialized_result = deserialize_and_execute(
                player_actor.setup,
                zip(args, [deserialize_map, identity, deserialize_colors])
            )

        elif fn_name == 'play':
            action_option = deserialize_and_execute(
                player_actor.play,
                zip(args, [lambda data: deserialize_player_state(train_map, data)])
            )
            serialized_result = serialize_action(action_option)

        elif fn_name == 'pick':
            unpicked_destinations = deserialize_and_execute(
                player_actor.pick,
                zip(args, [lambda data: deserialize_destinations(train_map, data)])
            )
            serialized_result = serialize_destinations(unpicked_destinations)

        elif fn_name == 'more':
            serialized_result = deserialize_and_execute(player_actor.more, zip(args, [deserialize_colors]))

        elif fn_name == 'win':
            serialized_result = deserialize_and_execute(player_actor.more, zip(args, [identity]))

        else:
            raise NotImplementedError(f"don't know what to do with fn_name {fn_name}")

        dump_encode_and_write_data(writer, serialized_result)

    writer.close()


def deserialize_and_execute(func: Callable,
                            args_and_deserializers: Iterable[Tuple[JSONValue, Callable[[JSONValue], T]]]) -> any:
    """
    Deserialize the arguments given, then call `func` with those arguments. Returns the result of `func`
    """
    deserialized_data = [deserializer(data) for data, deserializer in args_and_deserializers]
    return func(*deserialized_data)
