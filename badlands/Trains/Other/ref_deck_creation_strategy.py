from typing import Union, List
import random

from Trains.Other.color import Color

class DeckCreationStrategy:
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


class RandomDeckCreationStrategy(DeckCreationStrategy):
    """
    A strategy for generating a deck randomly using the possible Color values.
    """
    def __init__(self, seed: Union[int, None] = None):
        """
        Create this strategy with a random number seed if desired
        :param seed: an optional number, representing a seed
        """
        if seed:
            random.seed(seed)

    def create_deck(self, num_cards: int) -> List[Color]:
        """
        Create a deck of the given size with randomly assigned colors from the Color enum
        :param num_cards: size of deck
        :return: a random list of color of size num_cards
        """
        colors = [c for c in Color]
        return [random.choice(colors) for _ in range(num_cards)]

