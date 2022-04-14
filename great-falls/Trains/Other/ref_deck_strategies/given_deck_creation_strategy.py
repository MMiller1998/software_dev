from typing import List

from Trains.Other.color import Color
from Trains.Other.interfaces.i_ref_deck_creation_strategy import IDeckCreationStrategy


class GivenDeckCreationStrategy(IDeckCreationStrategy):
    """
    A strategy to give a Referee a pregenerated deck of cards
    """

    def __init__(self, cards: List[Color]):
        """
        Create this strategy with the given deck
        :param cards: the cards the Referee should be given
        """
        self.cards = cards

    def create_deck(self, _: int) -> List[Color]:
        """
        :param _: size of deck (unused)
        :return: the deck given to this strategy during construction
        """
        return self.cards
