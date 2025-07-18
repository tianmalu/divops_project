#!/usr/bin/env python3
"""
Test script for the Discussion API endpoints
Run this script to test all discussion-related functionality
"""

import unittest
import requests
import json
import time
import uuid

BASE_URL = "http://localhost:8000/genai"

class TestDiscussionAPI(unittest.TestCase):
    def test_health_check(self):
        response = requests.get(f"{BASE_URL}/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json())

    def test_start_discussion_and_flow(self):
        start_discussion_data = {
            "user_id": "test_user_123",
            "discussion_id": uuid.uuid4().hex,  
            "initial_question": "What guidance do I need for my career path?",
        }
        response = requests.post(f"{BASE_URL}/discussion/start", json=start_discussion_data)
        self.assertEqual(response.status_code, 200, f"Failed to start discussion: {response.text}")
        discussion_data = response.json()
        discussion_id = discussion_data["discussion_id"]
        self.assertEqual(discussion_data["initial_question"], start_discussion_data["initial_question"])
        self.assertTrue(len(discussion_data["cards_drawn"]) > 0)
        self.assertTrue(len(discussion_data["initial_response"]) > 0)
        # CardLayout fields check
        card = discussion_data["cards_drawn"][0]
        self.assertIn("name", card)
        self.assertIn("position", card)
        self.assertIn("upright", card)
        self.assertIn("meaning", card)
        self.assertIn("position_keywords", card)

        # Followup question
        followup_data = {
            "question": "Can you provide more details about the present situation card?"
        }
        response = requests.post(f"{BASE_URL}/discussion/{discussion_id}/followup", json=followup_data)
        self.assertEqual(response.status_code, 200, f"Followup failed: {response.text}")
        followup_response = response.json()
        self.assertEqual(followup_response["question"], followup_data["question"])
        self.assertTrue(len(followup_response["response"]) > 0)


if __name__ == "__main__":
    unittest.main()
