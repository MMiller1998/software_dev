from collections import deque
from typing import List, Set, Deque

from Trains.Admin.referee_game_state import RefereeGameState
from Trains.Common.map import Map
from Trains.Other.cards import Cards
from Trains.Other.color import Color
from Trains.Other.destination import Destination
from Trains.Other.game_result import GameResult
from Trains.Other.player_state import PrivatePlayerState, PublicPlayerState
from Trains.Other.ref_deck_creation_strategy import DeckCreationStrategy, RandomDeckCreationStrategy
from Trains.Other.ref_destination_options_strategy import DestinationOptionsStrategy, RandomDestinationOptionsStrategy
from Trains.Player.player import Player


class IllegalTurnError(Exception):
    """
    An exception representing an attempted illegal turn.
    """
    pass


class Referee:
    """
    Represents a referee for the Trains game. This class is responsible for running a Trains game.

    The Referee handles any exceptions that may arise when it is expecting a response from a Player (play and pick).
    This already extends to any remote functionality we may need in the future, so assuming issues that arise from
    remote communication all go through the player methods and throw errors, we currently handle them.
    Although a Player could throw an exception on void methods, when this moves to a remote connection, this will not be
    an issue, so the Referee does not handle it currently. The Referee also handles illegal turns, such as acquiring a
    connection that does not exist or invalid return destinations.

    Args:
        trains_map (Map): the map for the Trains game
        ordered_players (List[Player]): a list, ordered by age, of all players for a game
        starting_rails_count (int): the number of rails each player gets. The default is 45
        deck_creation_strategy (DeckCreationStrategy): a strategy for creating the referee's deck of 250 cards. The
                                                       default strategy is to randomly generate the deck
        destination_options_strategy (DestinationOptionsStrategy): a strategy for ordering the destinations to present
                                                                   to the players. The default strategy is to randomly
                                                                   order the destinations

    Attributes:
        __trains_map (Map): the map for the Trains game
        __players (Deque[Player]): a list, ordered by age, of all players for a game
        __cheaters (List[Player]): a list of cheaters who were kicked from the game
        __starting_rails_count (int): the number of rails each player gets
        __destination_options_strategy (DestinationOptionsStrategy): a strategy for ordering the destinations to present
                                                                   to the players
        __deck_creation_strategy (DeckCreationStrategy): a strategy for creating the referee's deck of 250 cards
        __cards (List[Color]): the ref's deck of cards
        __game_state (Union[None, RefereeGameState]): the current state of the game from the ref's perspective. It is
                                                    initialized to None until the player's pick destinations
    """
    NUM_DESTINATION_OPTIONS = 5
    STARTING_DECK_SIZE = 250
    STARTING_NUM_RAILS = 45
    STARTING_NUM_CARDS = 4
    CARDS_PER_REQUEST = 3

    def __init__(self, trains_map: Map, ordered_players: List[Player], starting_rails_count: int = STARTING_NUM_RAILS,
                 deck_creation_strategy: DeckCreationStrategy = RandomDeckCreationStrategy(),
                 destination_options_strategy: DestinationOptionsStrategy = RandomDestinationOptionsStrategy()):
        """
        :raises if the number of players is not between 2 and 8 inclusive
        """
        if not 2 <= len(ordered_players) <= 8:
            raise ValueError("Must have between 2 and 8 players (inclusive)")

        self.__trains_map = trains_map
        self.__players = deque(ordered_players)
        self.__cheaters = []
        self.__starting_rails_count = starting_rails_count
        self.__destination_options_strategy = destination_options_strategy
        self.__cards = deck_creation_strategy.create_deck(self.STARTING_DECK_SIZE)
        self.__game_state = None

    @staticmethod
    def run_game(map: Map, players: List[Player], starting_rails_count: int = STARTING_NUM_RAILS,
                 deck_creation_strategy: DeckCreationStrategy = RandomDeckCreationStrategy(),
                 destination_options_strategy: DestinationOptionsStrategy = RandomDestinationOptionsStrategy()) \
            -> GameResult:
        """
        Run an entire Trains game with the given map and players
        :param map: the map for the game
        :param players: a list of players ordered by age
        :param starting_rails_count: the starting number of rails each player gets
        :param deck_creation_strategy: the creation strategy for a deck
        :param destination_options_strategy: the destination option strategy
        :return: a result for the game
        """
        referee = Referee(map, players, starting_rails_count, deck_creation_strategy, destination_options_strategy)
        referee.setup_game()
        referee.run_turns()
        game_result = referee.end_game()

        return game_result

    def setup_game(self) -> None:
        """
        Setup a Trains game by giving all players their initial pieces and getting their destination choices.
        SIDE-EFFECT:
            - Update self.game_state to the initial game state
            - Side-effects from __setup_player
            - Side-effects from __remove_cheater
        """
        destinations = self.__generate_destination_ordering()
        private_player_states = []
        for player in self.__players:
            try:
                #todo: find a way to know the ordering of this destination list
                #todo: simplify try/except
                private_player_state, returned_destinations = self.__setup_player(player, destinations)
                destinations = list(returned_destinations) + destinations[5:]
                private_player_states.append(private_player_state)
            except:
                self.__remove_cheater()

        self.__game_state = RefereeGameState(self.__trains_map, private_player_states)

    def run_turns(self) -> None:
        """
        Play out turns in player order until either:
            - The termination condition is reached (a player has less than 3 rails)
            - The game state has not changed for an entire round of turns
            - The game has no more players
        If the termination condition is reached, all other players are granted one more turn.
        SIDE-EFFECTS:
            - Side-effects from __run_turn
            - Side-effects from __run_final_round
        """
        previous_game_states = deque(maxlen=len(self.__players) + 1)
        while self.__should_continue_turns(previous_game_states):
            successful_turn = self.__run_turn()
            if successful_turn:
                previous_game_states.appendleft(self.__game_state)
        if self.__has_players() and self.__game_state.reached_termination_condition():
            self.__run_final_round()

    def end_game(self) -> GameResult:
        """
        End the game by computing player scores and ranking them. Notify each player of whether they won or not.
        :return: the game's result
        """
        if self.__players:
            scores = self.__game_state.count_scores()
            game_result = GameResult(list(self.__players), scores, self.__cheaters)
        else:
            game_result = GameResult([], [], self.__cheaters)

        game_winners = game_result.get_winners()
        for player in list(self.__players):
            player.win(player in game_winners)

        return game_result

    def __setup_player(self, player: Player, destinations: List[Destination]) -> (PrivatePlayerState, Set[Destination]):
        """
        Setup a given player for the game by passing them their initial pieces and getting their destination choices.
        SIDE-EFFECTS:
            - Side-effects from __draw_cards
        :param player: the player to setup
        :param destinations: the destinations to pick from
        :return: the player's state and the destinations it did not pick
        """
        drawn_cards = self.__draw_cards(self.STARTING_NUM_CARDS)
        player.setup(self.__trains_map, self.__starting_rails_count, drawn_cards)
        offered_destinations = set(destinations[:5])
        returned_destinations = player.pick(offered_destinations)
        self.__check_returned_destinations(returned_destinations, offered_destinations)
        picked_destinations = offered_destinations - returned_destinations
        return PrivatePlayerState(Cards.from_list(drawn_cards), picked_destinations, self.__starting_rails_count,
                                  PublicPlayerState(set())), returned_destinations

    def __should_continue_turns(self, previous_game_states: Deque[RefereeGameState]) -> bool:
        """
        :param previous_game_states: a deque of the previous game states whose length is always capped at the original
                                     size of self.players
        :return: whether any of the conditions mentioned in run_turns are met
        """
        return self.__has_players() and \
               not self.__game_state.reached_termination_condition() and \
               not self.__stale_state(previous_game_states)


    def __run_turn(self) -> bool:
        """
        Gets the current active player's turn and execute it. After the game state is updated, rotate the player list
        to progress the turn. This method assumes the game has at least one player
        SIDE-EFFECTS:
            - Side-effects from __progress_turn
            - Side-effects from __perform_player_turn
            - Side-effects from __remove_cheater
        :return: whether the turn was successful (aka whether the player's turn was legal)
        """
        try:
            player_turn = self.__players[0].play(self.__game_state.create_player_game_state())
            self.__perform_player_turn(player_turn)
            self.__progress_turn()
            return True
        except:
            self.__remove_cheater()
            return False

    def __perform_player_turn(self, player_turn) -> None:
        """
        Executes a player's turn and updates the game state with the result.
        SIDE-EFFECTS:
            - Updates self.game_state with the player's turn
            - Side-effects from __draw_cards
        :param player_turn: UndirectedConnection to acquire, or string "more cards" to request more cards
        :raises if the player attempts to make an illegal turn
        """
        if isinstance(player_turn, str):
            drawn_cards = self.__draw_cards(self.CARDS_PER_REQUEST)
            self.__game_state = self.__game_state.draw_cards(Cards.from_list(drawn_cards))
        else:
            if not self.__game_state.can_acquire_connection(player_turn):
                raise IllegalTurnError("Current player attempting to illegally acquire a connection")

            self.__game_state = self.__game_state.acquire_connection(player_turn)

    def __stale_state(self, previous_states: Deque[RefereeGameState]) -> bool:
        """
        :param previous_states: a deque of the previous game states whose length is always capped at the original
                                size of self.players
        :return: whether the game state has not changed for an entire round of players
        """
        has_played_at_least_one_round = len(previous_states) > len(self.__players)
        return has_played_at_least_one_round and previous_states[0] == previous_states[len(self.__players)]

    def __has_players(self) -> bool:
        return len(self.__players) > 0

    def __run_final_round(self) -> None:
        """
        Runs a final round of the game for the remaining players (the player who triggered the termination condition
        is excluded)
        SIDE-EFFECTS:
            - Side-effects from __run_turn
        """
        for _ in range(len(self.__players) - 1):
            self.__run_turn()

    def __progress_turn(self) -> None:
        """
        Progresses a turn by moving the current player to the end of the list.
        SIDE-EFFECTS:
            - Rotate self.players list to progress the turn
            - Updates self.game_state with progressed turn
        """
        self.__players.rotate(-1)
        self.__game_state = self.__game_state.progress_turn()

    def __remove_cheater(self) -> None:
        """
        Removes the cheater (current player) from the game and adds them to the cheater list
        SIDE-EFFECTS:
            - Update self.players and self.cheaters accordingly to reflect a cheating turn
        """
        cheater = self.__players.popleft()
        self.__cheaters.append(cheater)
        self.__game_state = self.__game_state.remove_cheater()

    def __generate_destination_ordering(self) -> List[Destination]:
        destinations = self.__trains_map.get_feasible_destinations(self.STARTING_NUM_RAILS)
        return self.__destination_options_strategy.order_destinations(destinations)

    def __draw_cards(self, num_cards_to_draw: int) -> List[Color]:
        """
        Draws the given number of cards from the deck.
        SIDE-EFFECTS:
            - Remove n elements from the front of the deck, where n is the number of cards to draw
        :param num_cards_to_draw: number of cards to draw
        :return: a list of cards drawn
        """
        if len(self.__cards) < num_cards_to_draw:
            drawn_cards = self.__cards.copy()
            self.__cards = []
            return drawn_cards

        drawn_cards = self.__cards[:num_cards_to_draw]
        self.__cards = self.__cards[num_cards_to_draw:]
        return drawn_cards

    def __check_returned_destinations(self, returned_destinations: Set[Destination],
                                      offered_destinations: Set[Destination]) -> None:
        """
        Verifies that the returned destinations from a player all exist in the destinations offered to that player
        :param returned_destinations: destinations returned from the player
        :param offered_destinations: destinations offered to the player
        :raise IllegalTurnError: if any returned destination was not offered
        """
        if len(returned_destinations) != 3 or \
                len(offered_destinations.intersection(returned_destinations)) != len(returned_destinations):
            raise IllegalTurnError("Did not receive valid destinations from player")
