from typing import Callable, List, Tuple, Set, Iterable, Optional

from trains.map import TrainMap
from trains.utils import safe_player_call, MethodStatus
from trains.graph_elements import Destination
from trains.game.player import PlayerActor
from trains.game.referee import RefereeActor
from trains.game.constants import MIN_PLAYERS_IN_GAME, MAX_PLAYERS_IN_GAME
from trains.tournament.types import TournamentResult
from trains.state.cardsholder import CardDeck
from trains.strategy.lexico import lexicographically_sorted_destinations


def choose_first_map(map_options: List[TrainMap]) -> Optional[TrainMap]:
    """
    Choose the first map out of the given iterator.
    Returns `None` if `map_options` is empty.
    """
    if map_options:
        return map_options[0]
    return None

class TournamentManager:

    def __init__(
        self, players: List[PlayerActor], card_deck: CardDeck,
        dest_sorting_func: Callable[[Iterable[Destination]], List[Destination]] = lexicographically_sorted_destinations,
        map_chooser: Callable[[List[TrainMap]], TrainMap] = choose_first_map
    ):
        self.current_players: List[PlayerActor] = players
        self.cheaters: Set[PlayerActor] = set()
        self.previous_round_winners: Set[PlayerActor] = set()

        self.card_deck = card_deck
        self.map_chooser = map_chooser
        self.dest_sorting_func = dest_sorting_func

        self.train_map = None

        self.final_game_flag = False

    def run_tournament(self) -> TournamentResult:
        """
        Run a tournament. See https://www.ccs.neu.edu/home/matthias/4500-f21/8.html.
        """
        self.train_map = self.start_up()
        # While self.train_map could be None here, if that is the case, all players are
        # cheaters, and termination happens immediately.

        while not self.stop_condition_reached():
            player_allocations = self.allocate_players()
            if len(player_allocations) == 1:
                self.final_game_flag = True

            round_winners, round_cheaters = self.steady_state(player_allocations)

            self.cheaters = self.cheaters.union(round_cheaters)
            self.previous_round_winners = set(self.current_players)
            self.current_players = round_winners

        self.termination()

        return set(self.current_players), self.cheaters

    def start_up(self) -> Optional[TrainMap]:
        """
        Start up phase of a tournament. Informs participating players that the
        tournament is starting and selects a map from the returned options.

        If all players fail to provide a valid map, this method returns None.
        """
        map_options = []
        start_cheaters = set()

        for player in self.current_players:
            result = safe_player_call(lambda: player.start(True))

            if result == MethodStatus.ERROR:
                start_cheaters.add(player)
            else:
                player_map = result[1]
                map_options.append(player_map)

        for cheater in start_cheaters:
            self._remove_cheater(cheater)

        return self.map_chooser(map_options)

    def _remove_cheater(self, cheater: PlayerActor) -> None:
        """
        :raises ValueError: if `cheater` is not a currently active player
        """
        if cheater not in self.current_players:
            raise ValueError(f'cannot remove cheater {cheater}, not a currently active player')

        self.current_players.remove(cheater)
        self.cheaters.add(cheater)


    def steady_state(self, player_allocations: List[List[PlayerActor]]) -> Tuple[List[PlayerActor], Set[PlayerActor]]:
        """
        Run a round of the tournament.

        :param player_allocations: a grouping of which players will play a game together
        :return: a set of players who won this round, and a set of cheaters from this round
        """
        round_winners = []
        round_cheaters = []

        for players in player_allocations:
            ranking, cheaters = RefereeActor.run_game(players, self.train_map, self.card_deck.copy(), dest_sorting_func=self.dest_sorting_func)

            if ranking:
                round_winners += ranking[0]
            round_cheaters += cheaters

        # TODO: Need to sort the winners across games...how does that work?
        return round_winners, set(round_cheaters)

    def stop_condition_reached(self) -> bool:
        return (
            set(self.current_players) == self.previous_round_winners
            or len(self.current_players) < MIN_PLAYERS_IN_GAME
            or self.final_game_flag
        )

    def termination(self) -> None:
        """
        Notify players whether they won or lost.
        This should only be called once the tournament has concluded.
        """
        # TODO: Wrap calls
        for pa in self.current_players:
            result = safe_player_call(lambda: pa.end(True))

            if result == MethodStatus.ERROR:
                self._remove_cheater(pa)

        for pa in set(self.current_players) - self.cheaters:
            result = safe_player_call(lambda: pa.end(False))

            if result == MethodStatus.ERROR:
                self._remove_cheater(pa)

    def allocate_players(self) -> List[List[PlayerActor]]:
        """
        Group current players into a new round of games.

        :return: a grouping of players such that each group should play a game in the round
        """
        return self._allocate_players_helper([], self.current_players, MAX_PLAYERS_IN_GAME)

    @classmethod
    def _allocate_players_helper(
        cls,
        current_allocation: List[List[PlayerActor]],
        remaining_players: List[PlayerActor],
        game_size_to_try: int
    ) -> List[List[PlayerActor]]:
        """
        CONSTRAINT: len(remaning_players) must start as at least MIN_PLAYERS_IN_GAME
        """
        # Base case: enough players for final game
        if MIN_PLAYERS_IN_GAME <= len(remaining_players) <= game_size_to_try:
            return current_allocation + [remaining_players]

        # Recursive case: make as big of a game as possible
        if len(remaining_players) > game_size_to_try:
            return cls._allocate_players_helper(
                current_allocation + [remaining_players[:game_size_to_try]],
                remaining_players[game_size_to_try:],
                game_size_to_try
            )

        # Backtrack recursive case: need to shrink a game
        if len(remaining_players) < MIN_PLAYERS_IN_GAME:
            last_game = current_allocation[-1]
            return cls._allocate_players_helper(
                current_allocation[:-1],
                last_game + remaining_players,
                game_size_to_try - 1
            )
