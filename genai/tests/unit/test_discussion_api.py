#!/usr/bin/env python3
"""
Test script for the Discussion API endpoints
Run this script to test all discussion-related functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_discussion_api():
    """Test all discussion API endpoints"""
    
    print("🔮 Testing TarotAI Discussion API")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 2: Start a new discussion
    print("\n2. Starting a new discussion")
    start_discussion_data = {
        "user_id": "test_user_123",
        "initial_question": "What guidance do I need for my career path?",
        "topic": "Career Guidance"
    }
    
    response = requests.post(f"{BASE_URL}/discussion/start", json=start_discussion_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        discussion_data = response.json()
        discussion_id = discussion_data["discussion_id"]
        print(f"✅ Discussion created: {discussion_id}")
        print(f"Topic: {discussion_data['topic']}")
        print(f"Initial Question: {discussion_data['initial_question']}")
        print(f"Cards drawn: {len(discussion_data['cards_drawn'])}")
        print(f"Response preview: {discussion_data['initial_response'][:100]}...")
        
        # Test 3: Ask a followup question
        print("\n3. Asking a followup question")
        followup_data = {
            "question": "Can you provide more details about the present situation card?"
        }
        
        response = requests.post(f"{BASE_URL}/discussion/{discussion_id}/followup", json=followup_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            followup_response = response.json()
            print(f"✅ Followup answered: {followup_response['question_id']}")
            print(f"Question: {followup_response['question']}")
            print(f"Response preview: {followup_response['response'][:100]}...")
        else:
            print(f"❌ Followup failed: {response.text}")
        
        # Test 4: Get discussion details
        print("\n4. Getting discussion details")
        response = requests.get(f"{BASE_URL}/discussion/{discussion_id}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            details = response.json()
            print(f"✅ Discussion details retrieved")
            print(f"Topic: {details['topic']}")
            print(f"Cards: {len(details['cards_drawn'])}")
            print(f"History entries: {len(details['history'])}")
        else:
            print(f"❌ Get details failed: {response.text}")
        
        # Test 5: Get user discussions list
        print("\n5. Getting user discussions list")
        response = requests.get(f"{BASE_URL}/discussions/test_user_123")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            discussions = response.json()
            print(f"✅ User discussions retrieved: {len(discussions['discussions'])} discussions")
            for disc in discussions['discussions']:
                print(f"  - {disc['topic']} (ID: {disc['discussion_id'][:8]}...)")
        else:
            print(f"❌ Get user discussions failed: {response.text}")
    
    else:
        print(f"❌ Failed to start discussion: {response.text}")
    
    print("\n" + "=" * 50)
    print("🎯 Test completed!")

if __name__ == "__main__":
    test_discussion_api()
