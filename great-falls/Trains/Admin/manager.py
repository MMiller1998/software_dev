import itertools
from typing import List, Tuple

import Trains.Other.admin_utils as admin_utils
from Trains.Admin.referee import Referee
from Trains.Common.map import Map
from Trains.Other.interfaces.i_map_generator import IMapGenerator
from Trains.Other.interfaces.i_player import IPlayer


class Manager:
    """
    Represents a manager for Trains tournament. This class is responsible for running the tournament for the game Trains.

    Manager is reponsible for running the tournament and determing the tournament's winners. Manager also keeps track
    of cheaters in this tournament. The manager also picks a valid map, given from the players, which gets assigned
    to each game in the tournament.
    """

    @staticmethod
    def run_tournament(players: List[IPlayer], map_generator: IMapGenerator) -> Tuple[List[IPlayer], List[IPlayer]]:
        """
        Runs an entire tournament.
        :param players: all players participating in the tournament
        :param map_generator: the strategy to generate a map
        :return: a result of a tournament represented as a tuple of lists of winner and cheaters
        """
        all_cheaters = []
        tournament_map, setup_cheaters = Manager.setup_tournament(players, map_generator)
        active_players = Manager.__remove_players(players, setup_cheaters)
        winners, game_cheaters = Manager.run_rounds(active_players, tournament_map)
        all_cheaters = setup_cheaters + game_cheaters
        non_losers = winners + all_cheaters
        Manager.end_tournament(Manager.__remove_players(players, non_losers), winners)
        return winners, all_cheaters

    @staticmethod
    def setup_tournament(players: List[IPlayer], map_generator: IMapGenerator) -> Tuple[Map, List[IPlayer]]:
        """
        Informs the players that the tournament has started. 
        Sets up the tournament by choosing a valid map that will be used for the whole tournament.
        :param players: all players participating in the tournament
        :param map_generator: the strategy to generate a map
        :return: a map on which to play for the rest of the tournament
        """
        player_maps = []
        cheaters = []
        for player in players:
            try:
                player_maps.append(player.start(True))
            except:
                cheaters.append(player)
        tournament_map = Manager.__select_map(player_maps, map_generator)

        return tournament_map, cheaters

    @staticmethod
    def __select_map(player_maps: List[Map], map_generator: IMapGenerator) -> Map:
        """
        :param player_maps: maps to select from
        :param map_generator: the strategy to generate a map
        :return: a valid map from the given list of maps. If none valid then return a default map
        """
        valid_maps = [trains_map for trains_map in player_maps if
                      admin_utils.check_valid_map(trains_map, admin_utils.MAX_NUM_PLAYERS)]
        if valid_maps:
            return valid_maps[0]
        else:
            return map_generator.generate_map()

    @staticmethod
    def run_rounds(players: List[IPlayer], tournament_map: Map) -> Tuple[List[IPlayer], List[IPlayer]]:
        """
        Runs all round of the tournament. Distributes the number of players per game per round.
        :param players: all players participating in the tournament
        :param tournament_map: a map on which is used for all games in the tournament
        :return: the tournaments winners and cheaters
        """
        last_round_winners = []
        active_players = players
        all_cheaters = []
        while not Manager.__should_end_tournament(last_round_winners, active_players):
            winners, cheaters = Manager.__run_round(active_players, tournament_map)
            last_round_winners = active_players
            losers = Manager.__remove_players(active_players, winners)
            active_players = Manager.__remove_players(active_players, losers)
            all_cheaters += cheaters
        if admin_utils.check_enough_players(len(active_players)):
            winners, cheaters = Manager.__run_round(active_players, tournament_map)
            all_cheaters += cheaters
        return winners, all_cheaters

    @staticmethod
    def __remove_players(original_players: List[IPlayer], players_to_remove: List[IPlayer]) -> List[IPlayer]:
        """
        :return: the original players without players to remove 
        """
        return [player for player in original_players if player not in players_to_remove]

    @staticmethod
    def __run_round(active_players: List[IPlayer], tournament_map: Map) -> Tuple[List[IPlayer], List[IPlayer]]:
        """
        Runs a single round of the tournament.
        :param active_players: all currently active players
        :param tournament_map: a map on which is used for all games in this round
        :return: the round's winners in name order and cheaters in no order
        """
        player_groups = Manager.__distribute_players(active_players)
        round_game_results = [Referee.run_game(tournament_map, group) for group in player_groups]
        winners = list(itertools.chain(*[game_result.get_winners() for game_result in round_game_results]))
        cheaters = list(itertools.chain(*[game_result.get_cheaters() for game_result in round_game_results]))
        return winners, cheaters

    @staticmethod
    def __distribute_players(active_players: List[IPlayer]) -> List[List[IPlayer]]:
        """
        :param active_players: all players
        :return: players grouped into as many groups of the maximum number of players allowed per game as possible.
        If the final group of players has less than the minimum number of players required to play the game, then pull players 
        from the previous group until the minimum requirement is satisfied
        """
        player_groups = [active_players[i:i + admin_utils.MAX_NUM_PLAYERS] for i in
                         range(0, len(active_players), admin_utils.MAX_NUM_PLAYERS)]
        while len(player_groups[-1]) < admin_utils.MIN_NUM_PLAYERS:
            player_groups[-1].insert(0, player_groups[-2].pop())
        return player_groups

    @staticmethod
    def __should_end_tournament(last_round_winners: List[IPlayer], active_players: List[IPlayer]) -> bool:
        """
        Determines whether the tournament should end or not. If the length of two lists is the same or
        the number of players is less than or equal to the minimum number of players required to play a game, 
        the tournament should end.
        :param last_round_winners: players that have won during the last round
        :param active_players: all currently active players
        :return: whether the tournament should end
        """
        return len(last_round_winners) == len(active_players) or len(active_players) <= admin_utils.MAX_NUM_PLAYERS

    @staticmethod
    def end_tournament(losers: List[IPlayer], winners: List[IPlayer]) -> None:
        """
        Ends the tournament by notifying all non-cheating players whether or not they have won.
        :param losers: the players that have lost
        :param winners: the players that have won
        """
        for loser in losers:
            loser.end(False)

        for winner in winners:
            winner.end(True)
