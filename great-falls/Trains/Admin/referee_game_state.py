from collections import deque
from itertools import islice
from typing import List, Set, Deque, Tuple

from Trains.Common.map import Map
from Trains.Common.player_game_state import PlayerGameState
from Trains.Other.cards import Cards
from Trains.Other.color import Color
from Trains.Other.destination import Destination
from Trains.Other.directed_connection import DirectedConnection
from Trains.Other.interfaces.i_player import IPlayer
from Trains.Other.player_state import PrivatePlayerState
from Trains.Other.undirected_connection import UndirectedConnection


class RefereeGameState:
    """
    Represents the knowledge the referee has for a Trains game. All methods in the RefereeGameState assume that there
    is at least 1 player in the game.

    Args:
        map (Map): the map of the game
        states_and_players (Deque[Tuple[PrivatePlayerState, IPlayer]]: the private player states tupled with their
            player in turn order
        cards (List[Color]): the deck of colored cards the ref can give to players

    Attributes:
        __map (Map): the map of the game
        __states_and_players (Deque[Tuple[PrivatePlayerState, IPlayer]]): the private player states tupled with the owning
            Player
          The list rotates so the first element is always the player whose turn it is
        __cards (List[Color]): the deck of colored cards the ref can give to players
    """
    MIN_RAILS = 3
    CARDS_PER_REQUEST = 2
    __map: Map
    __states_and_players: Deque[Tuple[PrivatePlayerState, IPlayer]]

    def __init__(self, map: Map, states_and_players: Deque[Tuple[PrivatePlayerState, IPlayer]], cards: List[Color]):
        self.__map = map
        self.__states_and_players = states_and_players
        self.__cards = cards

    def __eq__(self, other):
        # ignore map, even though we shouldn't
        return isinstance(other, RefereeGameState) and \
               self.__states_and_players == other.__states_and_players and \
               self.__cards == other.__cards

    def __hash__(self):
        return hash((tuple(self.__cards), tuple(self.__states_and_players)))

    def get_players(self) -> List[IPlayer]:
        return [player_and_state[1] for player_and_state in self.__states_and_players]

    def get_current_player(self) -> IPlayer:
        return self.__states_and_players[0][1]

    def __get_player_states(self) -> List[PrivatePlayerState]:
        return [player_and_state[0] for player_and_state in self.__states_and_players]

    def create_player_game_state(self) -> PlayerGameState:
        """
        Constructs the game state of the currently active player.
        :return: a PlayerGameState for the active player
        """
        all_private_states = [player_and_state[0] for player_and_state in self.__states_and_players]
        own_state = self.__states_and_players[0][0]
        private_other_states = islice(all_private_states, 1, len(all_private_states))
        public_other_states = [player_state.public_state for player_state in private_other_states]

        return PlayerGameState(self.__map, own_state, public_other_states)

    def can_acquire_connection(self, connection: UndirectedConnection) -> bool:
        """
        Checks if the connection can be acquired based on the current state of the game
        :param connection: the connection to be acquired
        :return: whether the connection is acquirable
        """
        player_game_state = self.create_player_game_state()
        return connection in player_game_state.get_acquirable_connections()

    def acquire_connection(self, connection: UndirectedConnection) -> 'RefereeGameState':
        """
        Update the game state to acquire the given connection for the active player by removing the corresponding amount
        of cards and rails and add the connection to the player's acquired connections.
        This method assumes that the given connection is legal to acquire for the active player
        :param connection: connection to acquire
        :return: a new game state with the active player having purchased the connection
        """
        current_player_state = self.__states_and_players[0][0]
        new_player_state = current_player_state.buy_connection(connection)
        self.__states_and_players[0] = new_player_state, self.__states_and_players[0][1]
        return RefereeGameState(self.__map, self.__states_and_players, self.__cards)

    def reached_termination_condition(self) -> bool:
        """
        :return: whether the last player that went has reached the termination condition
        the termination condition is when a player has fewer rails than are necessary to purchase a connection
        """
        return self.__get_player_states()[-1].num_rails < self.MIN_RAILS

    def progress_turn(self) -> 'RefereeGameState':
        """
        Rotates the game state's list of players to move the current active player (index 0) to the back of the list
        :return: a new game state with the list of players rotated
        """
        new_states_and_players = deque(self.__states_and_players)
        new_states_and_players.rotate(-1)
        return RefereeGameState(self.__map, new_states_and_players, self.__cards)

    def remove_cheater(self) -> 'RefereeGameState':
        """
        Removes the current active player because it cheated
        :return: a new game state with the current player removed
        """
        self.__states_and_players.popleft()
        return RefereeGameState(self.__map, self.__states_and_players, self.__cards)

    def draw_cards(self, drawn_cards: List[Color]) -> 'RefereeGameState':
        """
        Add the drawn cards to the current active player
        :return: a new game state with the current player having received the drawn cards
        """
        remaining_cards = self.__cards[len(drawn_cards):]
        current_player_state = self.__states_and_players[0][0]
        new_player_state = current_player_state.draw_cards(Cards.from_list(drawn_cards))
        self.__states_and_players[0] = new_player_state, self.__states_and_players[0][1]
        return RefereeGameState(self.__map, self.__states_and_players, remaining_cards)

    def get_cards_to_draw(self) -> List[Color]:
        """
        :return: the cards to give to a player when they request cards
        """
        if len(self.__cards) >= self.CARDS_PER_REQUEST:
            drawn_cards = self.__cards[:self.CARDS_PER_REQUEST]
        else:
            drawn_cards = self.__cards.copy()
        return drawn_cards

    def count_scores(self) -> List[int]:
        """
        Computes the scores for each of the game's players. The player receives 1 point for each segment it acquired,
        10 points for each destination connected or -10 points for each destination not connected, and 20 points for
        holding the longest continuous path (which multiple players can have).
        :return: a list of scores, where the ordering mirrors the ordering of self.player_states
        """
        player_segment_counts = [self.__count_segment_score(player_state) for player_state in
                                 self.__get_player_states()]
        player_destination_scores = [self.__count_connected_destinations_score(player_state) for player_state in
                                     self.__get_player_states()]
        player_longest_path_scores = self.__count_longest_path_score()

        return [player_segment_counts[i] + player_destination_scores[i] + player_longest_path_scores[i] for i in
                range(len(player_segment_counts))]

    def __count_segment_score(self, player_state: PrivatePlayerState) -> int:
        """
        :param player_state: the player to compute the score for
        :return: the score for the player's acquired segments
        """
        acquired_connections_segment_count = map(lambda undirected_connection: undirected_connection.length,
                                                 player_state.public_state.acquired_connections)

        return sum(acquired_connections_segment_count)

    def __count_connected_destinations_score(self, player_state: PrivatePlayerState) -> int:
        """
        :param player_state: the player to compute the score for
        :return: the total score for the connections (or lack thereof) of the player's destinations
        """
        player_directed_connections = DirectedConnection.convert_undirected_connections(
            player_state.public_state.acquired_connections)
        player_destination_scores = map(
            lambda destination: self.__get_destination_score(destination, player_directed_connections),
            player_state.destinations)

        return sum(player_destination_scores)

    def __get_destination_score(self, destination: Destination,
                                acquired_directed_connections: Set[DirectedConnection]) -> int:
        """
        :param destination: the destination to check connection for
        :param acquired_directed_connections: the acquired connections
        :return: 10 if the destination is connected, -10 otherwise
        """
        if self.__map.are_cities_connected(destination.city_1, destination.city_2, acquired_directed_connections):
            return 10
        return -10

    def __count_longest_path_score(self) -> List[int]:
        """
        :return: a list of scores, where the player(s) who holds the longest continuous path has 20 and everyone else
        has 0. The ordering of this list mirrors the ordering of self.player_states
        """
        longest_continuous_path_per_player = [
            self.__map.longest_continuous_route(
                DirectedConnection.convert_undirected_connections(player.public_state.acquired_connections)) for
            player in self.__get_player_states()]
        longest_continuous_path = max(longest_continuous_path_per_player)
        return [20 if longest_continuous_path == player_longest_continuous_path else 0 for
                player_longest_continuous_path in longest_continuous_path_per_player]
