from typing import List
from collections import defaultdict

from Trains.Player.player import Player


class GameResult:
    """
    Represents the result of a Trains game

    Args:
        players (List[Player]): an ordered list of the players who played in the game
        scores (List[int]): a list of scores whose ordering mirrors the players list
        cheaters (List[Player]): a list of players who cheated and were removed from the game

    Attributes:
        rankings (List[List[Player]]): a list of list of players ordered by rank, where the first element of the list
                                       is all the players ranked number 1
    """
    def __init__(self, players: List[Player], scores: List[int], cheaters: List[Player]):
        scores_to_players = defaultdict(list)
        for i in range(len(players)):
            scores_to_players[scores[i]].append(players[i])

        sorted_player_scores = sorted(scores_to_players.items(), key=lambda score_players_tuple: score_players_tuple[0],
                                      reverse=True)

        self.__rankings = list(map(lambda score_player_tuple: score_player_tuple[1], sorted_player_scores))
        self.cheaters = cheaters

    def get_winners(self) -> List[Player]:
        if not self.__rankings:
            return []

        return self.__rankings[0]
