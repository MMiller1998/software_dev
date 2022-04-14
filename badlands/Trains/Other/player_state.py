from typing import Set
from Trains.Other.undirected_connection import UndirectedConnection
from Trains.Other.cards import Cards
from Trains.Other.destination import Destination


class PublicPlayerState:
    """
    Represents the portion of a player's state that is known to all players

    Args:
        acquired_connections (Set[UndirectedConnection]): the connections a player has acquired

    Attributes:
        acquired_connections (Set[UndirectedConnection]): the connections a player has acquired
    """
    acquired_connections: Set[UndirectedConnection]

    def __init__(self, acquired_connections: Set[UndirectedConnection]):
        self.acquired_connections = acquired_connections.copy()

    def __eq__(self, other):
        return isinstance(other, PublicPlayerState) and self.acquired_connections == other.acquired_connections

    def __hash__(self):
        return hash(tuple(sorted(self.acquired_connections)))

    def add_connection(self, connection: UndirectedConnection) -> 'PublicPlayerState':
        """
        :param connection: connection to acquire
        :return: a new public player state with the given connection added to self.acquired_connections
        """
        new_acquired_connections = self.acquired_connections.union({connection})
        return PublicPlayerState(new_acquired_connections)


class PrivatePlayerState:
    """
    Represents everything a player knows about his or her own state

    Args:
        cards (Cards): the cards this player has
        destinations (Set[Destination]): the destinations this player has
        num_rails (int): the number of rails this player has
        public_state (PublicPlayerState): the portion of this player's state that is public

    Attributes:
        cards (Cards): the cards this player has
        destinations (Set[Destination]): the destinations this player has
        num_rails (int): the number of rails this player has
        public_state (PublicPlayerState): the portion of this player's state that is public
    """

    NUM_DESTINATIONS = 2

    cards: Cards
    destinations: Set[Destination]
    num_rails: int
    public_state: PublicPlayerState

    def __init__(self, cards: Cards, destinations: Set[Destination],
                 num_rails: int, public_state: PublicPlayerState):
        """
        :raises ValueError: if the given number of rails is negative or if the length of destinations is not 2
        """
        if num_rails < 0:
            raise ValueError("num_rails must be non-negative")

        if len(destinations) != self.NUM_DESTINATIONS:
            raise ValueError("A player can only have 2 destinations")

        self.cards = cards
        self.destinations = destinations.copy()
        self.num_rails = num_rails
        self.public_state = public_state

    def __eq__(self, other):
        return isinstance(other,PrivatePlayerState) and \
               self.cards == other.cards and \
               self.destinations == other.destinations and \
               self.num_rails == other.num_rails and \
               self.public_state == other.public_state

    def __hash__(self):
        return hash((self.cards, tuple(self.destinations), self.num_rails, self.public_state))

    def draw_cards(self, drawn_cards: Cards) -> 'PrivatePlayerState':
        """
        Add the drawn cards to this player's deck of cards
        :param drawn_cards: drawn cards
        :return: a new private player state with the updated deck of cards
        """
        return PrivatePlayerState(self.cards.add_cards(drawn_cards), self.destinations, self.num_rails,
                                  self.public_state)

    def buy_connection(self, connection_to_buy: UndirectedConnection) -> 'PrivatePlayerState':
        """
        Buy the given connection for this player. This entails subtracting the correpsonding number of cards and rails
        and adding the connection to the player's acquired set of connections
        :param connection_to_buy: connection to buy
        :return: a new private player state with changes made from buying the connection
        """
        return PrivatePlayerState(self.cards.subtract_cards(connection_to_buy.color, connection_to_buy.length),
                                  self.destinations,
                                  self.num_rails - connection_to_buy.length,
                                  self.public_state.add_connection(connection_to_buy))
