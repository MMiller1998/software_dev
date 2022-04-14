from typing import Tuple, FrozenSet, Iterator, List, Set, Optional

from trains.game.constants import POINTS_FOR_LONGEST_PATH
from trains.game.types import ScorePoint, Ranking
from trains.graph_elements import TrainConnection
from trains.map import TrainMap
from trains.state.action import AGameOfTrains, ActionOption, WantCards, Acquire
from trains.state.cardsholder import CardDeck
from trains.state.constants import MIN_RAILS_BEFORE_GAME_WRAPS_UP, TURN_DRAW_CARDS_COUNT
from trains.state.errors import CantAcquireException
from trains.state.player import PlayerState, PlayerStateWrapper


class RefereeState(AGameOfTrains):
    """
    a ``RefereeState`` is a representation of all of the information
    that comprises the current game state
    """

    def __init__(self,
                 train_map: TrainMap,
                 players: Tuple[PlayerState, ...],
                 cheaters: FrozenSet[PlayerState],
                 cards: CardDeck,
                 turns_without_state_change: int):
        self._train_map: TrainMap = train_map
        self.__players: Tuple[PlayerState] = players
        """
        The players who will have a turn.
        """
        self.__cheaters: FrozenSet[PlayerState] = cheaters
        """
        The players who have cheated/misbehaved.
        """
        self._cards: CardDeck = cards
        """
        Colored cards in possession by this *referee*, which may be given to a
        *player* on their turn.
        """
        self._turns_without_state_change = turns_without_state_change

    def update(self,
               train_map: TrainMap = None,
               players: Tuple[PlayerState, ...] = None,
               cheaters: FrozenSet[PlayerState] = None,
               cards: CardDeck = None,
               turns_without_state_change=None
               ) -> 'RefereeState':
        return self.__class__(
            train_map=(train_map if train_map is not None else self._train_map),
            players=(players if players is not None else self.active_players),
            cheaters=(cheaters if cheaters is not None else self.cheaters),
            cards=(cards if cards is not None else self._cards),
            turns_without_state_change=(
                turns_without_state_change if turns_without_state_change is not None else self._turns_without_state_change)
        )

    def is_acquisition_allowed(self, connection: TrainConnection) -> bool:
        """
        Determine if a ``TrainConnection`` is able to be acquired, meaning it
        is has not already been acquired and that current player attempting to
        acquire it has the necessary cards and rails to do so.

        :param connection: the connection object which the current player wants ot acquire
        :return: whether or not the given ``TrainConnection`` can be acquired by the current player
        """
        if self.is_occupied(connection):
            return False
        return self.current_player.can_acquire(connection)

    def get_acquirable(self) -> Iterator[TrainConnection]:
        """
        :return: connections which the current player may legally acquired
        """
        return filter(self.is_acquisition_allowed, self._train_map.get_all_connections())

    def is_occupied(self, connection: TrainConnection):
        """
        :return: True if given connection is occupied by any player who has not yet cheated
        """
        return any(p.occupies(connection) for p in self.active_players)

    def accept_player_turn(self, action: ActionOption) -> Tuple[Optional[CardDeck], 'RefereeState']:
        """
        Execute a player's action. Return the new RefereeState after the action has been executed, and the cards given
        to the player during that turn if its action was requesting cards
        """
        cards_to_give = None
        if isinstance(action, WantCards):
            cards_to_give, new_state = self.attempt_request_cards()
        elif isinstance(action, Acquire):
            new_state = self.attempt_acquire_connection(action.connection)
        else:
            raise ValueError("Not a valid action")

        return cards_to_give, new_state

    def attempt_acquire_connection(self, connection: TrainConnection) -> 'RefereeState':
        """
        Have the current player attempt to occupy a connection.

        :return: a new `RefereeState` with the current player updated to reflect connection ownership
        :raises: `CantAcquireException` if the acquisition is illegal
        """
        if not self.is_acquisition_allowed(connection):
            raise CantAcquireException()

        player = self.current_player.occupy(connection)
        return self.update_current_player(player).update(turns_without_state_change=0)

    def attempt_request_cards(self) -> Tuple[CardDeck, 'RefereeState']:
        """
        Give the current player two (or fewer) cards from the referee's draw pile.
        """
        cards_to_give, new_deck = self._pick_cards()

        player = self.current_player.give_cards(cards_to_give)

        if not cards_to_give:
            turns_without_state_change = self._turns_without_state_change + 1
        else:
            turns_without_state_change = 0

        return cards_to_give, self.update_current_player(player).update(cards=new_deck,
                                                                        turns_without_state_change=turns_without_state_change)

    def _pick_cards(self) -> Tuple[CardDeck, CardDeck]:
        """
        Try to choose multiple colored cards at random, but only as much as there
        are cards left in the *referee*'s draw pile.

        :return: a `CardDeck` of the chosen cards and a `CardDeck` of the remaining cards
        """
        return self._cards[:TURN_DRAW_CARDS_COUNT], self._cards[TURN_DRAW_CARDS_COUNT:]

    @property
    def current_player(self) -> PlayerState:
        """
        :return: the player who is taking its turn
        """
        return self.active_players[0]

    @property
    def active_players(self) -> Tuple[PlayerState, ...]:
        """
        :return: all *players* who have not cheated yet, in turn order
        """
        return self.__players

    @property
    def cheaters(self):
        return self.__cheaters

    def generate_current_player_state_wrapper(self) -> PlayerStateWrapper:
        """
        Generate a `PlayerStateWrapper` for the current player, which represents all the
        information a player knows about the game.
        """
        return PlayerStateWrapper(self.current_player, self.get_opposing_connections())

    def is_game_over(self) -> bool:
        """
        :return: whether or not the game has ended.
            see https://www.ccs.neu.edu/home/matthias/4500-f21/trains.html for spec
        """
        return len(self.active_players) == 0 or \
               self.current_player.num_rails <= MIN_RAILS_BEFORE_GAME_WRAPS_UP or \
               self._turns_without_state_change >= len(self.active_players)

    def next_turn(self) -> 'RefereeState':
        return self.update(
            players=(self.active_players[1:] + self.active_players[:1])
        )

    def update_current_player(self, player: PlayerState) -> 'RefereeState':
        """
        Change the current *player* (without changing the turn).
        """
        return self.update(
            players=tuple((player,) + self.active_players[1:])
        )

    def remove_cheater(self) -> 'RefereeState':
        """
        Marks the current *player* as having misbehaved.
        The *connections* they own are released and once again available to be acquired by the
        other players who have not cheated yet.
        """
        return self.update(
            players=self.active_players[1:],
            cheaters=frozenset(
                self.cheaters | {self.current_player}
            )
        )

    def get_opposing_connections(self) -> List[List[TrainConnection]]:
        """
        Return the occupied connections of all players that are not the current player
        """
        return [player_state.occupied for player_state in self.__players if player_state != self.current_player]

    def _collective_points_for_acquired_segments(self) -> List[ScorePoint]:
        """
        Calculate segment scores for the active `PlayerState`s. Returns a list of `ScorePoint`s
        which correspond to the given `self.active_players`s by index.
        """
        return [ps.points_for_acquired_segments() for ps in self.active_players]

    def _collective_points_for_destinations(self) -> List[ScorePoint]:
        """
        Calculate destination scores for the active `PlayerState`s. Returns a list of `ScorePoint`s
        which correspond to the given `self.active_players`s by index.
        """
        return [ps.points_for_destinations() for ps in self.active_players]

    def _collective_points_for_longest_path(self) -> List[ScorePoint]:
        """
        Calculate longest path scores for the active `PlayerState`s. Returns a list of `ScorePoint`s
        which correspond to the given `self.active_players`s by index.
        """
        player_states = self.active_players
        if not player_states:
            return []

        longest_paths = {ps.destinations: ps.get_longest_path_length() for ps in player_states}
        max_length = max(longest_paths.values())

        return [POINTS_FOR_LONGEST_PATH if longest_paths[ps.destinations] == max_length else 0 for ps in player_states]

    def get_player_state_scores(self) -> List[ScorePoint]:
        """
        Create a list of scores corresponding to `self.active_players` by index.
        """
        segment_scores = self._collective_points_for_acquired_segments()
        destination_scores = self._collective_points_for_destinations()
        longest_path_scores = self._collective_points_for_longest_path()

        return [sum(scores) for scores in zip(segment_scores, destination_scores, longest_path_scores)]

    def get_player_state_ranking(self) -> Ranking[PlayerState]:
        """
        Get a ranking of active `PlayerState`s scores.
        """
        player_states = self.active_players
        scores = self.get_player_state_scores()
        states_and_scores = list(zip(player_states, scores))

        ordered_scores = sorted(set(scores), reverse=True)
        ranking = []
        for score in ordered_scores:
            ranking.append(self._player_states_that_got_score(states_and_scores, score))

        return ranking

    @staticmethod
    def _player_states_that_got_score(states_and_scores: List[Tuple[PlayerState, ScorePoint]], score: ScorePoint) -> \
            Set[PlayerState]:
        """
        Given a correspondance from a `PlayerState` to its score and a score to check,
        return the `PlayerStates` which obtained the given score.
        """
        return {ps for ps, ps_score in states_and_scores if ps_score == score}
