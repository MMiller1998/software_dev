import unittest
from unittest.mock import patch, Mock

from trains.strategy.strategy import (
    choose_among_lexicographically_sorted, choose_acquirable_lexicographically_first_connection,
    strategy_name_to_file_name, strategy_name_to_file_path
)
from trains.strategy.hold_10 import MyStrategy as HoldTen
from trains.strategy.buy_now import MyStrategy as BuyNow
from trains.strategy.cheat import MyStrategy as Cheat
from trains.graph_elements import RailColor
from trains.state.action import WantCards, Acquire
from trains.state.cardsholder import EMPTY_HAND, create_hand

import tests.examples.milestone2 as example
import tests.examples.milestone4 as milestone4
from tests.examples import bigger_map


class HelpersTestCase(unittest.TestCase):
    def setUp(self) -> None:
        _, self.player, _, _, _ = milestone4.create_example()

    def test_choose_among(self):
        destinations = frozenset((
            frozenset((example.bos, example.lax,)),
            frozenset((example.iad, example.mrtl,)),
            frozenset((example.bwi1, example.bwi2)),
        ))
        chosen = choose_among_lexicographically_sorted(
            destinations,
            lambda x: x[:2]
        )
        self.assertSetEqual(
            chosen,
            {
                frozenset((example.bwi1, example.bwi2)),
                frozenset((example.bos, example.lax,))
            }
        )

    def test_choose_first_no_cards(self):
        player = self.player.update(
            num_rails=6,
            cards=EMPTY_HAND
        )

        choice = choose_acquirable_lexicographically_first_connection(player, example.all_connections)
        self.assertIsNone(choice)

    def test_choose_first(self):
        player = self.player.update(
            num_rails=4,
            cards=create_hand(4)
        )
        choice = choose_acquirable_lexicographically_first_connection(player, example.all_connections)
        self.assertEqual(choice, example.c_bwi_bos2)


class HoldTenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        _, _, _, _, self.player_wrapper = milestone4.create_example()

    def test_choose_destinations(self):
        dests_offered = {
            bigger_map.dest_1_2, bigger_map.dest_1_4, bigger_map.dest_2_4,
            bigger_map.dest_5_7, bigger_map.dest_6_7
        }
        not_chosen = HoldTen().choose_destinations(dests_offered)

        self.assertSetEqual(not_chosen, {bigger_map.dest_2_4, bigger_map.dest_5_7, bigger_map.dest_6_7})

    def test_want_cards(self):
        action = HoldTen().take_turn(self.player_wrapper, example.all_connections)
        self.assertIsInstance(action, WantCards)

    def test_acquire_connection(self):
        new_player_state = self.player_wrapper.player_state.update(
            num_rails=30,
            cards=create_hand(3)
        )
        self.player_wrapper.player_state = new_player_state
        action = HoldTen().take_turn(self.player_wrapper, example.all_connections)
        self.assertIsInstance(action, Acquire)

    def test_draw_to_ten(self):
        new_player_state = self.player_wrapper.player_state.update(
            num_rails=30,
            cards={RailColor.RED: 5, RailColor.BLUE: 0, RailColor.GREEN: 0, RailColor.WHITE: 0}
        )
        self.player_wrapper.player_state = new_player_state

        action = HoldTen().take_turn(self.player_wrapper, example.all_connections)
        self.assertIsInstance(action, WantCards)


class BuyNowTestCase(unittest.TestCase):
    def setUp(self) -> None:
        _, _, _, _, self.player2_state_wrapper = milestone4.create_example()

    def test_choose_detinations(self):
        dests_offered = {
            bigger_map.dest_1_2, bigger_map.dest_1_4, bigger_map.dest_2_4,
            bigger_map.dest_5_7, bigger_map.dest_6_7
        }
        not_chosen = BuyNow().choose_destinations(dests_offered)

        self.assertSetEqual(not_chosen, {bigger_map.dest_1_2, bigger_map.dest_1_4, bigger_map.dest_2_4})

    def test_want_cards(self):
        new_player_state = self.player2_state_wrapper.player_state.update(
            num_rails=4,
            cards=dict.fromkeys(self.player2_state_wrapper.player_state.cards, 0)
        )
        self.player2_state_wrapper.player_state = new_player_state

        action = BuyNow().take_turn(self.player2_state_wrapper, example.all_connections)
        self.assertIsInstance(action, WantCards)

    def test_acquire_connection(self):
        new_player_state = self.player2_state_wrapper.player_state.update(
            num_rails=30,
            cards=dict.fromkeys(self.player2_state_wrapper.player_state.cards, 4)
        )
        self.player2_state_wrapper.player_state = new_player_state

        action = BuyNow().take_turn(self.player2_state_wrapper, example.all_connections)
        self.assertIsInstance(action, Acquire)
        self.assertEqual(example.c_bwi_bos2, action.connection)

    def test_acquire_connection_first_is_taken(self):
        new_player_state = self.player2_state_wrapper.player_state.update(
            num_rails=30,
            cards=dict.fromkeys(self.player2_state_wrapper.player_state.cards, 3)
        )
        self.player2_state_wrapper.player_state = new_player_state
        self.player2_state_wrapper.other_player_acquireds = [[example.c_bwi_bos1]]

        action = BuyNow().take_turn(self.player2_state_wrapper, example.all_connections)
        self.assertIsInstance(action, Acquire)
        self.assertEqual(example.c_bwi_lax, action.connection)


class CheatTestCase(unittest.TestCase):
    def setUp(self) -> None:
        _, _, _, _, self.player2_state_wrapper = milestone4.create_example()

    def test_choose_detinations(self):
        dests_offered = {
            bigger_map.dest_1_2, bigger_map.dest_1_4, bigger_map.dest_2_4,
            bigger_map.dest_5_7, bigger_map.dest_6_7
        }
        not_chosen = Cheat().choose_destinations(dests_offered)

        self.assertSetEqual(not_chosen, {bigger_map.dest_1_2, bigger_map.dest_1_4, bigger_map.dest_2_4})

    @patch('trains.strategy.cheat.Acquire', spec=Acquire)
    def test_take_turn(self, acquire_spy: Mock):
        Cheat().take_turn(self.player2_state_wrapper, example.all_connections)
        acquire_spy.assert_called_once()


class TestStrategyPath(unittest.TestCase):
    def test_strategy_name_to_file_name(self):
        self.assertEqual(strategy_name_to_file_name('Hold-10'), 'hold_10.py')
        self.assertEqual(strategy_name_to_file_name('Buy-Now'), 'buy_now.py')
        self.assertEqual(strategy_name_to_file_name('Cheat'), 'cheat.py')

    def test_strategy_name_to_file_path(self):
        self.assertTupleEqual(strategy_name_to_file_path('Hold-10').parts[-4:], ('Other', 'trains', 'strategy', 'hold_10.py'))
        self.assertTupleEqual(strategy_name_to_file_path('Buy-Now').parts[-4:], ('Other', 'trains', 'strategy', 'buy_now.py'))
        self.assertTupleEqual(strategy_name_to_file_path('Cheat').parts[-4:], ('Other', 'trains', 'strategy', 'cheat.py'))


if __name__ == '__main__':
    unittest.main()
