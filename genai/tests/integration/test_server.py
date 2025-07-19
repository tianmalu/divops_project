#!/usr/bin/env python3
import unittest
import requests
import time
from pprint import pprint
import uuid

BASE_URL = "http://localhost:8000/genai"

def get_discussion_id():
    payload = {
        "user_id": "test_user",
        "discussion_id": uuid.uuid4().hex,  
        "initial_question": "Will I find new opportunities in my career?",
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

    def test_daily_reading(self):
        res = requests.get(f"{BASE_URL}/daily-reading", params={"user_id": "test_user"})
        self.assertEqual(res.status_code, 200)
        self.assertIn("cards", res.json())

    def test_discussion_flow(self):
        # Start discussion
        discussion_id, discussion_data = get_discussion_id()
        self.assertEqual(discussion_data["initial_question"], "Will I find new opportunities in my career?")
        self.assertTrue(len(discussion_data["cards_drawn"]) > 0)
        self.assertTrue(len(discussion_data["initial_response"]) > 0)
        # CardLayout fields check
        card = discussion_data["cards_drawn"][0]
        self.assertIn("name", card)
        self.assertIn("position", card)
        self.assertIn("upright", card)
        self.assertIn("meaning", card)
        self.assertIn("position_keywords", card)

        # Followup with retry
        payload = {"question": "What should I do to attract success?"}
        max_retries = 5
        for i in range(max_retries):
            res = requests.post(f"{BASE_URL}/discussion/{discussion_id}/followup", json=payload)
            if res.status_code == 200:
                break
            time.sleep(2)
        else:
            self.fail(f"Followup failed after {max_retries} retries: {res.text}")

        self.assertIn("response", res.json())

if __name__ == "__main__":
    unittest.main()
