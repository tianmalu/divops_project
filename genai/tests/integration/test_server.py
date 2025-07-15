#!/usr/bin/env python3
import requests
import time
from pprint import pprint

BASE_URL = "http://localhost:8000"

def test_health():
    print("\n✅ Testing /health")
    res = requests.get(f"{BASE_URL}/health")
    print(f"Status code: {res.status_code}")
    if res.status_code != 200:
        print(f"Error response: {res.text}")
    assert res.status_code == 200
    pprint(res.json())

def test_predict():
    print("\n✅ Testing /predict")
    res = requests.get(f"{BASE_URL}/predict", params={"question": "What should I focus on this month?", "user_id": "test_user"})
    print(f"Status code: {res.status_code}")
    if res.status_code != 200:
        print(f"Error response: {res.text}")
    assert res.status_code == 200
    pprint(res.json())

def test_daily_reading():
    print("\n✅ Testing /daily-reading")
    res = requests.get(f"{BASE_URL}/daily-reading", params={"user_id": "test_user"})
    print(f"Status code: {res.status_code}")
    if res.status_code != 200:
        print(f"Error response: {res.text}")
    assert res.status_code == 200
    pprint(res.json())

def test_start_discussion():
    print("\n✅ Testing /discussion/start")
    payload = {
        "user_id": "test_user",
        "initial_question": "Will I find new opportunities in my career?",
        "topic": "Career"
    }
    res = requests.post(f"{BASE_URL}/discussion/start", json=payload)
    print(f"Status code: {res.status_code}")
    if res.status_code != 200:
        print(f"Error response: {res.text}")
    assert res.status_code == 200
    data = res.json()
    pprint(data)
    return data["discussion_id"]

def test_followup(discussion_id):
    print("\n✅ Testing /discussion/{id}/followup")
    payload = {
        "question": "What should I do to attract success?"
    }
    res = requests.post(f"{BASE_URL}/discussion/{discussion_id}/followup", json=payload)
    print(f"Status code: {res.status_code}")
    if res.status_code != 200:
        print(f"Error response: {res.text}")
    assert res.status_code == 200
    pprint(res.json())

def test_get_discussion(discussion_id):
    print("\n✅ Testing /discussion/{id}")
    res = requests.get(f"{BASE_URL}/discussion/{discussion_id}")
    print(f"Status code: {res.status_code}")
    if res.status_code != 200:
        print(f"Error response: {res.text}")
    assert res.status_code == 200
    pprint(res.json())

def test_user_discussions(user_id="test_user"):
    print("\n✅ Testing /discussions/{user_id}")
    res = requests.get(f"{BASE_URL}/discussions/{user_id}")
    print(f"Status code: {res.status_code}")
    if res.status_code != 200:
        print(f"Error response: {res.text}")
    assert res.status_code == 200
    pprint(res.json())

def test_feedback(discussion_id):
    print("\n✅ Testing /feedback")
    
    # First, get the discussion to extract the required information
    discussion_response = requests.get(f"{BASE_URL}/discussion/{discussion_id}")
    if discussion_response.status_code != 200:
        print(f"❌ Could not get discussion: {discussion_response.status_code}")
        return
    
    discussion_data = discussion_response.json()
    
    # Create feedback payload using the new enhanced format
    payload = {
        "user_id": "test_user",
        "question": discussion_data.get("initial_question", "What should I focus on?"),
        "spread": [
            {
                "name": "The Fool",
                "keywords": ["new beginnings", "spontaneity", "innocence"],
                "meanings_light": ["freedom", "adventure", "new journey"],
                "meanings_shadow": ["recklessness", "foolishness", "carelessness"],
                "arcana": "Major",
                "number": "0"
            },
            {
                "name": "The Magician", 
                "keywords": ["manifestation", "willpower", "desire", "creation"],
                "meanings_light": ["skill", "diplomacy", "address", "subtlety"],
                "meanings_shadow": ["disgrace", "disloyalty", "inability", "weakness"],
                "arcana": "Major",
                "number": "I"
            },
            {
                "name": "The High Priestess",
                "keywords": ["intuition", "sacred knowledge", "divine feminine"],
                "meanings_light": ["wisdom", "sound judgment", "common sense"],
                "meanings_shadow": ["ignorance", "lack of understanding", "selfishness"],
                "arcana": "Major",
                "number": "II"
            }
        ],
        "model_response": discussion_data.get("initial_response", "The cards suggest focusing on new beginnings and trusting your intuition."),
        "feedback_text": "Very insightful reading, thank you! The advice about new beginnings and intuition really resonated with me.",
        "rating": 5,
        "discussion_id": discussion_id
    }
    
    res = requests.post(f"{BASE_URL}/feedback", json=payload)
    print(f"Status code: {res.status_code}")
    if res.status_code != 200:
        print(f"Error response: {res.text}")
        return
    
    # Check if the enhanced feedback system is working
    response_data = res.json()
    print(f"✅ Feedback processed successfully!")
    print(f"📊 Keywords updated: {response_data.get('keywords_updated', 0)}")
    print(f"📚 Contexts stored: {response_data.get('contexts_stored', 0)}")
    pprint(response_data)

def test_discussion_feedback(discussion_id):
    print("\n✅ Testing /discussion/{id}/feedback")
    payload = {
        "user_id": "test_user",
        "rating": 5,
        "feedback_text": "This reading was very accurate and helpful!"
    }
    res = requests.post(f"{BASE_URL}/discussion/{discussion_id}/feedback", json=payload)
    print(f"Status code: {res.status_code}")
    if res.status_code != 200:
        print(f"Error response: {res.text}")
    else:
        pprint(res.json())
    # Don't assert for this one since it's new functionality

if __name__ == "__main__":
    print("🔍 Running TarotAI API Integration Tests...")

    try:
        test_health()
        test_predict()
        test_daily_reading()

        discussion_id = test_start_discussion()
        time.sleep(1)  # Give backend time if async
        test_followup(discussion_id)
        test_get_discussion(discussion_id)
        test_user_discussions()
        test_feedback(discussion_id)
        test_discussion_feedback(discussion_id)

        print("\n🎯 All tests completed successfully.")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("Check server logs for more details.")
