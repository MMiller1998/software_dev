from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock
from typing import FrozenSet, Set

from trains.graph_elements import Destination, RailColor
from trains.game.referee import RefereeActor
from trains.game.player import PlayerActor
from trains.game.constants import (
    STARTING_RAIL_COUNT, STARTING_DESTINATION_RETURN_COUNT, STARTING_CARD_COUNT
)
from trains.game.errors import DestinationChoiceException
from trains.strategy.lexico import lexicographically_sorted_destinations
from trains.strategy.buy_now import MyStrategy as BuyNow
from tests.examples import milestone2 as example, milestone4 as example2, bigger_map, decks


class TestRefereeActor(TestCase):

    def test__setup_player_go_right(self):
        cards = [RailColor.BLUE, RailColor.RED, RailColor.GREEN, RailColor.WHITE]

        destinations = {example.dest_bwi1_bos, example.dest_bwi1_bwi2, example.dest_bwi1_lax, example.dest_mrtl_iad, example.dest_bwi2_bos}
        dests_to_not_choose = set(lexicographically_sorted_destinations(list(destinations))[:STARTING_DESTINATION_RETURN_COUNT])

        player_actor = MagicMock()
        player_actor.pick.return_value = dests_to_not_choose

        dests_from_setup_player = RefereeActor._setup_player(player_actor, example.train_map, cards, destinations)

        player_actor.setup.assert_called_with(example.train_map, STARTING_RAIL_COUNT, cards)
        player_actor.pick.assert_called_with(destinations)

        self.assertSetEqual(dests_from_setup_player, dests_to_not_choose)

    def test__setup_player_wrong_number_of_destinations(self):
        cards = [RailColor.BLUE, RailColor.RED, RailColor.GREEN, RailColor.WHITE]

        destinations = {example.dest_bwi1_bos, example.dest_bwi1_bwi2, example.dest_bwi1_lax, example.dest_mrtl_iad, example.dest_bwi2_bos}
        dests_to_not_choose = destinations

        player_actor = MagicMock()
        player_actor.pick.return_value = dests_to_not_choose

        with self.assertRaises(DestinationChoiceException):
            RefereeActor._setup_player(player_actor, example.train_map, cards, destinations)

    def test__setup_player_bad_dest_return(self):
        cards = [RailColor.BLUE, RailColor.RED, RailColor.GREEN, RailColor.WHITE]

        destinations = {example.dest_bwi1_bos, example.dest_bwi1_bwi2, example.dest_bwi1_lax, example.dest_mrtl_iad, example.dest_bwi2_bos}
        dests_to_not_choose = set(lexicographically_sorted_destinations(list(destinations))[:STARTING_DESTINATION_RETURN_COUNT - 1]).union({example.dest_lax_bos})

        player_actor = MagicMock()
        player_actor.pick.return_value = dests_to_not_choose

        with self.assertRaises(DestinationChoiceException):
            RefereeActor._setup_player(player_actor, example.train_map, cards, destinations)

    def test__setup_players_go_right(self):
        player_actors = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        player_actors[0].pick.side_effect = player_pick_correct_mock_side_effect
        player_actors[1].pick.side_effect = player_pick_correct_mock_side_effect
        player_actors[2].pick.side_effect = player_pick_cheat_mock_side_effect
        player_actors[3].pick.side_effect = player_pick_cheat_mock_side_effect

        ordered_dests = lexicographically_sorted_destinations(bigger_map.train_map.get_destinations())
        player1_expected_dests = frozenset((ordered_dests[3], ordered_dests[4]))
        player2_expected_dests = frozenset((ordered_dests[5], ordered_dests[6]))
        expected_actor_map = {player1_expected_dests: player_actors[0], player2_expected_dests: player_actors[1]}

        (
            non_cheater_player_states,
            cheater_actors,
            remaining_deck,
            actor_map
        ) = RefereeActor._setup_players(player_actors, bigger_map.train_map, decks.green_deck, lexicographically_sorted_destinations)

        self.assertListEqual([ps.destinations for ps in non_cheater_player_states], [player1_expected_dests, player2_expected_dests])
        self.assertTrue(all((ps.card_count == STARTING_CARD_COUNT for ps in non_cheater_player_states)))
        self.assertSetEqual(cheater_actors, set(player_actors[2:]))
        self.assertEqual(len(remaining_deck), len(decks.green_deck) - (STARTING_CARD_COUNT * len(player_actors)))
        self.assertDictEqual(actor_map, expected_actor_map)

    @patch('trains.game.referee.RefereeState')
    def test__run_turns(self, mock_ref_game_state):
        mock_player_state = MagicMock()
        player_destinations = frozenset([bigger_map.dest_1_2, bigger_map.dest_1_3])
        mock_player_state.destinations = PropertyMock(return_value=player_destinations)

        mock_ref_game_state_instance = mock_ref_game_state.return_value
        mock_ref_game_state_instance.is_game_over.side_effect = [False, True]
        mock_ref_game_state_instance.current_player = PropertyMock(return_value=mock_player_state) # mock_player_state
        fake_acquirable_connections = MagicMock()
        mock_ref_game_state_instance.get_acquirable.return_value = fake_acquirable_connections

        mock_player_action = MagicMock()
        mock_player_actor = MagicMock()
        mock_player_actor.on_turn.return_value = mock_player_action

        actor_map = {player_destinations: mock_player_actor}
        print('actor_map', actor_map)
        print('mock current_player', mock_ref_game_state_instance.current_player)
        print('mock cp dests', mock_ref_game_state_instance.current_player.destinations)

        RefereeActor._run_turns(mock_ref_game_state_instance, actor_map)

        self.assertEqual(2, mock_ref_game_state_instance.is_game_over.call_count)
        mock_player_actor.on_turn.assert_called_with(mock_player_state, fake_acquirable_connections)
        mock_ref_game_state_instance.accept.assert_called_with(mock_player_action)

    def test__run_turns_take2(self):
        # real object setup
        referee_state, player1_state, player2_state, _, _ = example2.create_example()
        player1_actor = PlayerActor(BuyNow(), example.train_map)
        actor_map = {player1_state.destinations: player1_actor}
        print('actor_map', actor_map)

        # method mock setup
        referee_state.is_game_over = MagicMock(name='is_game_over', side_effect=[False, True])
        print('mock is game over', referee_state.is_game_over)
        print(referee_state.is_game_over())
        print(referee_state.is_game_over())
        print(referee_state.is_game_over())

        RefereeActor._run_turns(referee_state, actor_map)

        self.assertEqual(2, referee_state.is_game_over.call_count)


def player_pick_correct_mock_side_effect(destinations: Set[Destination]) -> FrozenSet[Destination]:
    return set(lexicographically_sorted_destinations(list(destinations))[:STARTING_DESTINATION_RETURN_COUNT])

def player_pick_cheat_mock_side_effect(destinations: Set[Destination]) -> FrozenSet[Destination]:
    return frozenset(destinations)
