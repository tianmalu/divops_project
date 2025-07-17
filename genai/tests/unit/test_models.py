#!/usr/bin/env python3
"""
Test for models.py
Tests Pydantic model validation and data structures
"""

import sys
import os
from datetime import datetime
from typing import List
import unittest

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models import TarotCard, Discussion, FollowupQuestion

class TestModels(unittest.TestCase):
    """Test suite for Pydantic models validation"""
    
    def setUp(self):
        """Setup test data"""
        self.valid_card_data = {
            "name": "The Fool",
            "arcana": "Major",
            "img": "https://example.com/fool.jpg",
            "keywords": ["new beginnings", "innocence", "spontaneity"],
            "meanings_light": ["Fresh start", "Unlimited potential", "New adventure"],
            "meanings_shadow": ["Recklessness", "Naivety", "Foolishness"]
        }
        
        self.valid_discussion_data = {
            "discussion_id": "test_discussion_123",
            "user_id": "test_user_456",
            "initial_question": "Will I find love this year?",
            "initial_response": "The cards suggest new opportunities...",
            "cards_drawn": [],
            "created_at": datetime.now()
        }
        
        self.valid_followup_data = {
            "question_id": "test_question_789",
            "discussion_id": "test_discussion_123",
            "question": "How can I prepare for love?",
            "response": "Focus on self-love and personal growth...",
            "timestamp": datetime.now(),
            "cards_drawn": []
        }

    def test_tarot_card_valid_creation(self):
        """Test creating valid TarotCard"""
        card = TarotCard(**self.valid_card_data)
        
        self.assertEqual(card.name, "The Fool")
        self.assertEqual(card.arcana, "Major")
        self.assertEqual(card.img, "https://example.com/fool.jpg")
        self.assertEqual(len(card.keywords), 3)
        self.assertEqual(len(card.meanings_light), 3)
        self.assertEqual(len(card.meanings_shadow), 3)
        self.assertIn("new beginnings", card.keywords)
        self.assertIn("Fresh start", card.meanings_light)
        self.assertIn("Recklessness", card.meanings_shadow)

    def test_tarot_card_missing_required_fields(self):
        """Test TarotCard validation with missing required fields"""
        invalid_data = self.valid_card_data.copy()
        del invalid_data["name"]
        
        with self.assertRaises(Exception) as e:
            TarotCard(**invalid_data)
        self.assertIn("name", str(e.exception).lower())

    def test_tarot_card_invalid_arcana(self):
        """Test TarotCard with invalid arcana"""
        invalid_data = self.valid_card_data.copy()
        invalid_data["arcana"] = "Invalid"
        
        card = TarotCard(**invalid_data)
        self.assertEqual(card.arcana, "Invalid")

    def test_tarot_card_type_validation(self):
        """Test TarotCard type validation"""
        invalid_data = self.valid_card_data.copy()
        invalid_data["keywords"] = "not a list"
        
        with self.assertRaises(Exception) as e:
            TarotCard(**invalid_data)
        self.assertTrue("keywords" in str(e.exception).lower() or "list" in str(e.exception).lower())

    def test_discussion_valid_creation(self):
        """Test creating valid Discussion"""
        discussion = Discussion(**self.valid_discussion_data)
        
        self.assertEqual(discussion.discussion_id, "test_discussion_123")
        self.assertEqual(discussion.user_id, "test_user_456")
        self.assertEqual(discussion.initial_question, "Will I find love this year?")
        self.assertEqual(discussion.initial_response, "The cards suggest new opportunities...")
        self.assertIsInstance(discussion.cards_drawn, list)
        self.assertIsInstance(discussion.created_at, datetime)

    def test_discussion_missing_required_fields(self):
        """Test Discussion validation with missing required fields"""
        invalid_data = self.valid_discussion_data.copy()
        del invalid_data["user_id"]  # This is now required
        
        with self.assertRaises(Exception) as e:
            Discussion(**invalid_data)
        self.assertIn("user_id", str(e.exception).lower())

    def test_discussion_empty_strings(self):
        """Test Discussion validation with empty strings"""
        invalid_data = self.valid_discussion_data.copy()
        invalid_data["user_id"] = ""  # Test empty user_id
        
        discussion = Discussion(**invalid_data)
        self.assertEqual(discussion.user_id, "")

    def test_discussion_with_cards(self):
        """Test Discussion with CardLayout objects"""
        cardlayout_data = {
            "name": "The Fool",
            "position": "past",
            "upright": True,
            "meaning": "Fresh start",
            "position_keywords": ["roots"]
        }
        discussion_data = self.valid_discussion_data.copy()
        discussion_data["cards_drawn"] = [cardlayout_data]
        discussion = Discussion(**discussion_data)
        self.assertEqual(len(discussion.cards_drawn), 1)
        from app.models import CardLayout
        self.assertIsInstance(discussion.cards_drawn[0], CardLayout)
        self.assertEqual(discussion.cards_drawn[0].name, "The Fool")

    def test_followup_question_valid_creation(self):
        """Test creating valid FollowupQuestion"""
        followup = FollowupQuestion(**self.valid_followup_data)
        
        self.assertEqual(followup.question_id, "test_question_789")
        self.assertEqual(followup.discussion_id, "test_discussion_123")
        self.assertEqual(followup.question, "How can I prepare for love?")
        self.assertEqual(followup.response, "Focus on self-love and personal growth...")
        self.assertIsInstance(followup.timestamp, datetime)
        self.assertIsInstance(followup.cards_drawn, list)

    def test_followup_question_missing_fields(self):
        """Test FollowupQuestion validation with missing fields"""
        invalid_data = self.valid_followup_data.copy()
        del invalid_data["question"]  # This is truly required
        
        with self.assertRaises(Exception) as e:
            FollowupQuestion(**invalid_data)
        self.assertIn("question", str(e.exception).lower())

    def test_followup_question_long_text(self):
        """Test FollowupQuestion with very long text"""
        long_data = self.valid_followup_data.copy()
        long_data["question"] = "This is a very long question that goes on and on " * 50
        long_data["response"] = "This is a very long response that provides detailed guidance " * 100
        
        followup = FollowupQuestion(**long_data)
        self.assertTrue(len(followup.question) > 1000)
        self.assertTrue(len(followup.response) > 5000)

    def test_model_serialization(self):
        """Test model serialization to dict"""
        card = TarotCard(**self.valid_card_data)
        
        try:
            card_dict = card.model_dump()
            self.assertIsInstance(card_dict, dict)
            self.assertEqual(card_dict["name"], "The Fool")
            self.assertEqual(card_dict["arcana"], "Major")
            self.assertIsInstance(card_dict["keywords"], list)
        except Exception:
            card_dict = card.dict()
            self.assertIsInstance(card_dict, dict)
            self.assertEqual(card_dict["name"], "The Fool")

    def test_model_json_serialization(self):
        """Test model JSON serialization"""
        card = TarotCard(**self.valid_card_data)
        
        try:
            card_json = card.model_dump_json()
            self.assertIsInstance(card_json, str)
            self.assertIn("The Fool", card_json)
            self.assertIn("Major", card_json)
        except Exception:
            card_json = card.json()
            self.assertIsInstance(card_json, str)
            self.assertIn("The Fool", card_json)

    def test_datetime_validation(self):
        """Test datetime field validation"""
        discussion_data = self.valid_discussion_data.copy()
        discussion_data["created_at"] = "not a datetime"
        
        with self.assertRaises(Exception) as e:
            Discussion(**discussion_data)
        self.assertTrue("datetime" in str(e.exception).lower() or "timestamp" in str(e.exception).lower())

    def test_model_equality(self):
        """Test model equality comparison"""
        card1 = TarotCard(**self.valid_card_data)
        card2 = TarotCard(**self.valid_card_data)
        
        # Same data should be equal
        self.assertEqual(card1.name, card2.name)
        self.assertEqual(card1.arcana, card2.arcana)
        self.assertEqual(card1.keywords, card2.keywords)
        
        # Different data should not be equal
        different_data = self.valid_card_data.copy()
        different_data["name"] = "The Magician"
        card3 = TarotCard(**different_data)
        
        self.assertNotEqual(card1.name, card3.name)

    def test_model_immutability(self):
        """Test model immutability (if configured)"""
        card = TarotCard(**self.valid_card_data)
        
        try:
            # Try to modify the card
            card.name = "Modified Name"
        except Exception:
            pass

    def test_discussion_missing_user_id(self):
        """Test Discussion validation specifically with missing user_id"""
        invalid_data = self.valid_discussion_data.copy()
        del invalid_data["user_id"]
        
        with self.assertRaises(Exception) as e:
            Discussion(**invalid_data)
        self.assertIn("user_id", str(e.exception).lower())

    def test_discussion_empty_user_id(self):
        """Test Discussion validation with empty user_id"""
        invalid_data = self.valid_discussion_data.copy()
        invalid_data["user_id"] = ""
        
        discussion = Discussion(**invalid_data)
        self.assertEqual(discussion.user_id, "")

def run_all_tests():
    """Run all model tests"""
    test_instance = TestModels()
    
    print("=== Models Validation Tests ===\n")
    
    test_methods = [
        test_instance.test_tarot_card_valid_creation,
        test_instance.test_tarot_card_missing_required_fields,
        test_instance.test_tarot_card_type_validation,
        test_instance.test_discussion_valid_creation,
        test_instance.test_discussion_missing_required_fields,
        test_instance.test_discussion_missing_user_id,
        test_instance.test_discussion_empty_user_id,
        test_instance.test_discussion_empty_strings,
        test_instance.test_discussion_with_cards,
        test_instance.test_followup_question_valid_creation,
        test_instance.test_followup_question_missing_fields,
        test_instance.test_followup_question_long_text,
        test_instance.test_model_serialization,
        test_instance.test_model_json_serialization,
        test_instance.test_datetime_validation,
        test_instance.test_model_equality,
        test_instance.test_model_immutability
    ]
    
    passed = 0
    failed = 0
    
    for test_method in test_methods:
        try:
            test_instance.setUp()
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
    unittest.main()
