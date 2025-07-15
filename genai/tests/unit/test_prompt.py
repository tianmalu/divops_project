#!/usr/bin/env python3
"""
Test for prompt_loader.py
Tests render_prompt function and template loading
"""

import pytest
import sys
import os
from unittest.mock import patch, mock_open

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.prompt_loader import (
    load_tarot_template, 
    render_prompt, 
    build_tarot_prompt_smart,
    build_followup_prompt
)
from app.models import TarotCard

class TestPromptLoader:
    """Test suite for prompt_loader functionality"""
    
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
        
        self.sample_template = """
        Question: {question}
        
        Cards drawn:
        {cards_section}
        
        Interpretation: Based on the cards drawn, here is your tarot reading...
        """

    def test_load_tarot_template_success(self):
        """Test successful template loading"""
        mock_template_content = "Question: {question}\nCards: {cards_section}"
        
        with patch("builtins.open", mock_open(read_data=mock_template_content)):
            result = load_tarot_template()
            assert result == mock_template_content
            print("✓ Template loading test passed")

    def test_load_tarot_template_file_not_found(self):
        """Test template loading when file doesn't exist"""
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = load_tarot_template()
            # Should return default template
            assert "Question:" in result
            assert "{question}" in result
            print("✓ Template file not found handling test passed")

    def test_render_prompt_basic(self):
        """Test basic prompt rendering"""
        template = "Question: {question}\nCards: {cards_section}"
        question = "What does the future hold?"
        
        result = render_prompt(template, question, self.sample_picks)
        
        assert "Question: What does the future hold?" in result
        assert "The Fool" in result
        assert "Fresh start" in result
        assert "past" in result
        assert "present" in result
        assert "future" in result
        print("✓ Basic prompt rendering test passed")

    def test_render_prompt_with_upright_and_reversed(self):
        """Test prompt rendering with both upright and reversed cards"""
        template = "{cards_section}"
        question = "Test question"
        
        result = render_prompt(template, question, self.sample_picks)
        
        # Should contain both upright and reversed indicators
        assert "upright" in result.lower() or "reversed" in result.lower()
        assert "Fresh start" in result  # Upright meaning
        assert "Recklessness" in result  # Reversed meaning
        print("✓ Upright/reversed cards rendering test passed")

    def test_render_prompt_empty_picks(self):
        """Test prompt rendering with empty picks"""
        template = "Question: {question}\nCards: {cards_section}"
        question = "Test question"
        
        result = render_prompt(template, question, [])
        
        assert "Question: Test question" in result
        assert "cards_section" not in result  # Should be replaced even if empty
        print("✓ Empty picks rendering test passed")

    def test_build_tarot_prompt_smart_without_history(self):
        """Test smart prompt building without history"""
        question = "What should I focus on today?"
        
        result = build_tarot_prompt_smart(question, self.sample_picks)
        
        assert question in result
        assert "The Fool" in result
        assert len(result) > 100  # Should be a substantial prompt
        print("✓ Smart prompt building without history test passed")

    def test_build_tarot_prompt_smart_with_history(self):
        """Test smart prompt building with conversation history"""
        question = "How can I achieve this?"
        history = [
            {"question": "What should I focus on?", "response": "Focus on new beginnings"},
            {"question": "Why is this important?", "response": "Because change is coming"}
        ]
        
        result = build_tarot_prompt_smart(question, self.sample_picks, history)
        
        assert question in result
        assert "The Fool" in result
        assert "Focus on new beginnings" in result  # Should include history
        assert "change is coming" in result.lower()
        print("✓ Smart prompt building with history test passed")

    def test_build_followup_prompt(self):
        """Test followup prompt building"""
        question = "How can I prepare for this?"
        original_cards = [self.sample_card]
        history = [
            {"question": "Will I find love?", "response": "Yes, new beginnings await"}
        ]
        
        result = build_followup_prompt(question, original_cards, history)
        
        assert question in result
        assert "The Fool" in result
        assert "original cards" in result.lower() or "cards drawn" in result.lower()
        assert "Will I find love?" in result
        assert "new beginnings await" in result
        print("✓ Followup prompt building test passed")

    def test_render_prompt_special_characters(self):
        """Test prompt rendering with special characters"""
        template = "Question: {question}\nCards: {cards_section}"
        question = "What about my 'future' & success?"
        
        result = render_prompt(template, question, self.sample_picks)
        
        assert "What about my 'future' & success?" in result
        assert "The Fool" in result
        print("✓ Special characters handling test passed")

    def test_render_prompt_long_question(self):
        """Test prompt rendering with very long question"""
        template = "Question: {question}\nCards: {cards_section}"
        question = "This is a very long question that goes on and on about many different aspects of life including career, relationships, health, finances, spirituality, and personal growth. What guidance can you provide?"
        
        result = render_prompt(template, question, self.sample_picks)
        
        assert question in result
        assert "The Fool" in result
        assert len(result) > len(question)  # Should include cards info
        print("✓ Long question handling test passed")

    def test_template_placeholders_replacement(self):
        """Test that all template placeholders are properly replaced"""
        template = "Q: {question}\nCards: {cards_section}\nExtra: {unknown_placeholder}"
        question = "Test question"
        
        result = render_prompt(template, question, self.sample_picks)
        
        assert "{question}" not in result  # Should be replaced
        assert "{cards_section}" not in result  # Should be replaced
        assert "Test question" in result
        assert "The Fool" in result
        # {unknown_placeholder} might remain if not handled
        print("✓ Template placeholders replacement test passed")

    def test_cards_section_formatting(self):
        """Test that cards section is properly formatted"""
        template = "{cards_section}"
        question = "Test"
        
        result = render_prompt(template, question, self.sample_picks)
        
        # Should contain card positions
        assert "past" in result.lower()
        assert "present" in result.lower()
        assert "future" in result.lower()
        
        # Should contain card names
        assert "The Fool" in result
        
        # Should contain meanings
        assert "Fresh start" in result or "Recklessness" in result
        print("✓ Cards section formatting test passed")

def run_all_tests():
    """Run all prompt tests"""
    test_instance = TestPromptLoader()
    
    print("=== Prompt Loader Tests ===\n")
    
    test_methods = [
        test_instance.test_load_tarot_template_success,
        test_instance.test_load_tarot_template_file_not_found,
        test_instance.test_render_prompt_basic,
        test_instance.test_render_prompt_with_upright_and_reversed,
        test_instance.test_render_prompt_empty_picks,
        test_instance.test_build_tarot_prompt_smart_without_history,
        test_instance.test_build_tarot_prompt_smart_with_history,
        test_instance.test_build_followup_prompt,
        test_instance.test_render_prompt_special_characters,
        test_instance.test_render_prompt_long_question,
        test_instance.test_template_placeholders_replacement,
        test_instance.test_cards_section_formatting
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
        print("\n🎉 All prompt tests passed!")
    else:
        print("\n❌ Some prompt tests failed!")
