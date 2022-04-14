import unittest
from unittest.mock import MagicMock, patch, Mock

from Trains.Admin.manager import Manager


class ManagerTests(unittest.TestCase):
    @patch('Trains.Admin.manager.IMapGenerator')
    @patch('Trains.Admin.manager.Referee')
    def test_run_tournament(self, mock_referee, mock_map_generator):
        all_players = self.setup_player_mocks()
        all_players[4].start = Mock(side_effect=Exception("Did not respond"))

        mock_valid_map = MagicMock()
        mock_valid_map.get_feasible_destinations.return_value = [1] * 80
        all_players[3].start.return_value = mock_valid_map

        mock_game_result_1 = MagicMock()
        mock_game_result_2 = MagicMock()
        mock_game_result_3 = MagicMock()
        mock_results_list = [mock_game_result_1, mock_game_result_2, mock_game_result_3]

        mock_referee.run_game = MagicMock(side_effect=mock_results_list)
        mock_game_result_1.get_winners.return_value = all_players[:2]
        mock_game_result_1.get_cheaters.return_value = all_players[1:3]
        mock_game_result_2.get_winners.return_value = all_players[-1]
        mock_game_result_3.get_winners.return_value = [all_players[0]]

        winners, cheaters = Manager.run_tournament(all_players, mock_map_generator.return_value)
        self.assertListEqual([all_players[0]], winners)
        self.assertSetEqual({all_players[1], all_players[2], all_players[4]}, set(cheaters))

    @patch('Trains.Admin.manager.IMapGenerator')
    def test_setup_with_valid_map(self, mock_generator):
        all_players = self.setup_player_mocks()
        mock_valid_map = MagicMock()
        mock_valid_map.get_feasible_destinations.return_value = [1] * 80
        all_players[3].start.return_value = mock_valid_map
        actual_map, cheaters = Manager.setup_tournament(all_players, mock_generator.return_value)
        for player in all_players:
            player.start.assert_called_with(True)
        self.assertEqual(mock_valid_map, actual_map)
        self.assertListEqual([], cheaters)

    @patch('Trains.Admin.manager.IMapGenerator')
    def test_setup_with_invalid_map(self, mock_generator):
        all_players = self.setup_player_mocks()
        mock_valid_map = MagicMock()
        mock_invalid_map = MagicMock()
        mock_invalid_map.get_feasible_destinations.return_value = [1] * 2
        all_players[0].start.return_value = mock_valid_map
        mock_map_generator_instance = mock_generator.return_value
        mock_map_generator_instance.generate_map.return_value = mock_valid_map
        actual_map, cheaters = Manager.setup_tournament(all_players, mock_generator.return_value)
        for player in all_players:
            player.start.assert_called_with(True)
        self.assertEqual(mock_valid_map, actual_map)
        self.assertListEqual([], cheaters)

    @patch('Trains.Admin.manager.IMapGenerator')
    def test_setup_with_cheaters(self, mock_generator):
        all_players = self.setup_player_mocks()
        mock_valid_map = MagicMock()
        mock_valid_map.get_feasible_destinations.return_value = [1] * 80
        all_players[3].start.return_value = mock_valid_map
        all_players[4].start = Mock(side_effect=Exception("Did not respond"))
        all_players[7].start = Mock(side_effect=Exception("Did not respond"))
        actual_map, cheaters = Manager.setup_tournament(all_players, mock_generator.return_value)
        for player in all_players:
            player.start.assert_called_with(True)
        self.assertEqual(mock_valid_map, actual_map)
        self.assertListEqual([all_players[4], all_players[7]], cheaters)

    @patch('Trains.Admin.manager.Referee')
    def test_run_rounds(self, mock_referee):
        all_players = self.setup_player_mocks()
        mock_game_result_1 = MagicMock()
        mock_game_result_2 = MagicMock()
        mock_game_result_3 = MagicMock()
        mock_results_list = [mock_game_result_1, mock_game_result_2, mock_game_result_3]
        mock_referee.run_game = MagicMock(side_effect=mock_results_list)
        mock_game_result_1.get_winners.return_value = all_players[:2]
        mock_game_result_2.get_winners.return_value = all_players[-1]
        mock_game_result_1.get_cheaters.return_value = [all_players[4], all_players[7]]
        mock_game_result_3.get_winners.return_value = all_players[:2]
        mock_map = MagicMock()
        winners, cheaters = Manager.run_rounds(all_players, mock_map)
        self.assertListEqual(all_players[:2], winners)
        self.assertListEqual([all_players[4], all_players[7]], cheaters)

    @patch('Trains.Admin.manager.Referee')
    def test_run_rounds_all_cheaters(self, mock_referee):
        all_players = self.setup_player_mocks()
        mock_game_result_1 = MagicMock()
        mock_game_result_2 = MagicMock()
        mock_game_result_3 = MagicMock()
        mock_results_list = [mock_game_result_1, mock_game_result_2, mock_game_result_3]
        mock_referee.run_game = MagicMock(side_effect=mock_results_list)
        mock_game_result_1.get_cheaters.return_value = all_players[:8]
        mock_game_result_2.get_cheaters.return_value = all_players[8:]
        mock_map = MagicMock()
        winners, cheaters = Manager.run_rounds(all_players, mock_map)
        self.assertListEqual([], winners)
        self.assertListEqual(all_players, cheaters)

    @patch('Trains.Admin.manager.Referee')
    def test_run_rounds_same_winners(self, mock_referee):
        all_players = self.setup_player_mocks()
        mock_game_result_1 = MagicMock()
        mock_game_result_2 = MagicMock()
        mock_game_result_3 = MagicMock()
        mock_results_list = [mock_game_result_1, mock_game_result_2, mock_game_result_3]
        mock_referee.run_game = MagicMock(side_effect=mock_results_list)
        mock_game_result_1.get_winners.return_value = all_players[:2]
        mock_game_result_2.get_winners.return_value = all_players[-1]
        mock_game_result_3.get_winners.return_value = all_players[:2] + [all_players[-1]]
        mock_map = MagicMock()
        winners, cheaters = Manager.run_rounds(all_players, mock_map)
        self.assertListEqual(all_players[:2] + [all_players[-1]], winners)
        self.assertListEqual([], cheaters)

    @patch('Trains.Admin.manager.Referee')
    def test_run_rounds_one_winner(self, mock_referee):
        all_players = self.setup_player_mocks()
        mock_game_result_1 = MagicMock()
        mock_game_result_2 = MagicMock()
        mock_results_list = [mock_game_result_1, mock_game_result_2]
        mock_referee.run_game = MagicMock(side_effect=mock_results_list)
        mock_game_result_1.get_winners.return_value = []
        mock_game_result_2.get_winners.return_value = [all_players[-1]]
        mock_map = MagicMock()
        winners, cheaters = Manager.run_rounds(all_players, mock_map)
        self.assertListEqual([all_players[-1]], winners)
        self.assertListEqual([], cheaters)

    def test_end_tournament(self):
        players = self.setup_player_mocks()
        losers = players[:5]
        winners = players[5:]
        Manager.end_tournament(losers, winners)
        for loser in losers:
            loser.end.assert_called_with(False)
        for winner in winners:
            winner.end.assert_called_with(True)

    def setup_player_mocks(self):
        player_1 = MagicMock()
        player_2 = MagicMock()
        player_3 = MagicMock()
        player_4 = MagicMock()
        player_5 = MagicMock()
        player_6 = MagicMock()
        player_7 = MagicMock()
        player_8 = MagicMock()
        player_9 = MagicMock()
        player_10 = MagicMock()
        return [player_1, player_2, player_3, player_4, player_5, player_6, player_7, player_8, player_9, player_10]
