#!/usr/bin/env python3
"""
Test script to verify the cards_drawn parsing fix
"""
import json
from typing import List
from datetime import datetime
import unittest

from app.models import CardLayout

def parse_cards_drawn(cards_drawn_str: str) -> List[CardLayout]:
    """
    Safely parse cards_drawn from Weaviate storage format.
    Handles JSON parsing errors, null values, and various data formats.
    """
    if not cards_drawn_str:
        return []
    cards_drawn = []
    try:
        cleaned_str = cards_drawn_str.replace("null", "null")
        cards_data = json.loads(cleaned_str.replace("'", '"'))
        if isinstance(cards_data, list):
            cards_drawn = [CardLayout(**card_data) for card_data in cards_data if card_data is not None]
        else:
            print(f"Warning: cards_drawn is not a list: {type(cards_data)}")
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error parsing cards_drawn as JSON: {e}")
        try:
            eval_str = cards_drawn_str.replace("null", "None")
            cards_data = eval(eval_str)
            if isinstance(cards_data, list):
                cards_drawn = [CardLayout(**card_data) for card_data in cards_data if card_data is not None]
            else:
                print(f"Warning: eval result is not a list: {type(cards_data)}")
        except Exception as e2:
            print(f"Error with eval fallback: {e2}")
            cards_drawn = []
    except Exception as e:
        print(f"Unexpected error parsing cards_drawn: {e}")
        cards_drawn = []
    return cards_drawn

# Test cases
class TestParseCardsDrawn(unittest.TestCase):
    def setUp(self):
        self.CardLayout = CardLayout
        self.parse_cards_drawn = parse_cards_drawn

    def test_json_with_null(self):
        test_json_with_null = '[{"name": "The Fool", "position": "past", "upright": true, "meaning": "New beginnings", "position_keywords": ["roots"]}, null, {"name": "The Magician", "position": "present", "upright": false, "meaning": "Blocked creativity", "position_keywords": ["focus"]}]'
        result = self.parse_cards_drawn(test_json_with_null)
        self.assertEqual(len(result), 2)

    def test_clean_json(self):
        test_json_clean = '[{"name": "The Fool", "position": "past", "upright": true, "meaning": "New beginnings", "position_keywords": ["roots"]}, {"name": "The Magician", "position": "present", "upright": false, "meaning": "Blocked creativity", "position_keywords": ["focus"]}]'
        result = self.parse_cards_drawn(test_json_clean)
        self.assertEqual(len(result), 2)

    def test_invalid_json(self):
        test_invalid_json = "{'name': 'The Fool', 'position': 'past', 'upright': True, 'meaning': 'New beginnings', 'position_keywords': ['roots']}"
        result = self.parse_cards_drawn(f"[{test_invalid_json}]")
        self.assertTrue(isinstance(result, list))

    def test_empty_string(self):
        result = self.parse_cards_drawn("")
        self.assertEqual(len(result), 0)

    def test_invalid_data(self):
        result = self.parse_cards_drawn("invalid data")
        self.assertEqual(len(result), 0)

if __name__ == "__main__":
    unittest.main()
