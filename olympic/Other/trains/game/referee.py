import itertools

from typing import Tuple, Dict, FrozenSet, List, Set, Callable, Iterable, Optional

from trains.map import TrainMap, Destination
from trains.utils import MethodStatus, safe_player_call
from trains.state.referee import RefereeState
from trains.state.action import WantCards, Acquire, ActionOption
from trains.state.player import PlayerState, PlayerStateWrapper
from trains.state.cardsholder import CardDeck, card_deck_to_card_hand
from trains.game.player import PlayerActor
from trains.game.constants import (
    MIN_PLAYERS_IN_GAME, MAX_PLAYERS_IN_GAME,
    STARTING_DESTINATION_TAKE_COUNT, STARTING_DESTINATION_OFFER_COUNT,
    TOTAL_CARD_DECK_SIZE, STARTING_RAIL_COUNT, STARTING_CARD_COUNT
)
from trains.game.types import Ranking, Rank
from trains.game.errors import (
    TooFewPlayersException, TooManyPlayersException,
    NotEnoughDestinationsException, CardDeckSizeException, DestinationChoiceException
)
from trains.strategy.lexico import lexicographically_sorted_destinations


class RefereeActor:
    """
    Oversees a game involving *players* from setup, steady-state, to end.

    It attempts to address some *player* misbehavior, such as

    - bad choice of destinations during setup
    - taking too long (DoS) to make a decision
    """

    @staticmethod
    def _validate_players(players: List[PlayerActor]) -> None:
        """
        :raises TooFewPlayersException:
        :raises TooManyPlayersException:
        """
        if len(players) < MIN_PLAYERS_IN_GAME:
            raise TooFewPlayersException('Not enough players to start the game. '
                                         f'{len(players)} joined, {MIN_PLAYERS_IN_GAME} needed.')

        if len(players) > MAX_PLAYERS_IN_GAME:
            raise TooManyPlayersException('Too many players are trying to join the game. '
                                          f'Only {MAX_PLAYERS_IN_GAME} may join this game.')

    @staticmethod
    def _validate_train_map(train_map: TrainMap, player_actors: List[PlayerActor]) -> None:
        """
        :raises NotEnoughDestinationsException:
        """
        num_dests_not_selected = STARTING_DESTINATION_OFFER_COUNT - STARTING_DESTINATION_TAKE_COUNT
        if len(list(train_map.get_destinations())) < (STARTING_DESTINATION_TAKE_COUNT * len(player_actors)) + num_dests_not_selected:
            raise NotEnoughDestinationsException()

    @staticmethod
    def _validate_cards(card_deck: CardDeck) -> None:
        """
        :raises CardDeckSizeEception:
        """
        if len(card_deck) != TOTAL_CARD_DECK_SIZE:
            raise CardDeckSizeException()

    @staticmethod
    def _validate_destinations(offered: Set[Destination], not_chosen: Set[Destination]) -> None:
        """
        :raises DestinationChoiceException:
        """
        if not (len(not_chosen) == (STARTING_DESTINATION_OFFER_COUNT - STARTING_DESTINATION_TAKE_COUNT) and not_chosen < offered):
            raise DestinationChoiceException()

    @staticmethod
    def _setup_player(
        player_actor: PlayerActor, train_map: TrainMap, cards: CardDeck, destinations_to_offer: FrozenSet[Destination]
    ) -> FrozenSet[Destination]:
        """
        Setup phase for a single player. Includes validation of destinations selected.

        :return: either an OK indicator and the unwanted destinations, or an ERROR indicator
            if the player cheated on destination selection
        :raises: DestinationChoiceException
        :raises: any error from `PlayerActor.setup` or `PlayerActor.pick`
        """
        player_actor.setup(train_map, STARTING_RAIL_COUNT, cards)
        destinations_not_chosen = player_actor.pick(destinations_to_offer)

        RefereeActor._validate_destinations(destinations_to_offer, destinations_not_chosen)

        return destinations_not_chosen

    @staticmethod
    def _setup_players(player_actors: List[PlayerActor], train_map: TrainMap, card_deck: CardDeck,
        dest_sorting_func: Callable[[Iterable[Destination]], List[Destination]]
    ) -> Tuple[List[PlayerState], Set[PlayerActor], CardDeck, Dict[FrozenSet[Destination], PlayerActor]]:
        """
        Setup phase for a game. See https://www.ccs.neu.edu/home/matthias/4500-f21/trains.html.

        :return: the `PlayerState`s of each player in the same order as `players`, the `PlayerActor`s
            that cheated during destination delection, the card deck after handing out cards to players,
            and a mapping of chosen destinations to `PlayerActor` instances for non-cheating players
        """
        handout_deck: CardDeck = card_deck.copy()
        destinations_left: List[Destination] = dest_sorting_func((train_map.get_destinations()))
        non_cheating_player_states: List[PlayerState] = []
        cheating_actors: Set[PlayerActor] = set()

        actor_map: Dict[FrozenSet[Destination], PlayerActor] = dict()

        for player_actor in player_actors:
            starting_cards = handout_deck[:STARTING_CARD_COUNT]
            handout_deck = handout_deck[STARTING_CARD_COUNT:]

            destinations_to_offer = frozenset(destinations_left[:STARTING_DESTINATION_OFFER_COUNT])

            result = safe_player_call(
                lambda: RefereeActor._setup_player(player_actor, train_map, starting_cards, destinations_to_offer)
            )

            if result == MethodStatus.ERROR:
                cheating_actors.add(player_actor)
            else:
                destinations_not_chosen = result[1]
                destinations_chosen = destinations_to_offer - destinations_not_chosen
                for chosen_dest in destinations_chosen:
                    destinations_left.remove(chosen_dest)

                non_cheating_player_states.append(
                    PlayerState(
                        destinations_chosen,
                        cards=card_deck_to_card_hand(starting_cards),
                        num_rails=STARTING_RAIL_COUNT
                    )
                )
                actor_map[destinations_chosen] = player_actor

        return non_cheating_player_states, cheating_actors, handout_deck, actor_map

    @staticmethod
    def run_game(
        players: List[PlayerActor], train_map: TrainMap, card_deck: CardDeck,
        dest_sorting_func: Callable[[Iterable[Destination]], List[Destination]] = lexicographically_sorted_destinations
    ) -> Tuple[Ranking[PlayerActor], Rank[PlayerActor]]:
        """
        Executes a game of Trains. This includes setup, steady-state, and termination, plus scoring.
        See https://www.ccs.neu.edu/home/matthias/4500-f21/trains.html.

        :return: a dictionary mapping remaining players to their final score, and the
            players which were removed for cheating
        :raises TooFewPlayersException:
        :raises TooManyPlayersException:
        :raises NotEnoughDestinationsException:
        :raises CardDeckSizeEception:
        """
        RefereeActor._validate_players(players)
        RefereeActor._validate_train_map(train_map, players)
        RefereeActor._validate_cards(card_deck)

        (
            non_cheater_player_states,
            setup_cheaters,
            remaining_deck,
            actor_map
        ) = RefereeActor._setup_players(players, train_map, card_deck, dest_sorting_func)

        starting_state = RefereeState(
            train_map=train_map,
            players=tuple(non_cheater_player_states),
            cheaters=frozenset(),
            cards=remaining_deck,
            turns_without_state_change=0
        )

        ending_state = RefereeActor._run_turns(starting_state, actor_map)

        tentative_ranking = RefereeActor._get_ranking(ending_state, actor_map)
        final_ranking, result_cheaters = RefereeActor._notify_players_of_result(tentative_ranking)

        cheater_actors = setup_cheaters.union(set(
            (actor_map[cheater_state.destinations] for cheater_state in ending_state.cheaters)
        )).union(result_cheaters)

        return final_ranking, cheater_actors

    @staticmethod
    def _run_turn(state: RefereeState, player_actor: PlayerActor) -> RefereeState:
        """
        Generate the next state of the game after having the given `PlayerActor` take a turn.

        :raises: any error from `PlayerActor.play`
        :raises CantAcquireException:
        """
        action = player_actor.play(state.generate_current_player_state_wrapper())
        cards_to_give, new_state = state.accept_player_turn(action)
        if cards_to_give is not None:
            result = safe_player_call(lambda: player_actor.more(cards_to_give))
            if result is MethodStatus.ERROR:
                return new_state.remove_cheater()

        return new_state.next_turn()

    @staticmethod
    def _run_turns(state: RefereeState, actor_map: Dict[FrozenSet[Destination], PlayerActor]) -> RefereeState:
        """
        Steady-state phase of a game of Trains. Each iteration of this method is one turn of the game.

        :param state: the current `RefereeState` of the game
        :param actor_map: the mapping used to identify a `PlayerActor` based on information available in `PlayerState`
        :return: the final `RefereeState` of the game
        """
        if state.is_game_over():
            return state

        player_actor = actor_map[state.current_player.destinations]

        result = safe_player_call(lambda: RefereeActor._run_turn(state, player_actor))
        if result == MethodStatus.ERROR:
            next_state = state.remove_cheater()
        else:
            next_state = result[1]

        return RefereeActor._run_turns(next_state, actor_map)

    @staticmethod
    def _notify_players_of_result(ranking: Ranking[PlayerActor]) -> Tuple[Ranking[PlayerActor], Set[PlayerActor]]:
        """
        Calls `PlayerActor.win` on each `PlayerActor` in the given ranking.

        :return: a tuple of the final ranking after notifying players of their result
            and a set of `PlayerActor`s who "cheated" while being called.
        """
        final_ranking = []
        cheaters = set()

        if ranking:
            winners = ranking[0]
            losers = list(itertools.chain.from_iterable(ranking[1:]))

            winner_cheaters = RefereeActor._notify_players_of_result_helper(winners, True)
            final_ranking.append([winner for winner in winners if winner not in winner_cheaters])

            loser_cheaters = RefereeActor._notify_players_of_result_helper(losers, False)
            for rank in ranking[1:]:
                final_ranking.append([loser for loser in rank if loser not in loser_cheaters])

            cheaters = winner_cheaters.union(loser_cheaters)

        return final_ranking, cheaters

    @staticmethod
    def _notify_players_of_result_helper(player_actors: List[PlayerActor], won: bool) -> Set[PlayerActor]:
        """
        :return: a set containing the `PlayerActor`s who "cheated" while being called.
        """
        cheaters = set()
        for pa in player_actors:
            result = safe_player_call(lambda: pa.win(won))
            if result == MethodStatus.ERROR:
                cheaters.add(pa)
        return cheaters

    @staticmethod
    def _get_ranking(end_state: RefereeState, actor_map: Dict[FrozenSet[Destination], PlayerActor]) -> Ranking[PlayerActor]:
        """
        Get a ranking based on `PlayerActor`s scores from the given end-game state.

        :return: a list where each ith inner list contains all ith-place finishers.
            An ith-place finisher is a player that has the ith-highest score.
        """
        player_state_ranking = end_state.get_player_state_ranking()
        return RefereeActor._state_to_actor_ranking(player_state_ranking, actor_map)

    @staticmethod
    def _state_to_actor_ranking(
        player_state_ranking: Ranking[PlayerState],
        actor_map: Dict[FrozenSet[Destination], PlayerActor]
    ) -> Ranking[PlayerActor]:
        """
        Translates `PlayerState`s in a ranking to their corresponding `PlayerActor`.
        """
        return [{actor_map[ps.destinations] for ps in rank} for rank in player_state_ranking]
