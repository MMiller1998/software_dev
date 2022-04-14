from typing import Dict, Iterable, List
from trains.graph_elements import RailColor

CardHand = Dict[RailColor, int]
"""
There is an entry for every RailColor. If no cards of that
color are held, the associated value is 0 

Interpretation: 
Cards in a player's hand
"""

CardDeck = List[RailColor]
# An ordered deck of cards to distribute


def add_to_card_hand(current_hand: CardHand, to_add: CardDeck) -> CardHand:
    new_hand = current_hand.copy()
    for color in to_add:
        new_hand[color] += 1
    return new_hand


def remove_from_card_hand(current_hand: CardHand, to_remove: CardDeck) -> CardHand:
    new_hand = current_hand.copy()
    for color in to_remove:
        new_hand[color] -= 1
    return new_hand


def create_hand(number_of_each: int = 0) -> CardHand:
    """
    :return:  a ``CardHand`` with ``n`` of each colored card. Creates empty pile by default.
    """
    return dict.fromkeys((e for e in RailColor), number_of_each)


def count_card_hand(cards: CardHand) -> int:
    return sum(cards.values())


def card_deck_to_card_hand(deck: CardDeck) -> CardHand:
    hand = dict()
    for c in RailColor:
        hand[c] = 0
    for card in deck:
        hand[card] += 1
    return hand


EMPTY_HAND = create_hand()
