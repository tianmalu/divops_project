#!/usr/bin/env python3
"""
Test script for start discussion with feedback context integration.
Tests that new discussions benefit from previous feedback contexts.
"""

import os
import sys
import json
from datetime import datetime
import uuid

# Add the genai directory to the path (parent of tests)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import requests
from app.rag_engine import start_discussion
from app.models import TarotCard
from app.weaviate_client import get_weaviate_client

def test_weaviate_connection():
    """Test if Weaviate is accessible."""
    try:
        client = get_weaviate_client()
        is_ready = client.is_ready()
        print(f"Weaviate is ready: {is_ready}")
        
        # Check if collections exist
        collections = {
            "Feedback": client.collections.exists("Feedback"),
            "KeywordMeaning": client.collections.exists("KeywordMeaning"),
            "ReadingContext": client.collections.exists("ReadingContext")
        }
        print(f"Collections status: {collections}")
        
        client.close()
        return is_ready
    except Exception as e:
        print(f"❌ Weaviate connection failed: {e}")
        return False

def create_test_cards():
    """Create test tarot cards."""
    from app.models import CardLayout
    return [
        CardLayout(name="The Fool", position="past", upright=True, meaning="freedom", position_keywords=["new beginnings"]),
        CardLayout(name="The Magician", position="present", upright=True, meaning="skill", position_keywords=["manifestation"]),
        CardLayout(name="The High Priestess", position="future", upright=True, meaning="wisdom", position_keywords=["intuition"])
    ]

def setup_feedback_context():
    print("🔧 Setting up feedback context via API...")
    BASE_URL = "http://localhost:8000/genai"  
    career_feedback = [
        {
            "user_id": "setup_user_1",
            "discussion_id": "setup_career_1",
            "feedback_text": "This reading was incredibly accurate! The advice about new beginnings and manifestation really helped me start my new project with confidence.",
            "rating": 5
        },
        {
            "user_id": "setup_user_2",
            "discussion_id": "setup_career_2",
            "feedback_text": "Perfect timing! The reading about trusting my intuition while taking action was exactly what I needed to hear before my job interview.",
            "rating": 4
        },
        {
            "user_id": "setup_user_3",
            "discussion_id": "setup_career_3",
            "feedback_text": "The reading about new beginnings and creative manifestation gave me the courage to start my own business. Very insightful!",
            "rating": 5
        }
    ]
    contexts_created = 0
    for fb_data in career_feedback:
        try:
            res = requests.post(f"{BASE_URL}/discussion/feedback", json=fb_data)
            if res.status_code == 200 and res.json().get("status") == "success":
                contexts_created += 1
                print(f"  ✅ Created context for: {fb_data['discussion_id']}")
            else:
                print(f"  ❌ Failed to create context: {res.text}")
        except Exception as e:
            print(f"  ❌ Error creating feedback: {e}")
    print(f"🔧 Setup complete! Created {contexts_created} feedback contexts.")
    return contexts_created > 0

def test_start_discussion_with_context():
    """Test starting a discussion and see if it uses feedback context."""
    print("\n🔮 Testing Start Discussion with Feedback Context")
    print("=" * 60)
    
    try:
        client = get_weaviate_client()
        
        # Test 1: Start discussion with similar question type
        print("\n📝 Test 1: Starting career-related discussion...")
        discussion = start_discussion(
            user_id="test_context_user",
            discussion_id= uuid.uuid4().hex, 
            initial_question="What should I focus on to grow my career?",
            client=client
        )
        
        print(f"✅ Discussion created: {discussion.discussion_id}")
        print(f"❓ Question: {discussion.initial_question}")
        print(f"🃏 Cards drawn: {[card.name for card in discussion.cards_drawn]}")
        # CardLayout fields check
        card = discussion.cards_drawn[0]
        assert hasattr(card, "name")
        assert hasattr(card, "position")
        assert hasattr(card, "upright")
        assert hasattr(card, "meaning")
        assert hasattr(card, "position_keywords")
        print(f"📖 Response length: {len(discussion.initial_response)} characters")
        
        # Check if response contains context enhancement indicators
        response_text = discussion.initial_response
        context_indicators = [
            "Context Enhancement",
            "Based on Similar Readings",
            "similar readings",
            "supported by",
            "high accuracy ratings"
        ]
        
        context_found = any(indicator in response_text for indicator in context_indicators)
        print(f"🔍 Context enhancement detected: {'✅ YES' if context_found else '❌ NO'}")
        
        if context_found:
            print("📚 Context enhancement found in response!")
            # Show a preview of the enhanced parts
            lines = response_text.split('\n')
            for i, line in enumerate(lines):
                if any(indicator in line for indicator in context_indicators):
                    print(f"  Enhanced section preview: {line[:100]}...")
                    break
        
        # Test 2: Start discussion with different question type
        print("\n📝 Test 2: Starting relationship-related discussion...")
        discussion2 = start_discussion(
            user_id="test_context_user_2",
            discussion_id=uuid.uuid4().hex,
            initial_question="What can I expect in my love life?",
            client=client
        )
        
        print(f"✅ Discussion created: {discussion2.discussion_id}")
        print(f"❓ Question: {discussion2.initial_question}")
        print(f"🃏 Cards drawn: {[card.name for card in discussion2.cards_drawn]}")
        card2 = discussion2.cards_drawn[0]
        assert hasattr(card2, "name")
        assert hasattr(card2, "position")
        assert hasattr(card2, "upright")
        assert hasattr(card2, "meaning")
        assert hasattr(card2, "position_keywords")
        
        # Check for context enhancement
        response_text2 = discussion2.initial_response
        context_found2 = any(indicator in response_text2 for indicator in context_indicators)
        print(f"🔍 Context enhancement detected: {'✅ YES' if context_found2 else '❌ NO'}")
        
        if not context_found2:
            print("📝 No context enhancement (expected for different question type)")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error testing start discussion: {e}")
        return False

