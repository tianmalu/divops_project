#!/usr/bin/env python3
import unittest
import requests
import time
from pprint import pprint

BASE_URL = "http://localhost:8000"

def get_discussion_id():
    payload = {
        "user_id": "test_user",
        "initial_question": "Will I find new opportunities in my career?",
        "topic": "Career"
    }
    res = requests.post(f"{BASE_URL}/discussion/start", json=payload)
    assert res.status_code == 200
    data = res.json()
    return data["discussion_id"], data

class TestServerAPI(unittest.TestCase):
    def test_health(self):
        res = requests.get(f"{BASE_URL}/health")
        self.assertEqual(res.status_code, 200)
        self.assertIn("status", res.json())

    def test_predict(self):
        res = requests.get(f"{BASE_URL}/predict", params={"question": "What should I focus on this month?", "user_id": "test_user"})
        self.assertEqual(res.status_code, 200)
        # Accept either 'cards' or 'result' in response for compatibility
        response_json = res.json()
        self.assertTrue("cards" in response_json or "result" in response_json)

    def test_daily_reading(self):
        res = requests.get(f"{BASE_URL}/daily-reading", params={"user_id": "test_user"})
        self.assertEqual(res.status_code, 200)
        self.assertIn("cards", res.json())

    def test_discussion_flow(self):
        # Start discussion
        discussion_id, discussion_data = get_discussion_id()
        self.assertEqual(discussion_data["topic"], "Career")
        self.assertEqual(discussion_data["initial_question"], "Will I find new opportunities in my career?")
        self.assertTrue(len(discussion_data["cards_drawn"]) > 0)
        self.assertTrue(len(discussion_data["initial_response"]) > 0)
        time.sleep(1)
        # Followup
        payload = {"question": "What should I do to attract success?"}
        res = requests.post(f"{BASE_URL}/discussion/{discussion_id}/followup", json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertIn("response", res.json())
        # Get discussion
        res = requests.get(f"{BASE_URL}/discussion/{discussion_id}")
        self.assertEqual(res.status_code, 200)
        self.assertIn("topic", res.json())
        # User discussions
        res = requests.get(f"{BASE_URL}/discussions/test_user")
        self.assertEqual(res.status_code, 200)
        self.assertIn("discussions", res.json())

    def test_feedback(self):
        discussion_id, discussion_data = get_discussion_id()
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
        self.assertEqual(res.status_code, 200)
        self.assertIn("keywords_updated", res.json())
        self.assertIn("contexts_stored", res.json())

    def test_discussion_feedback(self):
        discussion_id, _ = get_discussion_id()
        payload = {
            "user_id": "test_user",
            "rating": 5,
            "feedback_text": "This reading was very accurate and helpful!"
        }
        res = requests.post(f"{BASE_URL}/discussion/{discussion_id}/feedback", json=payload)
        self.assertEqual(res.status_code, 200)
        # Accept either 'feedback_text' or 'message' in response for compatibility
        response_json = res.json()
        self.assertTrue("feedback_text" in response_json or "message" in response_json)

if __name__ == "__main__":
    unittest.main()
