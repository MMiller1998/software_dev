from typing import Iterator, FrozenSet, Optional, Iterable, Set, List

from trains.map import Destination
from trains.graph_traversals import get_longest_path_from_place_length
from trains.graph_elements import TrainConnection, TrainPlace
from trains.game.constants import (
    POINTS_PER_ACQUIRED_SEGMENT, POINTS_FOR_CONNECTED_DESTINATION,
    POINTS_FOR_DISCONNECTED_DESTINATION, STARTING_RAIL_COUNT
)
from trains.game.types import ScorePoint
from trains.state.cardsholder import CardDeck, CardHand, add_to_card_hand, remove_from_card_hand, EMPTY_HAND


class PlayerState:
    """
    A ``PlayerState`` has all information about the represented player,
    even the information that only the referee and the player themselves
    know.

    CONSTRAINT:
    Two `PlayerState` objects with the same `destinations` field are considered
    to represent the same player in a game.
    """

    def __init__(self, destinations: FrozenSet[Destination],
                 occupied: Optional[Iterable[TrainConnection]] = None,
                 cards: CardHand = EMPTY_HAND,
                 num_rails: int = STARTING_RAIL_COUNT):
        """
        Constructor for ``PlayerState``. The ``PlayerState`` starts with a default
        number of rails, defined in :const:`trains.game.constants.STARTING_RAIL_COUNT`,
        and an empty hand of colored cards.
        """
        if not occupied:
            occupied = frozenset()
        self._occupied: FrozenSet[TrainConnection] = frozenset(occupied)
        self.__destinations = destinations
        self.__cards: CardHand = cards
        self.__num_rails: int = num_rails

    def update(self,
               destinations: FrozenSet[Destination] = None,
               occupied: Iterable[TrainConnection] = None,
               cards: CardHand = None,
               num_rails: int = None
               ) -> 'PlayerState':
        return self.__class__(
            destinations=(destinations if destinations is not None else self.destinations),
            occupied=(occupied if occupied is not None else self.occupied),
            cards=(cards if cards is not None else self.cards),
            num_rails=(num_rails if num_rails is not None else self.num_rails)
        )

    @property
    def occupied(self):
        return self._occupied

    def occupies(self, connection: TrainConnection) -> bool:
        return connection in self.occupied

    def occupy(self, connection: TrainConnection) -> 'PlayerState':
        return self.__class__(self.occupied | {connection})

    @property
    def cards(self):
        return self.__cards.copy()

    @property
    def card_count(self):
        return sum(self.__cards.values())

    @property
    def num_rails(self):
        return self.__num_rails

    @property
    def destinations(self):
        return self.__destinations

    @property
    def seen_places(self) -> Set[TrainPlace]:
        """
        A set of ``TrainPlace``s that are part of any connection occupied by this ``PlayerState``.
        """
        seen = set()
        for conn in self.occupied:
            seen = seen.union(conn.get_places())
        return seen

    def acquirable_connections(self, possible_connections: Iterable[TrainConnection]) -> Iterator[TrainConnection]:
        """
        :return: all connections that can still be acquired
        """
        return filter(self.can_acquire, possible_connections)

    def can_acquire(self, connection: TrainConnection) -> bool:
        """
        :return: True if this player has enough cards and rails to acquire the *connection*
        """
        return self.num_rails >= connection.length and self.cards[connection.color] >= connection.length

    def give_cards(self, cards_to_give: CardDeck) -> 'PlayerState':
        return self.update(cards=add_to_card_hand(self.cards, cards_to_give))

    def occupy(self, connection: TrainConnection) -> 'PlayerState':
        """
        Deduct colored cards and rails to acquire the given :class:`TrainConnection`.

        :param connection: a connection which is not occupied by any player yet
        """
        return self._deduct_cost(connection).update(
            occupied=frozenset(self.occupied | {connection})
        )

    def _deduct_cost(self, connection: TrainConnection) -> 'PlayerState':
        """
        Take away the number of colored cards and rails for the given :class:`TrainConnection`'s length.
        """
        return self.update(
            num_rails=self.num_rails - connection.length,
            cards=remove_from_card_hand(
                self.cards,
                [connection.color] * connection.length,
            )
        )

    def points_for_acquired_segments(self) -> ScorePoint:
        """
        :return: the score for segments this `PlayerState` has acquired
        """
        return ScorePoint(sum(c.length for c in self.occupied) * POINTS_PER_ACQUIRED_SEGMENT)

    def _points_for_destination(self, destination: Destination) -> ScorePoint:
        """
        Returns the number of points that a player got/lost for connecting/not connecting a
        destination.
        """
        start, end = destination
        if self.places_are_connected(start, end):
            return POINTS_FOR_CONNECTED_DESTINATION
        return POINTS_FOR_DISCONNECTED_DESTINATION

    def points_for_destinations(self) -> ScorePoint:
        """
        Returns the total number of points a player earned or lost from their destinations
        """
        return ScorePoint(sum(self._points_for_destination(d) for d in self.destinations))

    def occupied_connections_from(self, origin: TrainPlace) -> Iterator[TrainConnection]:
        """
        :return: connections occupied by this `PlayerState` which originate from a given place
        """
        return filter(self.occupies, origin.get_connections())

    def unvisited_occupied_neighbors(self, current: TrainPlace, visited: Set[TrainPlace]
                                     ) -> Iterator[TrainPlace]:
        """
        :return: neighbors of current reachable by connections which are occupied by
            this `PlayerState` and not previously visited
        """
        return filter(
            lambda next_hop: next_hop not in visited,
            current.get_neighbors(connection_filter=self.occupied_connections_from(current))
        )

    def places_are_connected(self, start: TrainPlace, end: TrainPlace,
                             current: TrainPlace = None, visited: Set[TrainPlace] = None) -> bool:
        """
        Checks if this `PlayerState` has connected two given places with connections that it has acquired.

        :param player:
        :param start:
        :param end:
        :param current:
        :param visited: accumulator tracking which places have been visited previously
        :return: True if start and end are connected by connections which are occupied by the player
        """
        if not current:
            current = start
        if not visited:
            visited = set()

        if current == end:
            return True

        return any(map(
            lambda next_hop: self.places_are_connected(start, end, next_hop, visited | {current}),
            self.unvisited_occupied_neighbors(current, visited)
        ))

    def get_longest_path_length(self) -> int:
        """
        Calculate the number of segments in the longest continuous route occupied by this `PlayerState`.
        """
        if not self.seen_places:
            return 0
        return max((get_longest_path_from_place_length(place, self.occupied) for place in self.seen_places))

    def __repr__(self):
        return 'PlayerState'

    # PLEASE NOTE:
    # The player's cards are currently excluded from the hash and equality implementations.
    # This is simply because CardHand is currently represented as a dict, and there is no
    # immutable map type in Python. We would change this to be something that lends itself
    # better to hashing, but for the sake of time and due dates, the immediate solution is
    # to simply exclude the field and leave this note :)

    def __hash__(self):
        return hash((self.__destinations, self._occupied, self.__num_rails))

    def __eq__(self, other):
        return (
                isinstance(other, type(self))
                and other.occupied == self.occupied
                and other.destinations == self.destinations
                and other.num_rails == self.num_rails
        )


class PlayerStateWrapper:
    """
    A ``PlayerStateWrapper`` has all information a represented player, knows about
    the game, including the player's own state, and all opposing players' connections
    """

    def __init__(self, player_state: PlayerState, other_players_acquireds: List[List[TrainConnection]]) -> None:
        self.player_state = player_state
        self.other_player_acquireds = other_players_acquireds

    def get_unavailable_connections(self) -> Set[TrainConnection]:
        """
        Generate a set of all `TrainConnection`s owned by either the represented player or any other player.
        """
        return self.player_state.occupied.union(
            *[set(other_player_acquired) for other_player_acquired in self.other_player_acquireds]
        )
