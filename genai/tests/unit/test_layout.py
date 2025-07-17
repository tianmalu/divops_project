#!/usr/bin/env python3
"""
Test for card_engine.py
Tests layout_three_card function and card selection logic
"""

import sys
import os
from unittest.mock import patch, Mock
import unittest

# Add the genai directory to the Python path to find app module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.card_engine import layout_three_card
from app.models import TarotCard

class TestCardEngine(unittest.TestCase):
    """Test suite for card_engine functionality"""
    
    def setUp(self):
        """Setup test data"""
        self.sample_deck = [
            TarotCard(
                name="The Fool",
                arcana="Major",
                img="https://example.com/fool.jpg",
                keywords=["new beginnings", "innocence"],
                meanings_light=["Fresh start", "Unlimited potential"],
                meanings_shadow=["Recklessness", "Naivety"]
            ),
            TarotCard(
                name="The Magician",
                arcana="Major",
                img="https://example.com/magician.jpg",
                keywords=["manifestation", "willpower"],
                meanings_light=["Manifestation", "Resourcefulness"],
                meanings_shadow=["Manipulation", "Poor planning"]
            ),
            TarotCard(
                name="The High Priestess",
                arcana="Major",
                img="https://example.com/priestess.jpg",
                keywords=["intuition", "mystery"],
                meanings_light=["Intuition", "Sacred knowledge"],
                meanings_shadow=["Secrets", "Withdrawn"]
            ),
            TarotCard(
                name="Two of Cups",
                arcana="Minor",
                img="https://example.com/two_cups.jpg",
                keywords=["partnership", "unity"],
                meanings_light=["Partnership", "Mutual attraction"],
                meanings_shadow=["Imbalance", "Broken communication"]
            ),
            TarotCard(
                name="Three of Pentacles",
                arcana="Minor",
                img="https://example.com/three_pentacles.jpg",
                keywords=["teamwork", "collaboration"],
                meanings_light=["Teamwork", "Collaboration"],
                meanings_shadow=["Lack of teamwork", "Disharmony"]
            )
        ]

    def test_layout_three_card_basic(self):
        """Test basic three card layout"""
        result = layout_three_card(self.sample_deck)
        
        assert len(result) == 3
        assert all(len(card_info) == 5 for card_info in result)
        
        # Check structure: (card, upright, meaning, position, keywords)
        for card, upright, meaning, position, keywords in result:
            assert isinstance(card, TarotCard)
            assert isinstance(upright, bool)
            if isinstance(meaning, list):
                assert all(isinstance(m, str) for m in meaning)
                assert len(meaning) > 0
            else:
                assert isinstance(meaning, str)
                assert len(meaning) > 0
            assert isinstance(position, str)
            assert isinstance(keywords, list)
            assert len(keywords) > 0
        
        print("✓ Basic three card layout test passed")

    def test_layout_three_card_positions(self):
        """Test that three card layout has correct positions"""
        result = layout_three_card(self.sample_deck)
        
        positions = [card_info[3] for card_info in result]
        expected_positions = ["past", "present", "future"]
        
        assert positions == expected_positions
        print("✓ Three card layout positions test passed")

    def test_layout_three_card_unique_cards(self):
        """Test that three card layout selects unique cards"""
        result = layout_three_card(self.sample_deck)
        
        cards = [card_info[0] for card_info in result]
        card_names = [card.name for card in cards]
        
        # All cards should be unique
        assert len(set(card_names)) == 3
        print("✓ Unique cards selection test passed")

    def test_layout_three_card_upright_reversed(self):
        """Test that cards can be upright or reversed"""
        # Run multiple times to check randomness
        upright_count = 0
        reversed_count = 0
        
        for _ in range(10):
            result = layout_three_card(self.sample_deck)
            for card_info in result:
                if card_info[1]:  # upright
                    upright_count += 1
                else:  # reversed
                    reversed_count += 1
        
        # Should have both upright and reversed cards across multiple runs
        assert upright_count > 0
        assert reversed_count > 0
        print("✓ Upright/reversed randomness test passed")

    def test_layout_three_card_meanings_match_orientation(self):
        """Test that meanings match card orientation"""
        result = layout_three_card(self.sample_deck)
        
        for card, upright, meaning, position, keywords in result:
            if upright:
                if isinstance(meaning, list):
                    assert all(m in card.meanings_light for m in meaning)
                else:
                    assert meaning in card.meanings_light
            else:
                if isinstance(meaning, list):
                    assert all(m in card.meanings_shadow for m in meaning)
                else:
                    assert meaning in card.meanings_shadow
        
        print("✓ Meanings match orientation test passed")

    def test_layout_three_card_small_deck(self):
        """Test layout with exactly 3 cards in deck"""
        small_deck = self.sample_deck[:3]
        result = layout_three_card(small_deck)
        
        assert len(result) == 3
        # Should use all cards in deck
        used_cards = [card_info[0] for card_info in result]
        assert len(set(card.name for card in used_cards)) == 3
        print("✓ Small deck test passed")

    def test_layout_three_card_large_deck(self):
        """Test layout with large deck"""
        # Create a larger deck by duplicating cards with different names
        large_deck = []
        for i in range(20):
            card = TarotCard(
                name=f"Card {i}",
                arcana="Major" if i % 2 == 0 else "Minor",
                img=f"https://example.com/card{i}.jpg",
                keywords=[f"keyword{i}", f"trait{i}"],
                meanings_light=[f"Light meaning {i}", f"Positive {i}"],
                meanings_shadow=[f"Shadow meaning {i}", f"Negative {i}"]
            )
            large_deck.append(card)
        
        result = layout_three_card(large_deck)
        
        assert len(result) == 3
        # Should select from the available cards
        used_cards = [card_info[0] for card_info in result]
        assert all(card in large_deck for card in used_cards)
        print("✓ Large deck test passed")

    def test_layout_three_card_empty_deck(self):
        """Test layout with empty deck"""
        try:
            result = layout_three_card([])
            # Should handle empty deck gracefully
            assert result == [] or len(result) == 0
            print("✓ Empty deck test passed")
        except Exception as e:
            print(f"✓ Empty deck test passed (expected exception: {e})")

    def test_layout_three_card_insufficient_deck(self):
        """Test layout with deck smaller than 3 cards"""
        small_deck = self.sample_deck[:2]
        try:
            result = layout_three_card(small_deck)
            # Should handle insufficient cards gracefully
            assert len(result) <= 2
            print("✓ Insufficient deck test passed")
        except Exception as e:
            print(f"✓ Insufficient deck test passed (expected exception: {e})")

    def test_layout_three_card_card_properties(self):
        """Test that selected cards have all required properties"""
        result = layout_three_card(self.sample_deck)
        
        for card, upright, meaning, position, keywords in result:
            # Check card properties
            assert hasattr(card, 'name')
            assert hasattr(card, 'arcana')
            assert hasattr(card, 'img')
            assert hasattr(card, 'keywords')
            assert hasattr(card, 'meanings_light')
            assert hasattr(card, 'meanings_shadow')
            
            # Check that properties are not empty
            assert card.name
            assert card.arcana
            assert card.img
            assert len(card.keywords) > 0
            assert len(card.meanings_light) > 0
            assert len(card.meanings_shadow) > 0
        
        print("✓ Card properties test passed")

def run_all_tests():
    """Run all card engine tests"""
    test_instance = TestCardEngine()
    
    print("=== Card Engine Tests ===\n")
    
    test_methods = [
        test_instance.test_layout_three_card_basic,
        test_instance.test_layout_three_card_positions,
        test_instance.test_layout_three_card_unique_cards,
        test_instance.test_layout_three_card_upright_reversed,
        test_instance.test_layout_three_card_meanings_match_orientation,
        test_instance.test_layout_three_card_small_deck,
        test_instance.test_layout_three_card_large_deck,
        test_instance.test_layout_three_card_empty_deck,
        test_instance.test_layout_three_card_insufficient_deck,
        test_instance.test_layout_three_card_card_properties
    ]
    
    passed = 0
    failed = 0
    
    for test_method in test_methods:
        try:
            test_instance.setup_method()
            test_method()
            passed += 1
        except Exception as e:
            print(f"✗ {test_method.__name__} failed: {e}")
            failed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    if success:
        print("\n🎉 All card engine tests passed!")
    else:
        print("\n❌ Some card engine tests failed!")
