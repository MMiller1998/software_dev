import itertools
from typing import List, Tuple, Dict

from Trains.Other.interfaces.i_player import IPlayer


class GameResult:
    """
    Represents the result of a Trains game

    Args:
        players (List[IPlayer]): an ordered list of the players who played in the game
        scores (List[int]): a list of scores whose ordering mirrors the players list
        cheaters (List[IPlayer]): a list of players who cheated and were removed from the game

    Attributes:
        __rankings (Dict[int, List[IPlayer]]): a dict of players by rank, where the keys are placements and the values
        are lists of the players with that placement
    """

    def __init__(self, players: List[IPlayer], scores: List[int], cheaters: List[IPlayer]):
        scores_to_players = []
        for i in range(len(players)):
            scores_to_players.append((scores[i], players[i]))
        sorted_player_scores = sorted(scores_to_players, key=lambda score_players_tuple: score_players_tuple[0],
                                      reverse=True)

        self.__rankings = self.__initialize_rankings(sorted_player_scores)
        self.cheaters = cheaters

    def get_winners(self) -> List[IPlayer]:
        if not self.__rankings:
            return []

        return self.__rankings[0]

    def get_rankings(self) -> List[List[IPlayer]]:
        return self.__rankings.copy()
    
    def get_cheaters(self) -> List[IPlayer]:
        return self.cheaters.copy()

    def __initialize_rankings(self, sorted_scores_to_players: List[Tuple[int, IPlayer]]) -> List[List[IPlayer]]:
        """
        :param sorted_scores_to_players: the tuple pairing a player to its score
        :return: a dictionary of placements to all the players with that placement
        """
        ranking = []
        if sorted_scores_to_players:
            previous_score = sorted_scores_to_players[0][0]
            players_with_same_score = []
            for score, player in sorted_scores_to_players:
                if score == previous_score:
                    players_with_same_score.append(player)
                else:
                    previous_score = score
                    ranking.append(players_with_same_score)
                    players_with_same_score = [player]
            ranking.append(players_with_same_score)

        return ranking
