import asyncio

from asyncio.streams import StreamReader, StreamWriter
from typing import FrozenSet, Callable, List, Tuple

from trains.map import TrainMap
from trains.graph_elements import Destination
from trains.state.cardsholder import CardDeck
from trains.state.player import PlayerStateWrapper
from trains.state.action import ActionOption
from trains.game.player import PlayerActor
from trains.json.serializers import (
    serialize_train_map, serialize_card_deck, serialize_destinations, serialize_player_state_wrapper
)
from trains.json.deserializers import deserialize_map, deserialize_destinations, deserialize_action_option
from trains.json.types import JSONValue
from trains.remote.utils import identity, dump_encode_and_write_data, receive_message_and_deserialize
from trains.remote.remote_types import T

RESPONSE_WAIT_TIME = 2  # seconds to wait for response when calling client


class RemotePlayerActor(PlayerActor):
    """
    `PlayerActor` which communicates with remote client.
    """

    def __init__(self, name: str, reader: StreamReader, writer: StreamWriter):
        self.name = name
        self.reader = reader
        self.writer = writer

        self.train_map = None

    def _serialize_and_write(self, fn_name: str, args_and_serializers: List[Tuple[T, Callable[[T], JSONValue]]]) -> None:
        serialized_args = [serializer(data) for data, serializer in args_and_serializers]
        function_call_data = (fn_name, serialized_args)

        dump_encode_and_write_data(self.writer, function_call_data)

    def _receive_response_and_deserialize(self, deserializer: Callable[[JSONValue], T]) -> T:
        """
        :raises asyncio.exceptions.TimeoutError: if data doesn't come back in `RESPONSE_WAIT_TIME` seconds
        :raises: any exception from the deserializer
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(receive_message_and_deserialize(self.reader, deserializer, RESPONSE_WAIT_TIME))

    def close_connection(self) -> None:
        self.writer.close()

    # API for referee

    def setup(self, train_map: TrainMap, r: int, cards: CardDeck) -> None:
        self.train_map = train_map

        self._serialize_and_write(
            'setup',
            [(train_map, serialize_train_map), (r, identity), (cards, serialize_card_deck)]
        )
        return self._receive_response_and_deserialize(identity)

    def pick(self, destinations: FrozenSet[Destination]) -> FrozenSet[Destination]:
        self._serialize_and_write('pick', [(destinations, serialize_destinations)])
        return self._receive_response_and_deserialize(lambda data: deserialize_destinations(self.train_map, data))

    def play(self, state: PlayerStateWrapper) -> ActionOption:
        self._serialize_and_write('play', [(state, serialize_player_state_wrapper)])
        return self._receive_response_and_deserialize(lambda data: deserialize_action_option(self.train_map, data))

    def more(self, cards: CardDeck) -> None:
        self._serialize_and_write('more', [(cards, serialize_card_deck)])
        return self._receive_response_and_deserialize(identity)

    def win(self, won_game: bool) -> None:
        self._serialize_and_write('win', [(won_game, identity)])
        return self._receive_response_and_deserialize(identity)

    # API for manager

    def start(self, participating: bool) -> TrainMap:
        self._serialize_and_write('start', [(participating, identity)])
        return self._receive_response_and_deserialize(deserialize_map)

    def end(self, won_tournament: bool) -> None:
        self._serialize_and_write('end', [(won_tournament, identity)])
        return self._receive_response_and_deserialize(identity)
