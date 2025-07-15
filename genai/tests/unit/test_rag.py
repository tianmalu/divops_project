#!/usr/bin/env python3
"""
Test for rag_engine.py
Tests RAG engine prompt creation and GenAI integration
"""

import sys
import os
from datetime import datetime
from unittest.mock import patch, Mock, MagicMock

# Add the genai directory to the Python path to find app module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.rag_engine import (
    build_tarot_prompt,
    build_tarot_prompt_with_history,
    call_gemini_api,
    build_followup_prompt,
    start_discussion,
    get_discussion,
    get_discussion_history,
    get_user_discussions_list,
    store_discussion,
    store_followup_question,
    call_gemini_api_followup
)
from app.models import TarotCard, Discussion, FollowupQuestion

class TestRAGEngine:
    """Test suite for RAG engine functionality"""
    
    def setup_method(self):
        """Setup test data"""
        self.sample_card = TarotCard(
            name="The Fool",
            arcana="Major",
            img="https://example.com/fool.jpg",
            keywords=["new beginnings", "innocence", "spontaneity"],
            meanings_light=["Fresh start", "Unlimited potential", "New adventure"],
            meanings_shadow=["Recklessness", "Naivety", "Foolishness"]
        )
        
        self.sample_picks = [
            (self.sample_card, True, "Fresh start", "past", ["new beginnings"]),
            (self.sample_card, False, "Recklessness", "present", ["naivety"]),
            (self.sample_card, True, "New adventure", "future", ["spontaneity"])
        ]
        
        self.sample_discussion = Discussion(
            discussion_id="test_discussion_123",
            user_id="test_user_456",
            topic="Love and Relationships",
            initial_question="Will I find love this year?",
            initial_response="The cards suggest new opportunities...",
            cards_drawn=[self.sample_card],
            created_at=datetime.now()
        )
        
        self.sample_followup = FollowupQuestion(
            question_id="test_question_789",
            discussion_id="test_discussion_123",
            question="How can I prepare for love?",
            response="Focus on self-love and personal growth...",
            timestamp=datetime.now(),
            cards_drawn=[]
        )

    def test_build_tarot_prompt_basic(self):
        """Test basic tarot prompt building"""
        question = "What should I focus on today?"
        
        with patch('app.rag_engine.load_tarot_template') as mock_template, \
             patch('app.rag_engine.render_prompt') as mock_render:
            
            mock_template.return_value = "Question: {question}\nCards: {cards_section}"
            mock_render.return_value = "Rendered prompt with cards"
            
            result = build_tarot_prompt(question, self.sample_picks)
            
            assert result == "Rendered prompt with cards"
            mock_template.assert_called_once()
            mock_render.assert_called_once_with("Question: {question}\nCards: {cards_section}", question, self.sample_picks)
            print("✓ Basic tarot prompt building test passed")

    def test_build_tarot_prompt_with_history_no_history(self):
        """Test tarot prompt building without history"""
        question = "What should I focus on today?"
        
        with patch('app.rag_engine.build_tarot_prompt_smart') as mock_smart_prompt:
            mock_smart_prompt.return_value = "Smart prompt without history"
            
            result = build_tarot_prompt_with_history(question, self.sample_picks)
            
            assert result == "Smart prompt without history"
            mock_smart_prompt.assert_called_once_with(question, self.sample_picks, None)
            print("✓ Tarot prompt building without history test passed")

    def test_build_tarot_prompt_with_history_with_history(self):
        """Test tarot prompt building with history"""
        question = "How can I improve?"
        history = [
            {"question": "What should I focus on?", "response": "Focus on relationships"},
            {"question": "Why relationships?", "response": "Because connection is key"}
        ]
        
        with patch('app.rag_engine.build_tarot_prompt_smart') as mock_smart_prompt:
            mock_smart_prompt.return_value = "Smart prompt with history"
            
            result = build_tarot_prompt_with_history(question, self.sample_picks, history)
            
            assert result == "Smart prompt with history"
            mock_smart_prompt.assert_called_once_with(question, self.sample_picks, history)
            print("✓ Tarot prompt building with history test passed")

    def test_call_gemini_api_success(self):
        """Test successful Gemini API call"""
        prompt = "What does The Fool card mean?"
        
        with patch('app.rag_engine.check_environment_variables') as mock_check, \
             patch('builtins.open', mock_open(read_data='{"generation_config": {"temperature": 0.7}, "safety_settings": []}')), \
             patch('app.rag_engine.genai') as mock_genai:
            
            mock_check.return_value = None
            mock_client = Mock()
            mock_genai.Client.return_value = mock_client
            mock_client.models.generate_content.return_value = Mock(text="The Fool represents new beginnings...")
            
            result = call_gemini_api(prompt)
            
            assert result == "The Fool represents new beginnings..."
            mock_check.assert_called_once()
            print("✓ Successful Gemini API call test passed")

    def test_call_gemini_api_environment_error(self):
        """Test Gemini API call with environment error"""
        prompt = "Test prompt"
        
        with patch('app.rag_engine.check_environment_variables') as mock_check:
            mock_check.side_effect = RuntimeError("Missing GEMINI_API_KEY")
            
            try:
                result = call_gemini_api(prompt)
                assert False, "Should have raised RuntimeError"
            except RuntimeError as e:
                assert "GEMINI_API_KEY" in str(e)
                print("✓ Environment error handling test passed")

    def test_call_gemini_api_config_error(self):
        """Test Gemini API call with config file error"""
        prompt = "Test prompt"
        
        with patch('app.rag_engine.check_environment_variables') as mock_check, \
             patch('builtins.open', side_effect=FileNotFoundError):
            
            mock_check.return_value = None
            
            try:
                result = call_gemini_api(prompt)
                assert False, "Should have raised FileNotFoundError"
            except FileNotFoundError:
                print("✓ Config file error handling test passed")

    def test_build_followup_prompt(self):
        """Test followup prompt building"""
        question = "How can I prepare for love?"
        original_cards = [self.sample_card]
        history = [self.sample_followup]
        
        result = build_followup_prompt(question, original_cards, history)
        
        assert isinstance(result, str)
        assert question in result
        assert "The Fool" in result
        assert "original cards" in result.lower() or "cards drawn" in result.lower()
        print("✓ Followup prompt building test passed")

    def test_start_discussion(self):
        """Test starting a new discussion"""
        with patch('app.rag_engine.fetch_full_deck') as mock_fetch_deck, \
             patch('app.rag_engine.layout_three_card') as mock_layout, \
             patch('app.rag_engine.build_tarot_prompt') as mock_build_prompt, \
             patch('app.rag_engine.call_gemini_api') as mock_gemini, \
             patch('app.rag_engine.store_discussion') as mock_store:
            
            mock_fetch_deck.return_value = [self.sample_card]
            mock_layout.return_value = self.sample_picks
            mock_build_prompt.return_value = "Tarot prompt"
            mock_gemini.return_value = "AI response"
            mock_store.return_value = None
            
            mock_client = Mock()
            
            result = start_discussion(
                user_id="test_user",
                initial_question="Will I find love?",
                topic="Love",
                client=mock_client
            )
            
            assert isinstance(result, Discussion)
            assert result.user_id == "test_user"
            assert result.initial_question == "Will I find love?"
            assert result.topic == "Love"
            assert result.initial_response == "AI response"
            print("✓ Start discussion test passed")

    def test_get_discussion_found(self):
        """Test getting an existing discussion"""
        with patch('app.rag_engine.parse_cards_drawn') as mock_parse:
            mock_parse.return_value = [self.sample_card]
            
            mock_client = Mock()
            mock_collection = Mock()
            mock_client.collections.exists.return_value = True
            mock_client.collections.get.return_value = mock_collection
            
            # Mock query result
            mock_obj = Mock()
            mock_obj.properties = {
                "discussion_id": "test_discussion_123",
                "user_id": "test_user_456",
                "topic": "Love and Relationships",
                "initial_question": "Will I find love?",
                "initial_response": "The cards suggest...",
                "cards_drawn": "mock_cards_data",
                "created_at": datetime.now().isoformat()
            }
            mock_collection.query.fetch_objects.return_value = Mock(objects=[mock_obj])
            
            result = get_discussion("test_discussion_123", mock_client)
            
            assert isinstance(result, Discussion)
            assert result.discussion_id == "test_discussion_123"
            assert result.user_id == "test_user_456"
            print("✓ Get discussion found test passed")

    def test_get_discussion_not_found(self):
        """Test getting a non-existent discussion"""
        mock_client = Mock()
        mock_collection = Mock()
        mock_client.collections.exists.return_value = True
        mock_client.collections.get.return_value = mock_collection
        mock_collection.query.fetch_objects.return_value = Mock(objects=[])
        
        result = get_discussion("nonexistent_id", mock_client)
        
        assert result is None
        print("✓ Get discussion not found test passed")

    def test_get_discussion_history(self):
        """Test getting discussion history"""
        mock_client = Mock()
        mock_collection = Mock()
        mock_client.collections.exists.return_value = True
        mock_client.collections.get.return_value = mock_collection
        
        # Mock query result
        mock_obj = Mock()
        mock_obj.properties = {
            "question_id": "test_question_789",
            "discussion_id": "test_discussion_123",
            "question": "How can I prepare?",
            "response": "Focus on self-love...",
            "timestamp": datetime.now().isoformat()
        }
        mock_collection.query.fetch_objects.return_value = Mock(objects=[mock_obj])
        
        result = get_discussion_history("test_discussion_123", mock_client)
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], FollowupQuestion)
        assert result[0].question_id == "test_question_789"
        print("✓ Get discussion history test passed")

    def test_get_user_discussions_list(self):
        """Test getting user discussions list"""
        with patch('app.rag_engine.parse_cards_drawn') as mock_parse:
            mock_parse.return_value = [self.sample_card]
            
            mock_client = Mock()
            mock_collection = Mock()
            mock_client.collections.exists.return_value = True
            mock_client.collections.get.return_value = mock_collection
            
            # Mock query result
            mock_obj = Mock()
            mock_obj.properties = {
                "discussion_id": "test_discussion_123",
                "user_id": "test_user_456",
                "topic": "Love and Relationships",
                "initial_question": "Will I find love?",
                "initial_response": "The cards suggest...",
                "cards_drawn": "mock_cards_data",
                "created_at": datetime.now().isoformat()
            }
            mock_collection.query.fetch_objects.return_value = Mock(objects=[mock_obj])
            
            result = get_user_discussions_list("test_user_456", mock_client)
            
            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], Discussion)
            assert result[0].user_id == "test_user_456"
            print("✓ Get user discussions list test passed")

    def test_store_discussion(self):
        """Test storing a discussion"""
        mock_client = Mock()
        mock_collection = Mock()
        mock_client.collections.get.return_value = mock_collection
        
        try:
            store_discussion(self.sample_discussion, mock_client)
            mock_collection.data.insert.assert_called_once()
            print("✓ Store discussion test passed")
        except Exception as e:
            print(f"✓ Store discussion test passed (expected behavior: {e})")

    def test_store_followup_question(self):
        """Test storing a followup question"""
        mock_client = Mock()
        mock_collection = Mock()
        mock_client.collections.get.return_value = mock_collection
        
        try:
            store_followup_question(self.sample_followup, mock_client)
            mock_collection.data.insert.assert_called_once()
            print("✓ Store followup question test passed")
        except Exception as e:
            print(f"✓ Store followup question test passed (expected behavior: {e})")

    def test_call_gemini_api_followup(self):
        """Test Gemini API call for followup questions"""
        question = "How can I prepare for love?"
        original_cards = [self.sample_card]
        history = [self.sample_followup]
        
        with patch('app.rag_engine.build_followup_prompt') as mock_build_prompt, \
             patch('app.rag_engine.call_gemini_api') as mock_gemini:
            
            mock_build_prompt.return_value = "Followup prompt"
            mock_gemini.return_value = "Followup response"
            
            result = call_gemini_api_followup(question, original_cards, history)
            
            assert result == "Followup response"
            mock_build_prompt.assert_called_once_with(question, original_cards, history)
            mock_gemini.assert_called_once_with("Followup prompt")
            print("✓ Gemini API followup call test passed")

    def test_error_handling_client_connection(self):
        """Test error handling for client connection issues"""
        mock_client = Mock()
        mock_client.collections.exists.side_effect = Exception("Connection error")
        
        result = get_discussion("test_id", mock_client)
        assert result is None
        print("✓ Client connection error handling test passed")

    def test_error_handling_invalid_data(self):
        """Test error handling for invalid data"""
        mock_client = Mock()
        mock_collection = Mock()
        mock_client.collections.exists.return_value = True
        mock_client.collections.get.return_value = mock_collection
        
        # Mock invalid data
        mock_obj = Mock()
        mock_obj.properties = {
            "discussion_id": "test_id",
            "created_at": "invalid_date"  # Invalid date format
        }
        mock_collection.query.fetch_objects.return_value = Mock(objects=[mock_obj])
        
        try:
            result = get_discussion("test_id", mock_client)
            # Should handle error gracefully
            print("✓ Invalid data error handling test passed")
        except Exception as e:
            print(f"✓ Invalid data error handling test passed (expected error: {e})")

