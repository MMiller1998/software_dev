from collections import Counter
from typing import Dict, List
from Trains.Other.color import Color


class Cards:
    """
    Represents all the cards that a player or referee has

    Args:
        card_dict (Dict[Color, int]): a dictionary mapping the Color to its non-negative card count

    Attributes:
        __card_dict (Dict[Color, int]): a dictionary mapping the Color to its non-negative card count
    """
    __card_dict: Dict[Color, int]

    def __init__(self, card_dict: Dict[Color, int]):
        """
        Constructs an instance of Cards by copying the card_dict. If the card_dict is missing Colors, Cards will fill
        them in will a value of 0
        :param card_dict: a dictionary mapping the Color to its non-negative card count
        """
        if any(map(lambda count: count < 0, card_dict.values())):
            raise ValueError("Card counts must be non-negative")

        cards = {}
        for c in Color:
            cards[c] = card_dict.get(c, 0)

        self.__card_dict = cards

    def __eq__(self, other):
        return isinstance(other, Cards) and self.__card_dict == other.__card_dict

    def __hash__(self):
        return hash(tuple([(c, self.__card_dict[c]) for c in Color]))

    @staticmethod
    def from_list(card_list: List[Color]) -> 'Cards':
        return Cards(Counter(card_list))

    def get_card_count(self, color: Color) -> int:
        return self.__card_dict[color]

    def get_total_count(self) -> int:
        return sum(self.__card_dict.values())

    def add_cards(self, cards_to_add: 'Cards') -> 'Cards':
        return Cards({color: count + cards_to_add.get_card_count(color) for color, count in self.__card_dict.items()})

    def subtract_cards(self, color: Color, count: int) -> 'Cards':
        """
        This function assumes that there are sufficient cards to subtract from
        """
        return Cards({existing_color: existing_count - count if existing_color == color else existing_count for
                      existing_color, existing_count in self.__card_dict.items()})
