#!/usr/bin/env python3
import requests
import time
from pprint import pprint

BASE_URL = "http://localhost:8000"

def test_health():
    print("\n✅ Testing /health")
    res = requests.get(f"{BASE_URL}/health")
    assert res.status_code == 200
    pprint(res.json())

def test_predict():
    print("\n✅ Testing /predict")
    res = requests.get(f"{BASE_URL}/predict", params={"question": "What should I focus on this month?", "user_id": "test_user"})
    assert res.status_code == 200
    pprint(res.json())

def test_daily_reading():
    print("\n✅ Testing /daily-reading")
    res = requests.get(f"{BASE_URL}/daily-reading", params={"user_id": "test_user"})
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
    assert res.status_code == 200
    pprint(res.json())

def test_get_discussion(discussion_id):
    print("\n✅ Testing /discussion/{id}")
    res = requests.get(f"{BASE_URL}/discussion/{discussion_id}")
    assert res.status_code == 200
    pprint(res.json())

def test_user_discussions(user_id="test_user"):
    print("\n✅ Testing /discussions/{user_id}")
    res = requests.get(f"{BASE_URL}/discussions/{user_id}")
    assert res.status_code == 200
    pprint(res.json())

def test_feedback(discussion_id):
    print("\n✅ Testing /feedback")
    payload = {
        "reading_id": f"{discussion_id}-reading",
        "user_id": "test_user",
        "question_id": "mock-question-id",
        "discussion_id": discussion_id,
        "feedback_text": "Very insightful reading, thank you!",
        "rating": 5,
        "helpful": True
    }
    res = requests.post(f"{BASE_URL}/feedback", json=payload)
    assert res.status_code == 200
    pprint(res.json())

if __name__ == "__main__":
    print("🔍 Running TarotAI API Integration Tests...")

    test_health()
    test_predict()
    test_daily_reading()

    discussion_id = test_start_discussion()
    time.sleep(1)  # Give backend time if async
    test_followup(discussion_id)
    test_get_discussion(discussion_id)
    test_user_discussions()
    test_feedback(discussion_id)

    print("\n🎯 All tests completed successfully.")
