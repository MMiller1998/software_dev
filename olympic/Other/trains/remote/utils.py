import asyncio
from typing import Callable

import json

from asyncio.streams import StreamWriter, StreamReader

from trains.remote.constants import ENCODING, MAX_MSG_SIZE
from trains.json.types import JSONValue
from trains.remote.remote_types import T


def identity(x: T) -> T:
    return x


def dump_encode_and_write_data(writer: StreamWriter, data: JSONValue) -> None:
    if data is None:
        encoded = 'void'.encode(ENCODING)
    else:
        encoded: bytes = json.dumps(data).encode(ENCODING)

    writer.write(encoded)


async def _read_message(reader: StreamReader) -> str:
    return (await reader.read(MAX_MSG_SIZE)).decode(ENCODING)


async def receive_message_and_deserialize(reader: StreamReader,
                                          deserializer: Callable[[JSONValue], T],
                                          timeout_time: int
                                          ) -> T:
    """
    :raises asyncio.exceptions.TimeoutError: if data doesn't come back in timeout_time seconds
    :raises: any exception from the deserializer
    """
    response = await asyncio.wait_for(_read_message(reader), timeout_time)

    if response != 'void':
        return deserializer(json.loads(response))
    return None
