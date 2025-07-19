import unittest
import random
from app.card_engine import draw_cards, interpret_card, layout_three_card
from app.models import TarotCard, CardLayout

class TestCardEngine(unittest.TestCase):

    def setUp(self):
        self.deck = [
            TarotCard(
                name=f"Card{i}",
                arcana="major",
                keywords=["keyword1", "keyword2"],
                meanings_light=[f"light{i}"],
                meanings_shadow=[f"shadow{i}"],
                fortune_telling=[]
            )
            for i in range(10)
        ]

    def test_draw_cards(self):
        picks = draw_cards(self.deck, 3)
        self.assertEqual(len(picks), 3)
        for card, upright in picks:
            self.assertIsInstance(card, TarotCard)
            self.assertIsInstance(upright, bool)

    def test_interpret_card(self):
        card = self.deck[0]
        meaning_light = interpret_card(card, upright=True)
        meaning_shadow = interpret_card(card, upright=False)
        self.assertEqual(meaning_light, card.meanings_light)
        self.assertEqual(meaning_shadow, card.meanings_shadow)

    def test_layout_three_card(self):
        layout = layout_three_card(self.deck)
        self.assertEqual(len(layout), 3)
        expected_positions = ["past", "present", "future"]
        for i, card_layout in enumerate(layout):
            self.assertIsInstance(card_layout, CardLayout)
            self.assertEqual(card_layout.position, expected_positions[i])
            assert isinstance(card_layout.meaning, str) 
            self.assertTrue(card_layout.name.startswith("Card"))

if __name__ == '__main__':
    unittest.main()
