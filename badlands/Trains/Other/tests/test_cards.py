import unittest
from Trains.Other.cards import Cards
from Trains.Other.color import Color

class CardTests(unittest.TestCase):
    CARDS = {Color.RED : 3, Color.BLUE : 4, Color.WHITE: 0, Color.GREEN: 10}

    def test_cards_constructor_valid(self):
        cards = Cards(self.CARDS)

        self.assertEqual(3, cards.get_card_count(Color.RED))
        self.assertEqual(4, cards.get_card_count(Color.BLUE))
        self.assertEqual(0, cards.get_card_count(Color.WHITE))
        self.assertEqual(10, cards.get_card_count(Color.GREEN))

    def test_cards_constructor_valid_missing_colors(self):
        cards = Cards({Color.RED: 10, Color.BLUE: 1})

        self.assertEqual(10, cards.get_card_count(Color.RED))
        self.assertEqual(1, cards.get_card_count(Color.BLUE))
        self.assertEqual(0, cards.get_card_count(Color.WHITE))
        self.assertEqual(0, cards.get_card_count(Color.GREEN))

    def test_cards_constructor_valid_empty(self):
        cards = Cards({})

        self.assertEqual(0, cards.get_card_count(Color.RED))
        self.assertEqual(0, cards.get_card_count(Color.BLUE))
        self.assertEqual(0, cards.get_card_count(Color.WHITE))
        self.assertEqual(0, cards.get_card_count(Color.GREEN))

    def test_cards_constructor_invalid_negative(self):
        with self.assertRaises(ValueError):
            Cards({Color.RED : -1, Color.BLUE : 4, Color.WHITE: 0, Color.GREEN: 10})

    def test_cards_from_list(self):
        card_list = [Color.RED, Color.BLUE, Color.GREEN, Color.WHITE]
        cards = Cards.from_list(card_list)
        for c in Color:
            self.assertEqual(1, cards.get_card_count(c))

    def test_eq(self):
        cards_1 = Cards(self.CARDS)
        cards_2 = Cards(self.CARDS)
        self.assertTrue(cards_2 == cards_1)

    def test_not_eq(self):
        cards_1 = Cards(self.CARDS)
        cards_2 = Cards({Color.RED : 0, Color.BLUE : 4, Color.WHITE: 1, Color.GREEN: 10})
        self.assertFalse(cards_2 == cards_1)

    def test_hash_eq(self):
        cards_1 = Cards(self.CARDS)
        cards_2 = Cards(self.CARDS)
        self.assertEqual(cards_2.__hash__(), cards_1.__hash__())

    def test_hash_not_eq(self):
        cards_1 = Cards(self.CARDS)
        cards_2 = Cards({Color.WHITE: 1, Color.BLUE : 4, Color.GREEN: 10})
        self.assertNotEqual(cards_2.__hash__(), cards_1.__hash__())

    def test_get_total_count(self):
        cards = Cards(self.CARDS)
        self.assertEqual(17, cards.get_total_count())

    def test_add_cards(self):
        cards = Cards(self.CARDS)
        new_cards = cards.add_cards(Cards({Color.RED: 2, Color.WHITE: 1}))

        self.assertEqual(5, new_cards.get_card_count(Color.RED))
        self.assertEqual(4, new_cards.get_card_count(Color.BLUE))
        self.assertEqual(1, new_cards.get_card_count(Color.WHITE))
        self.assertEqual(10, new_cards.get_card_count(Color.GREEN))

    def test_subtract_cards(self):
        cards = Cards(self.CARDS)
        new_cards = cards.subtract_cards(Color.RED, 2)

        self.assertEqual(1, new_cards.get_card_count(Color.RED))
        self.assertEqual(4, new_cards.get_card_count(Color.BLUE))
        self.assertEqual(0, new_cards.get_card_count(Color.WHITE))
        self.assertEqual(10, new_cards.get_card_count(Color.GREEN))
