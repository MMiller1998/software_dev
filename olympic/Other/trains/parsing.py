import json
import re

from asyncio.streams import StreamReader
from typing import Any, Optional

from trains.json.types import JSONValue
from trains.remote.constants import MAX_MSG_SIZE, ENCODING

FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)


class JSONStreamParser:

    def __init__(self, reader: StreamReader):
        self.reader = reader
        self._buffer = ''
        self._decoder = json.JSONDecoder()

    async def decode_next_value(self) -> Optional[JSONValue]:
        """
        Get and return the next JSON value from the stream, if one exists.
        If EOF has been reached on the stream, return `None`.
        """
        if not self._buffer:
            bytes_msg = await self.reader.read(MAX_MSG_SIZE)

            if not bytes_msg and self.reader.at_eof():
                return None

            self._buffer = bytes_msg.decode(ENCODING)

        return self._decode_from_buffer()

    def _decode_from_buffer(self) -> JSONValue:
        parsed, end = self._decoder.raw_decode(self._buffer)

        self._buffer = self._buffer[end:]
        m = re.match(WHITESPACE, self._buffer)
        self._buffer = self._buffer[m.end():]

        return parsed


class StatefulSpacedJSONParser:
    """
    A ``StatefulSpacedJSONParser`` processes :class:`str` data which is
    a sequence of well-formed, valid JSON separated by whitespace.

    Similar functionality to :meth:`json.JSONDecoder.raw_decode` but tolerates
    leading extraneous data in front of tokens.

    After calling a method, the "seek" position is advanced to the
    end of the token.
    """

    def __init__(self, data: str):
        """
        Constructor for ``StatefulSpacedJSONParser``.

        :param data: a sequence of well-formed, valid JSON separated by whitespace
        """
        self.__data = data
        self.__decoder = json.JSONDecoder()
        self.__idx = 0

    def __decode_next_something(self, char: str) -> Any:
        """
        Decode the next instance of a JSON.

        :param char: character which the next encoded JSON should start with
        :return: the next JSON, decoded
        """
        self.__idx = self.__data.find(char, self.__idx)
        token, self.__idx = self.__decoder.raw_decode(self.__data, idx=self.__idx)
        return token

    def read_string(self) -> str:
        """
        :return: the next string in the sequence of JSON data
        """
        return self.__decode_next_something('"')

    def read_object(self) -> dict:
        """
        :return: the next object in the sequence of JSON data
        """
        return self.__decode_next_something('{')

    def read_array(self) -> list:
        """
        :return: the next object in the sequence of JSON data
        """
        return self.__decode_next_something('[')
