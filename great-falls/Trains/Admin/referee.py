from collections import deque
from typing import Iterable, List, Set, Deque

from Trains.Admin.referee_game_state import RefereeGameState
from Trains.Common.map import Map
from Trains.Other.cards import Cards
from Trains.Other.color import Color
from Trains.Other.destination import Destination
from Trains.Other.game_result import GameResult
import Trains.Other.admin_utils as admin_utils
from Trains.Other.interfaces.i_player import IPlayer
from Trains.Other.interfaces.i_ref_deck_creation_strategy import IDeckCreationStrategy
from Trains.Other.interfaces.i_ref_destination_options_strategy import IDestinationOptionsStrategy
from Trains.Other.player_state import PrivatePlayerState, PublicPlayerState
from Trains.Other.ref_deck_strategies.random_deck_creation_strategy import RandomDeckCreationStrategy
from Trains.Other.ref_destination_options_strategies.random_destination_options_strategy import \
    RandomDestinationOptionsStrategy


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
        starting_rails_count (int): the number of rails each player gets. The default is 45
        deck_creation_strategy (IDeckCreationStrategy): a strategy for creating the referee's deck of 250 cards. The
                                                       default strategy is to randomly generate the deck
        destination_options_strategy (IDestinationOptionsStrategy): a strategy for ordering the destinations to present
                                                                   to the players. The default strategy is to randomly
                                                                   order the destinations

    Attributes:
        __trains_map (Map): the map for the Trains game
        __cheaters (List[IPlayer]): a list of cheaters who were kicked from the game
        __starting_rails_count (int): the number of rails each player gets
        __destination_options_strategy (IDestinationOptionsStrategy): a strategy for ordering the destinations to present
                                                                   to the players
        __deck_creation_strategy (IDeckCreationStrategy): a strategy for creating the referee's deck of 250 cards
        __game_state (Union[None, RefereeGameState]): the current state of the game from the ref's perspective. It is
                                                    initialized to None until the player's pick destinations
    """
    #todo: remove starting rails
    def __init__(self, trains_map: Map, starting_rails_count: int = admin_utils.STARTING_NUM_RAILS,
                 deck_creation_strategy: IDeckCreationStrategy = RandomDeckCreationStrategy(),
                 destination_options_strategy: IDestinationOptionsStrategy = RandomDestinationOptionsStrategy()):
        self.__trains_map = trains_map
        self.__cheaters = []
        self.__starting_rails_count = starting_rails_count
        self.__destination_options_strategy = destination_options_strategy
        self.__deck_creation_strategy = deck_creation_strategy
        self.__game_state = None

    @staticmethod
    def run_game(map: Map, players: List[IPlayer], starting_rails_count: int = admin_utils.STARTING_NUM_RAILS,
                 deck_creation_strategy: IDeckCreationStrategy = RandomDeckCreationStrategy(),
                 destination_options_strategy: IDestinationOptionsStrategy = RandomDestinationOptionsStrategy()) \
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
        referee = Referee(map, starting_rails_count, deck_creation_strategy, destination_options_strategy)
        valid_game = referee.__check_valid_game(map, players)
        if not valid_game:
            raise ValueError("Game was invalid")
        referee.setup_game(players)
        referee.run_turns()
        game_result = referee.end_game()

        return game_result

    def __remove_destinations(self, destinations: List[Destination], destinations_to_remove: Iterable[Destination]) -> \
            List[Destination]:
        """
        :param destinations: a list of destinations
        :param destinations_to_remove: the destinations to be removed
        :return given destinations list after removing the given destinations
        """
        return [destination for destination in destinations if destination not in destinations_to_remove]

    def setup_game(self, players: List[IPlayer]) -> None:
        """
        Setup a Trains game by giving all players their initial pieces and getting their destination choices.
        SIDE-EFFECTS:
            - Update self.game_state to the initial game state
            - Update cheater list with any cheating players
            - Side-effects from __setup_player
        :param players: a list of players in turn order
        """
        destinations = self.__generate_destination_ordering()
        final_states_and_players = []
        card_deck = self.__deck_creation_strategy.create_deck(admin_utils.STARTING_DECK_SIZE)
        for player in players:
            try:
                # todo: simplify try/except
                private_player_state, selected_destinations = self.__setup_player(player, destinations,
                                                                                  card_deck[:admin_utils.STARTING_NUM_CARDS])
                card_deck = card_deck[admin_utils.STARTING_NUM_CARDS:]
                destinations = self.__remove_destinations(destinations, selected_destinations)
                final_states_and_players.append((private_player_state, player))
            except:
                self.__cheaters.append(player)

        self.__game_state = RefereeGameState(self.__trains_map, deque(final_states_and_players), card_deck)

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
        previous_game_states = deque(maxlen=len(self.__game_state.get_players()) + 1)
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
        remaining_players = self.__game_state.get_players()
        if remaining_players:
            scores = self.__game_state.count_scores()
            game_result = GameResult(remaining_players, scores, self.__cheaters)
        else:
            game_result = GameResult([], [], self.__cheaters)

        game_winners = game_result.get_winners()
        #todo: handle errors from player
        for player in remaining_players:
            player.win(player in game_winners)

        return game_result

    def __setup_player(self, player: IPlayer, destinations: List[Destination], cards: List[Color]) \
            -> (PrivatePlayerState, List[Destination]):
        """
        Setup a given player for the game by passing them their initial pieces and getting their destination choices.
        :param player: the player to setup
        :param destinations: the destinations to pick from
        :param cards: the cards this player starts with
        :return: the player's state and the destinations it did not pick
        """
        player.setup(self.__trains_map, self.__starting_rails_count, cards)
        offered_destinations = destinations[:5]
        offered_destinations_set = set(offered_destinations)
        unwanted_destinations = player.pick(offered_destinations_set)
        self.__check_returned_destinations(unwanted_destinations, offered_destinations_set)
        picked_destinations = offered_destinations_set - unwanted_destinations
        return PrivatePlayerState(Cards.from_list(cards), picked_destinations, self.__starting_rails_count,
                                  PublicPlayerState(set())), self.__remove_destinations(offered_destinations,
                                                                                        unwanted_destinations)

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
            player_turn = self.__game_state.get_current_player().play(self.__game_state.create_player_game_state())
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
        :param player_turn: UndirectedConnection to acquire, or string "more cards" to request more cards
        :raises if the player attempts to make an illegal turn
        """
        if isinstance(player_turn, str):
            current_player = self.__game_state.get_current_player()
            drawn_cards = self.__game_state.get_cards_to_draw()
            self.__game_state = self.__game_state.draw_cards(drawn_cards)
            current_player.more_cards(drawn_cards)
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
        players = self.__game_state.get_players()
        has_played_at_least_one_round = len(previous_states) > len(players)
        return has_played_at_least_one_round and previous_states[0] == previous_states[len(players)]

    def __has_players(self) -> bool:
        return len(self.__game_state.get_players()) > 0

    def __run_final_round(self) -> None:
        """
        Runs a final round of the game for the remaining players (the player who triggered the termination condition
        is excluded)
        SIDE-EFFECTS:
            - Side-effects from __run_turn
        """
        for _ in range(len(self.__game_state.get_players()) - 1):
            self.__run_turn()

    def __progress_turn(self) -> None:
        """
        Progresses a turn using the RefereeGameState
        SIDE-EFFECTS:
            - Updates self.game_state with progressed turn
        """
        self.__game_state = self.__game_state.progress_turn()

    def __remove_cheater(self) -> None:
        """
        Removes the cheater (current player) from the game and adds them to the cheater list
        SIDE-EFFECTS:
            - Update self.players and self.cheaters accordingly to reflect a cheating turn
        """
        cheater = self.__game_state.get_current_player()
        self.__cheaters.append(cheater)
        self.__game_state = self.__game_state.remove_cheater()

    def __generate_destination_ordering(self) -> List[Destination]:
        destinations = self.__trains_map.get_feasible_destinations(admin_utils.STARTING_NUM_RAILS)
        return self.__destination_options_strategy.order_destinations(destinations)

    def __check_returned_destinations(self, returned_destinations: Set[Destination],
                                      offered_destinations: Set[Destination]) -> None:
        """
        Verifies that the returned destinations from a player all exist in the destinations offered to that player
        :param returned_destinations: destinations returned from the player
        :param offered_destinations: destinations offered to the player
        :raise IllegalTurnError: if any returned destination was not offered
        """
        if len(returned_destinations) != admin_utils.NUM_DESTINATIONS_RETURNED or \
                len(offered_destinations.intersection(returned_destinations)) != len(returned_destinations):
            raise IllegalTurnError("Did not receive valid destinations from player")

    def __check_valid_game(self, trains_map: Map, players: List[IPlayer]) -> bool:
        """
        A game is valid if:
            - the number of players falls within bounds
            - the map contains enough destinations to offer all players the same amount
        :param trains_map: the map to check
        :param players: the list of players playing the game
        :return: if the game is valid
        """
        enough_players = admin_utils.check_enough_players(len(players))
        enough_destinations = admin_utils.check_valid_map(trains_map, len(players))
        return enough_players and enough_destinations