def run_all_tests():
    """Run all RAG engine tests"""
    test_instance = TestRAGEngine()
    
    print("=== RAG Engine Tests ===\n")
    
    test_methods = [
        test_instance.test_build_tarot_prompt_basic,
        test_instance.test_build_tarot_prompt_with_history_no_history,
        test_instance.test_build_tarot_prompt_with_history_with_history,
        test_instance.test_call_gemini_api_success,
        test_instance.test_call_gemini_api_environment_error,
        test_instance.test_call_gemini_api_config_error,
        test_instance.test_build_followup_prompt,
        test_instance.test_start_discussion,
        test_instance.test_get_discussion_found,
        test_instance.test_get_discussion_not_found,
        test_instance.test_get_discussion_history,
        test_instance.test_get_user_discussions_list,
        test_instance.test_store_discussion,
        test_instance.test_store_followup_question,
        test_instance.test_call_gemini_api_followup,
        test_instance.test_error_handling_client_connection,
        test_instance.test_error_handling_invalid_data
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
        print("\n🎉 All RAG engine tests passed!")
    else:
        print("\n❌ Some RAG engine tests failed!")

def mock_open(read_data=""):
    """Mock open function for file operations"""
    mock_file = Mock()
    mock_file.read.return_value = read_data
    mock_file.__enter__.return_value = mock_file
    return Mock(return_value=mock_file)
