#!/usr/bin/env python3
"""
Test script to verify the cards_drawn parsing fix
"""
import json
from typing import List
from datetime import datetime

# Mock TarotCard class for testing
class TarotCard:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f"TarotCard(name='{getattr(self, 'name', 'Unknown')}')"

def parse_cards_drawn(cards_drawn_str: str) -> List[TarotCard]:
    """
    Safely parse cards_drawn from Weaviate storage format.
    Handles JSON parsing errors, null values, and various data formats.
    """
    if not cards_drawn_str:
        return []
    
    cards_drawn = []
    try:
        # First try to parse as JSON
        # Handle null values in JSON by replacing with proper JSON null
        cleaned_str = cards_drawn_str.replace("null", "null")  # Keep as valid JSON null
        cards_data = json.loads(cleaned_str.replace("'", '"'))
        
        if isinstance(cards_data, list):
            # Filter out null values and create TarotCard objects
            cards_drawn = [TarotCard(**card_data) for card_data in cards_data if card_data is not None]
        else:
            print(f"Warning: cards_drawn is not a list: {type(cards_data)}")
            
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error parsing cards_drawn as JSON: {e}")
        # Fallback to eval if json fails
        try:
            # For eval, we need to handle null differently
            eval_str = cards_drawn_str.replace("null", "None")
            cards_data = eval(eval_str)
            if isinstance(cards_data, list):
                cards_drawn = [TarotCard(**card_data) for card_data in cards_data if card_data is not None]
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
def test_parse_cards_drawn():
    print("Testing parse_cards_drawn function...")
    
    # Test case 1: Valid JSON with null values
    test_json_with_null = '[{"name": "The Fool", "arcana": "Major"}, null, {"name": "The Magician", "arcana": "Major"}]'
    result1 = parse_cards_drawn(test_json_with_null)
    print(f"Test 1 - JSON with null: {result1}")
    assert len(result1) == 2, f"Expected 2 cards, got {len(result1)}"
    
    # Test case 2: Valid JSON without null
    test_json_clean = '[{"name": "The Fool", "arcana": "Major"}, {"name": "The Magician", "arcana": "Major"}]'
    result2 = parse_cards_drawn(test_json_clean)
    print(f"Test 2 - Clean JSON: {result2}")
    assert len(result2) == 2, f"Expected 2 cards, got {len(result2)}"
    
    # Test case 3: Invalid JSON (should fallback to eval)
    test_invalid_json = "{'name': 'The Fool', 'arcana': 'Major'}"
    result3 = parse_cards_drawn(f"[{test_invalid_json}]")
    print(f"Test 3 - Invalid JSON: {result3}")
    
    # Test case 4: Empty string
    result4 = parse_cards_drawn("")
    print(f"Test 4 - Empty string: {result4}")
    assert len(result4) == 0, f"Expected 0 cards, got {len(result4)}"
    
    # Test case 5: Completely invalid data
    result5 = parse_cards_drawn("invalid data")
    print(f"Test 5 - Invalid data: {result5}")
    assert len(result5) == 0, f"Expected 0 cards, got {len(result5)}"
    
    print("All tests passed! ✅")

if __name__ == "__main__":
    test_parse_cards_drawn()
