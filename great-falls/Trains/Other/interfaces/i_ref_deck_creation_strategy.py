from typing import List

from Trains.Other.color import Color


class IDeckCreationStrategy:
    """
    Represents a strategy to create a deck of colored cards. Extending classes must implement create_deck.
    """

    def create_deck(self, num_cards: int) -> List[Color]:
        """
        Create a deck (represented as a list of Color, where each color is a card) of the given size
        :param num_cards: the size of the deck to create
        :return: a list of Color representing a deck
        """
        raise NotImplementedError()
