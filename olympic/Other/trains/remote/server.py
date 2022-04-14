import asyncio
from asyncio.events import AbstractEventLoop

from asyncio.streams import StreamReader, StreamWriter
from json.decoder import JSONDecodeError
from typing import List, Callable

from trains.remote.utils import receive_message_and_deserialize, identity
from trains.state.cardsholder import CardDeck
from trains.remote.remote_player_actor import RemotePlayerActor
from trains.remote.constants import MAX_MSG_SIZE
from trains.tournament.manager import TournamentManager
from trains.tournament.types import TournamentResult
from trains.tournament.constants import EMPTY_TOURNAMENT_RESULT

HOST = '127.0.0.1'

MAX_NUM_PLAYERS = 50
CLIENT_NAME_WAIT_SEC = 3
WAITING_PERIOD_WAIT_SEC = 20
WP1_MIN_NUM_PLAYERS = 5
WP2_MIN_NUM_PLAYERS = 2
MAX_PLAYER_NAME_LEN = 50  # characters


class TrainsServer:
    """
    Component to keep track of connected client metadata and transport information.
    """

    def __init__(self):
        self.clients: List[RemotePlayerActor] = []

    def add_client(self, name, reader, writer) -> None:
        self.clients.append(RemotePlayerActor(name, reader, writer))

    def check_signups(self, min_num_required: int, on_failure: Callable) -> None:
        """
        Check if we've gotten enough sign ups. If so then fire the `got_enough_signups` future. If not then
        execute the given on_failure function.
        If the `got_enough_signups` future has already been fired, then do nothing.
        """
        # TODO: This seems quite vulnerable to a race condition where the signup limit is hit
        #   and got_enough_signups gets set after the not .done() check happens but before
        #   we set the resuilt here...
        if self.got_enough_signups.done():
            return
        if len(self.clients) >= min_num_required:
            self.got_enough_signups.set_result(True)
        else:
            on_failure()

    def check_signups_after_wait_periods(self, loop: AbstractEventLoop) -> None:
        loop.call_later(
            WAITING_PERIOD_WAIT_SEC,
            self.check_signups,
            WP1_MIN_NUM_PLAYERS,
            lambda: loop.call_later(
                WAITING_PERIOD_WAIT_SEC,
                self.check_signups,
                WP2_MIN_NUM_PLAYERS,
                lambda: self.got_enough_signups.set_result(False)
            )
        )

    @staticmethod
    async def receive_client_name(reader: StreamReader) -> bytes:
        return await reader.read(MAX_MSG_SIZE)

    @staticmethod
    def validate_client_name(name: str) -> bool:
        """
        :return: `True` if the given name is valid, `False` otherwise
        """
        return len(name) <= MAX_PLAYER_NAME_LEN

    @staticmethod
    async def receive_and_validate_client_name(reader: StreamReader) -> str:
        name = await receive_message_and_deserialize(reader, identity, CLIENT_NAME_WAIT_SEC)

        if not TrainsServer.validate_client_name(name):
            raise ValueError('Client name was not valid')

        return name

    async def handle_client_connect(self, reader: StreamReader, writer: StreamWriter) -> None:
        """
        Wait for valid names to come over the wire. When one comes, create a `RemotePlayerActor`
        with the given name.
        """
        # if max number of players reached, drop the connection
        if len(self.clients) >= MAX_NUM_PLAYERS:
            writer.close()
            return

        try:
            name = await self.receive_and_validate_client_name(reader)
            self.add_client(name, reader, writer)

            if len(self.clients) >= MAX_NUM_PLAYERS:
                self.got_enough_signups.set_result(True)

        except (asyncio.exceptions.TimeoutError, ValueError, JSONDecodeError):
            # if a name was not sent, or was invalid, drop the connection
            writer.close()

    def accept_signups(self, loop: asyncio.AbstractEventLoop, port: int) -> bool:
        """
        Run the sign-up period of a tournament.

        :return: `True` if enough sign-ups were received, `False` otherwise
        """
        self.got_enough_signups = loop.create_future()

        self.check_signups_after_wait_periods(loop)

        async def start_signup_server() -> None:
            await asyncio.start_server(self.handle_client_connect, HOST, port)

        asyncio.ensure_future(start_signup_server())
        return loop.run_until_complete(self.got_enough_signups)

    def run_tournament(self, card_deck: CardDeck) -> TournamentResult:
        """
        Run a tournament. Must be called after the sign-up process has completed.
        """
        tm = TournamentManager(self.clients, card_deck)
        return tm.run_tournament()

    def close_remote_proxies(self) -> None:
        for client in self.clients:
            client.close_connection()

    @staticmethod
    def run_tournament_server(port: int, card_deck: CardDeck) -> TournamentResult:
        """
        Run the sign-up period of a Trains server, and if enough sign-ups are received,
        run the tournament. If not enough sign-ups are received, return an empty result.

        :raises NotEnoughDestinationsException: if the `TrainMap` selected for the tournament
            does not have enough destinations for all players in a game
        """
        loop = asyncio.get_event_loop()

        server = TrainsServer()
        enough_signups = server.accept_signups(loop, port)

        tournament_result = EMPTY_TOURNAMENT_RESULT
        if enough_signups:
            tournament_result = server.run_tournament(card_deck)

        server.close_remote_proxies()
        loop.close()

        return tournament_result
