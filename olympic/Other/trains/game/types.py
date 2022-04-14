from typing import NewType, TypeVar, List, Set

ScorePoint = NewType('ScorePoint', int)

T = TypeVar('T')
Rank = Set[T]
# INTERPRETATION:
# A Rank represents a set of players which got the same score in a
# game of Trains.
# Rank takes a type argument for the player representation.

Ranking = List[Rank[T]]
# INTERPRETATION:
# A Ranking is a list where the ith inner collection contains all ith-place finishers.
# An ith-place finisher is a player that has the ith-highest score.
# Ranking takes a type argument for the player representation.
