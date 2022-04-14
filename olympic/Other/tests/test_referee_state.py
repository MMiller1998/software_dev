import unittest

from unittest.mock import Mock

from trains.state.constants import TURN_DRAW_CARDS_COUNT
from trains.state.action import WantCards, Acquire
from trains.graph_elements import RailColor
from trains.state.cardsholder import count_card_hand
from trains.state.referee import RefereeState
from trains.state.player import PlayerState
from trains.state.errors import GameOverException

import tests.examples.milestone2 as example
from tests.examples.milestone4 import create_example

from tests.helpers.change_player import give_player_cards, change_rail_count


class TestRefereeState(unittest.TestCase):
    def setUp(self) -> None:
        self.referee, self.player1, self.player2, self.player3, _ = create_example()

    def test_get_player(self):
        self.assertIs(self.referee.current_player, self.player1)
        self.assertIs(
            self.referee.next_turn().current_player, self.player2
        )
        self.assertIs(
            self.referee.next_turn().next_turn().current_player, self.player3
        )
        self.assertIs(
            self.referee.next_turn().next_turn().next_turn().current_player, self.player1
        )

    def test_request_cards(self):
        _, new_referee = self.referee.attempt_request_cards()
        self.assertEqual(count_card_hand(new_referee.current_player.cards), 2)
        self.assertEqual(len(new_referee._cards),
                         len(self.referee._cards) - 2)

    def test_is_acquisition_allowed(self):
        referee = give_player_cards(self.referee, RailColor.GREEN, 5)
        self.assertTrue(referee.is_acquisition_allowed(example.c_bwi_bwi))
        self.assertFalse(referee.is_acquisition_allowed(example.c_mrtl_iad))

        referee = change_rail_count(referee, num_rails=4)
        self.assertTrue(referee.is_acquisition_allowed(example.c_bwi_bwi))
        self.assertFalse(referee.is_acquisition_allowed(example.c_bwi_bos1))

    def test_acquire_connection(self):
        connection = example.c_bwi_lax
        referee = self.referee
        referee = give_player_cards(referee, connection.color, 5)
        referee = change_rail_count(referee, num_rails=6)
        referee.is_acquisition_allowed = Mock(return_value=True)

        after = referee.attempt_acquire_connection(connection)
        referee.is_acquisition_allowed.assert_called_once_with(connection)

        self.assertTrue(after.current_player.occupies(connection))
        self.assertEqual(after.current_player.num_rails, 6 - connection.length,
                         msg=f'Player.num_rails was not deducted after acquiring a connection')
        self.assertEqual(after.current_player.cards[connection.color], 5 - connection.length,
                         msg=f'Player colored cards were not taken away after acquiring a connection')

    def test_is_game_over_not_over(self):
        referee = self.referee
        self.assertFalse(referee.is_game_over())

        referee = change_rail_count(referee, num_rails=10)
        referee = give_player_cards(referee, RailColor.RED, 3)

        _, referee = referee.accept_player_turn(Acquire(example.c_bwi_lax))
        self.assertFalse(referee.is_game_over())

        _, referee = referee.accept_player_turn(WantCards())
        self.assertFalse(referee.is_game_over())

        _, referee = referee.accept_player_turn(WantCards())
        self.assertFalse(referee.is_game_over())

    def test_is_game_over_not_enough_rails(self):
        referee = self.referee

        referee = change_rail_count(referee, num_rails=5)
        referee = give_player_cards(referee, RailColor.RED, 3)

        self.assertFalse(referee.is_game_over())
        _, referee = referee.accept_player_turn(Acquire(example.c_bwi_lax))
        self.assertTrue(referee.is_game_over())

    def test_is_game_over_no_active_players(self):
        referee = self.referee.update(players=(), cheaters=self.referee.active_players)

        self.assertTrue(referee.is_game_over())

    def test_is_game_over_stale_state(self):
        referee = self.referee.update(cards=[])

        self.assertFalse(referee.is_game_over())
        _, referee = referee.accept_player_turn(WantCards())

        self.assertFalse(referee.is_game_over())
        _, referee = referee.accept_player_turn(WantCards())

        self.assertFalse(referee.is_game_over())
        _, referee = referee.accept_player_turn(WantCards())

        self.assertTrue(referee.is_game_over())

    def _deplete_cards(self, referee: RefereeState) -> RefereeState:
        starting_cards = len(referee._cards)
        _, after = referee.accept_player_turn(WantCards())
        remaining_cards = len(after._cards)
        drawn_cards = starting_cards - remaining_cards

        if drawn_cards < TURN_DRAW_CARDS_COUNT:
            self.assertEqual(drawn_cards, remaining_cards)
            return after

        self.assertEqual(drawn_cards, TURN_DRAW_CARDS_COUNT)
        return self._deplete_cards(after)

    def test_deplete_cards(self):
        referee = self._deplete_cards(self.referee)
        self.assertEqual(0, len(referee._cards),
                         msg='Referee draw pile is not empty but it should be.')

        cards_before = referee.current_player.cards.copy()
        _, referee = referee.attempt_request_cards()
        self.assertEqual(cards_before, referee.current_player.cards,
                         msg="Player's colored cards changed after asking referee "
                             "for cards when the referee has no cards left.")

        _, referee = referee.attempt_request_cards()
        self.assertEqual(0, len(referee._cards),
                         msg='Referee draw pile is not empty but it should be.')

    def test_get_player_state_scores(self):
        player1_state, player2_state, player3_state = self.setup_simple_players()
        referee_state = self.referee.update(players=(player1_state, player2_state, player3_state))

        self.assertEqual(referee_state.get_player_state_scores(), [-15, 48, 28])

    def test_get_player_state_ranking_empty(self):
        referee_state = self.referee.update(players=())
        self.assertListEqual(referee_state.get_player_state_ranking(), [])

    def test_get_player_state_ranking_simple(self):
        player1_state, player2_state, player3_state = self.setup_simple_players()
        referee_state = self.referee.update(players=(player1_state, player2_state, player3_state))

        self.assertListEqual(
            referee_state.get_player_state_ranking(),
            [{player2_state}, {player3_state}, {player1_state}]
        )

    def test_get_player_state_ranking_tie(self):
        referee_state, player1_state, player2_state, player3_state, _ = create_example()

        self.assertListEqual(referee_state.get_player_state_ranking(), [{player1_state, player2_state, player3_state}])

    def test_get_player_state_ranking_partial_tie(self):
        referee_state, player1_state, player2_state, player3_state, _ = create_example()
        player1_state = player1_state.update(occupied=[example.c_bwi_lax])
        referee_state = referee_state.update(players=(player1_state, player2_state, player3_state))

        self.assertListEqual(referee_state.get_player_state_ranking(), [{player1_state}, {player2_state, player3_state}])

    def setup_simple_players(self):
        player1_state = PlayerState(
            destinations=frozenset((
                frozenset((example.bos, example.bwi2)),
                frozenset((example.lax, example.bwi1))
            )),
            occupied=[example.c_mrtl_iad]
        )

        player2_state = PlayerState(
            destinations=frozenset((
                frozenset((example.bos, example.lax)),
                frozenset((example.lax, example.bwi2))
            )),
            occupied=[example.c_bwi_lax, example.c_bwi_bos1]
        )

        player3_state = PlayerState(
            destinations=frozenset((
                frozenset((example.bos, example.bwi1)),
                frozenset((example.mrtl, example.iad))
            )),
            occupied=[example.c_bwi_bos2, example.c_bwi_bwi]
        )

        return player1_state, player2_state, player3_state
