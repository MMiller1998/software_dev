from typing import Iterable, List

from trains.graph_elements import TrainPlace, TrainConnection, Destination

# TODO refactor using list.sort(something, key=func)
# https://docs.python.org/3/howto/sorting.html


class LexicographicPairOfCities:
    """
    A ``LexicographicPairOfCities`` is a pair of :class:`TrainPlace` which can be
    compared lexicographically with other ``LexicographicPairOfCities``.

    Only the name of the city is relevant to lexicographic ordering.
    """
    def __init__(self, city1: TrainPlace, city2: TrainPlace):
        if city1.name > city2.name:
            city1, city2 = city2, city1
        self._city1 = city1
        self._city2 = city2

    def __cmp__(self, other: 'LexicographicPairOfCities'):

        if self._city1.name < other._city1.name:
            return -1
        if self._city1.name > other._city1.name:
            return +1

        if self._city2.name < other._city2.name:
            return -1
        if self._city2.name > other._city2.name:
            return +1

        return 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def to_destination(self) -> Destination:
        # it'd be better if Destination was the superclass to LexicographicPairOfCities,
        # but Destination is not a class.
        return frozenset((self._city1, self._city2,))


class LexicographicConnection:
    """
    Extends :class:`TrainConnection` to define lexicographic ordering,
    as specified in Milestone 5.
    """
    def __init__(self, c: TrainConnection):
        place1, place2 = c.get_places()
        self.__pair = LexicographicPairOfCities(place1, place2)
        self.original = c

    def __cmp__(self, other: 'LexicographicConnection'):
        cities_comparison = self.__pair.__cmp__(other.__pair)
        if cities_comparison != 0:
            return cities_comparison

        segments_comparison = self.original.length - other.original.length
        if segments_comparison != 0:
            return segments_comparison

        if self.original.color.value < other.original.color.value:
            return -1
        if self.original.color.value > other.original.color.value:
            return +1
        return 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return super().__eq__(other)
        return self.__cmp__(other) == 0

    def __hash__(self):
        return hash(self.original)


def lexicographically_sorted_places(places: Iterable[TrainPlace]) -> List[TrainPlace]:
    return sorted(places, key=lambda p: p.name)


def lexicographically_sorted_destinations(destinations: Iterable[Destination]) -> List[Destination]:
    sorted_lexicos = sorted([LexicographicPairOfCities(a, b) for a, b in destinations])
    return [lex.to_destination() for lex in sorted_lexicos]