def test_response_comparison():
    """Compare responses with and without context enhancement."""
    print("\n📊 Testing Response Quality Comparison")
    print("=" * 60)
    
    try:
        client = get_weaviate_client()
        
        # Create a baseline discussion (before feedback context)
        print("📝 Creating baseline discussion...")
        baseline_discussion = start_discussion(
            user_id="baseline_user",
            discussion_id=uuid.uuid4().hex,
            initial_question="How can I improve my professional skills?",
            client=client
        )
        
        print(f"📏 Baseline response length: {len(baseline_discussion.initial_response)} characters")
        # CardLayout fields check
        card = baseline_discussion.cards_drawn[0]
        assert hasattr(card, "name")
        assert hasattr(card, "position")
        assert hasattr(card, "upright")
        assert hasattr(card, "meaning")
        assert hasattr(card, "position_keywords")
        
        # Now add some feedback context via API
        print("\n🔧 Adding feedback context via API...")
        feedback_data = {
            "user_id": "context_builder",
            "discussion_id": "context_builder_discussion",
            "feedback_text": "This reading was very helpful! The advice about trusting my intuition when choosing skills to develop really resonated with me.",
            "rating": 5
        }
        BASE_URL = "http://localhost:8000/genai"
        try:
            res = requests.post(f"{BASE_URL}/discussion/feedback", json=feedback_data)
            if res.status_code == 200 and res.json().get("status") == "success":
                print("  ✅ Context feedback submitted via API.")
            else:
                print(f"  ❌ Failed to submit context feedback: {res.text}")
        except Exception as e:
            print(f"  ❌ Error submitting context feedback: {e}")
        
        # Create a new discussion with similar question
        print("📝 Creating context-enhanced discussion...")
        enhanced_discussion = start_discussion(
            user_id="enhanced_user",
            discussion_id=uuid.uuid4().hex,
            initial_question="What skills should I focus on developing?",
            client=client
        )
        
        print(f"📏 Enhanced response length: {len(enhanced_discussion.initial_response)} characters")
        card2 = enhanced_discussion.cards_drawn[0]
        assert hasattr(card2, "name")
        assert hasattr(card2, "position")
        assert hasattr(card2, "upright")
        assert hasattr(card2, "meaning")
        assert hasattr(card2, "position_keywords")
        
        # Compare responses
        baseline_len = len(baseline_discussion.initial_response)
        enhanced_len = len(enhanced_discussion.initial_response)
        
        print(f"\n📊 Comparison Results:")
        print(f"  • Baseline length: {baseline_len} characters")
        print(f"  • Enhanced length: {enhanced_len} characters")
        print(f"  • Difference: {enhanced_len - baseline_len} characters ({((enhanced_len - baseline_len) / baseline_len * 100):.1f}%)")
        
        # Check for enhancement indicators
        enhancement_indicators = ["Context Enhancement", "Based on Similar Readings", "supported by"]
        enhanced_has_context = any(indicator in enhanced_discussion.initial_response for indicator in enhancement_indicators)
        
        print(f"  • Context enhancement: {'✅ Present' if enhanced_has_context else '❌ Not detected'}")
        
        client.close()
        return enhanced_has_context
        
    except Exception as e:
        print(f"❌ Error in response comparison: {e}")
        return False

def main():
    """Run all tests."""
    print("🔮 Start Discussion with Feedback Context Test")
    print("=" * 70)
    
    # Test Weaviate connection
    if not test_weaviate_connection():
        print("❌ Cannot proceed without Weaviate connection")
        return
    
    # Set up feedback context
    if not setup_feedback_context():
        print("❌ Failed to set up feedback context")
        return
    
    # Test start discussion with context
    discussion_test = test_start_discussion_with_context()
    
    # Test response comparison
    comparison_test = test_response_comparison()
    
    # Summary
    print(f"\n📋 Test Results:")
    print(f"- Start discussion with context: {'✅ PASSED' if discussion_test else '❌ FAILED'}")
    print(f"- Response quality comparison: {'✅ PASSED' if comparison_test else '❌ FAILED'}")
    
    if discussion_test and comparison_test:
        print("\n🎉 All tests passed! Start discussion now utilizes feedback context.")
        print("🚀 New discussions benefit from previous user feedback!")
    else:
        print("\n⚠️ Some tests failed. Check the implementation.")

if __name__ == "__main__":
    main()
