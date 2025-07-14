import requests
import json
import time
import threading

BASE_URL = "http://localhost:8000"

def test_basic_endpoints():
    """Test basic endpoints of the TarotAI API."""
    print("🧪 Testing TarotAI API...")
    
    # 1. Health Check
    print("\n1. Health Check:")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data.get('status')}")
            print(f"   ✅ Version: {data.get('version')}")
            print(f"   ✅ Timestamp: {data.get('timestamp')}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 2. Basic Prediction (Scenario 0 - Simple Question)
    print("\n2. Basic Prediction (Simple Question):")
    try:
        response = requests.get(f"{BASE_URL}/predict", 
                              params={"question": "What does my future hold?"})
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Has result: {'result' in result}")
            print(f"   ✅ Result length: {len(result.get('result', ''))}")
            print(f"   📝 Result preview: {result.get('result', '')[:150]}...")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 3. Daily Reading (Scenario 1 - 3-card spread)
    print("\n3. Daily Reading (3-card spread):")
    try:
        response = requests.get(f"{BASE_URL}/daily-reading")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Cards Count: {len(result.get('cards', []))}")
            print(f"   ✅ Has answer: {'answer' in result}")
            print(f"   ✅ Has question: {'question' in result}")
            print(f"   ✅ Reading type: {result.get('reading_type', 'N/A')}")
            
            cards = result.get('cards', [])
            if cards:
                first_card = cards[0]
                print(f"   🃏 First Card: {first_card.get('name', 'N/A')}")
                print(f"   🃏 Upright: {first_card.get('upright', 'N/A')}")
                print(f"   🃏 Position: {first_card.get('position', 'N/A')}")
                print(f"   🃏 Arcana: {first_card.get('arcana', 'N/A')}")
                print(f"   🃏 Has image_url: {'image_url' in first_card}")
            
            answer = result.get('answer', '')
            print(f"   📝 Answer length: {len(answer)}")
            print(f"   📝 Answer preview: {answer[:100]}...")
            
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 4. Daily Reading with User ID
    print("\n4. Daily Reading with User ID:")
    try:
        response = requests.get(f"{BASE_URL}/daily-reading", 
                              params={"user_id": "test_user_123"})
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Cards Count: {len(result.get('cards', []))}")
            print(f"   ✅ Same structure as anonymous: {set(result.keys())}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_custom_ask_endpoint():
    """Test the custom ask endpoint with POST requests."""
    print("\n🔮 Testing Custom Ask Endpoint...")
    
    # Test different question types
    test_questions = [
        "Should I change my career?",
        "What does my love life look like?",
        "How can I improve my finances?",
        "What should I focus on this month?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Custom Ask: '{question}'")
        try:
            response = requests.post(f"{BASE_URL}/ask", 
                                   json={"question": question})
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Has question: {'question' in result}")
                print(f"   ✅ Cards Count: {len(result.get('cards', []))}")
                print(f"   ✅ Has interpretation: {'interpretation' in result}")
                print(f"   ✅ Reading type: {result.get('reading_type', 'N/A')}")
                print(f"   ✅ Has discussion_id: {'discussion_id' in result}")
                print(f"   ✅ Is followup: {result.get('is_followup', False)}")
                
                # Check card structure
                cards = result.get('cards', [])
                if cards:
                    first_card = cards[0]
                    print(f"   🃏 First Card: {first_card.get('name', 'N/A')}")
                    print(f"   🃏 Position: {first_card.get('position', 'N/A')}")
                
                answer = result.get('interpretation', '')
                print(f"   📝 Answer length: {len(answer)}")
                print(f"   📝 Question echoed: {result.get('question') == question}")
                
            else:
                print(f"   ❌ Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_discussion_functionality():
    """Test discussion creation and followup questions."""
    print("\n💬 Testing Discussion Functionality...")
    
    # 5. Create a new discussion
    print("\n5. Create New Discussion:")
    discussion_id = None
    try:
        response = requests.post(f"{BASE_URL}/ask", 
                               json={
                                   "question": "What should I focus on in my career?",
                                   "user_id": "test_user_discussion"
                               })
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            discussion_id = result.get('discussion_id')
            print(f"   ✅ Discussion created: {discussion_id}")
            print(f"   ✅ Is followup: {result.get('is_followup', False)}")
            print(f"   ✅ Has cards: {len(result.get('cards', []))}")
            print(f"   ✅ Has interpretation: {'interpretation' in result}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 6. Test followup question using /ask endpoint
    if discussion_id:
        print(f"\n6. Followup Question via /ask (Discussion: {discussion_id}):")
        try:
            response = requests.post(f"{BASE_URL}/ask", 
                                   json={
                                       "question": "How can I overcome the challenges mentioned?",
                                       "discussion_id": discussion_id,
                                       "user_id": "test_user_discussion"
                                   })
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Same discussion_id: {result.get('discussion_id') == discussion_id}")
                print(f"   ✅ Is followup: {result.get('is_followup', False)}")
                print(f"   ✅ Has new cards: {len(result.get('cards', []))}")
                print(f"   ✅ Has interpretation: {'interpretation' in result}")
            else:
                print(f"   ❌ Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # 7. Test dedicated followup endpoint
    if discussion_id:
        print(f"\n7. Dedicated Followup Endpoint (Discussion: {discussion_id}):")
        try:
            response = requests.post(f"{BASE_URL}/followup", 
                                   json={
                                       "discussion_id": discussion_id,
                                       "question": "What specific steps should I take next?",
                                       "user_id": "test_user_discussion"
                                   })
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Same discussion_id: {result.get('discussion_id') == discussion_id}")
                print(f"   ✅ Has question_id: {'question_id' in result}")
                print(f"   ✅ Has cards: {len(result.get('cards', []))}")
                print(f"   ✅ Has interpretation: {'interpretation' in result}")
                print(f"   ✅ Previous context: {result.get('previous_context', 0)}")
            else:
                print(f"   ❌ Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # 8. Get discussion history
    if discussion_id:
        print(f"\n8. Get Discussion History (Discussion: {discussion_id}):")
        try:
            response = requests.get(f"{BASE_URL}/discussion/{discussion_id}")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Discussion ID: {result.get('discussion_id')}")
                print(f"   ✅ Initial question: {result.get('initial_question')}")
                print(f"   ✅ Followup questions: {len(result.get('followup_questions', []))}")
                print(f"   ✅ Total questions: {result.get('total_questions', 0)}")
                print(f"   ✅ User ID: {result.get('user_id')}")
                print(f"   ✅ Created at: {result.get('created_at')}")
            else:
                print(f"   ❌ Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # 9. Get user discussions
    print(f"\n9. Get User Discussions:")
    try:
        response = requests.get(f"{BASE_URL}/discussions", 
                              params={"user_id": "test_user_discussion"})
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ User ID: {result.get('user_id')}")
            print(f"   ✅ Total discussions: {result.get('total_discussions', 0)}")
            discussions = result.get('discussions', [])
            if discussions:
                print(f"   ✅ First discussion ID: {discussions[0].get('discussion_id')}")
                print(f"   ✅ First discussion question: {discussions[0].get('initial_question')}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_advanced_endpoints():
    """Test advanced endpoints that require authentication."""
    print("\n🔐 Testing Advanced Endpoints...")
    
    # 10. Test feedback endpoint
    print("\n10. Feedback Submission:")
    try:
        def test_edge_cases():
            """Test edge cases and boundary conditions."""
            print("\n🔍 Testing Edge Cases...")
            
            # Test 1: Empty question string
            print("\n1. Empty Question String:")
            try:
                response = requests.get(f"{BASE_URL}/predict", params={"question": ""})
                print(f"   Status: {response.status_code}")
                if response.status_code == 422:
                    print(f"   ✅ Correctly rejects empty question")
                else:
                    print(f"   ❌ Unexpected status: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            # Test 2: Very long question
            print("\n2. Very Long Question:")
            try:
                long_question = "What does my future hold? " * 100  # 2500+ characters
                response = requests.get(f"{BASE_URL}/predict", params={"question": long_question})
                print(f"   Status: {response.status_code}")
                print(f"   ✅ Handles long question: {response.status_code == 200}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            # Test 3: Special characters in question
            print("\n3. Special Characters in Question:")
            try:
                special_question = "What about my 💰 finances & career? 🔮✨"
                response = requests.get(f"{BASE_URL}/predict", params={"question": special_question})
                print(f"   Status: {response.status_code}")
                print(f"   ✅ Handles special characters: {response.status_code == 200}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            # Test 4: Non-English question
            print("\n4. Non-English Question:")
            try:
                response = requests.get(f"{BASE_URL}/predict", params={"question": "¿Qué me depara el futuro?"})
                print(f"   Status: {response.status_code}")
                print(f"   ✅ Handles non-English: {response.status_code == 200}")
            except Exception as e:
                print(f"   ❌ Error: {e}")

        def test_concurrent_requests():
            """Test concurrent request handling."""
            print("\n⚡ Testing Concurrent Requests...")
            
            
            results = []
            
            def make_request(question_id):
                try:
                    response = requests.get(f"{BASE_URL}/predict", 
                                          params={"question": f"Test question {question_id}"})
                    results.append({
                        "id": question_id,
                        "status": response.status_code,
                        "success": response.status_code == 200
                    })
                except Exception as e:
                    results.append({
                        "id": question_id,
                        "status": "error",
                        "success": False,
                        "error": str(e)
                    })
            
            # Create 5 concurrent requests
            threads = []
            for i in range(5):
                thread = threading.Thread(target=make_request, args=(i,))
                threads.append(thread)
            
            # Start all threads
            start_time = time.time()
            for thread in threads:
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            end_time = time.time()
            
            successful_requests = sum(1 for r in results if r["success"])
            print(f"   ✅ Concurrent requests: {successful_requests}/5 successful")
            print(f"   ✅ Total time: {end_time - start_time:.3f}s")
            print(f"   ✅ Average time per request: {(end_time - start_time) / 5:.3f}s")

        def test_response_structure():
            """Test response structure consistency."""
            print("\n📋 Testing Response Structure...")
            
            # Test 1: Predict endpoint structure
            print("\n1. Predict Endpoint Structure:")
            try:
                response = requests.get(f"{BASE_URL}/predict", 
                                      params={"question": "Test structure"})
                if response.status_code == 200:
                    result = response.json()
                    expected_fields = ["question", "result", "question_id", "discussion_id", 
                                     "user_id", "reading_type", "timestamp"]
                    
                    for field in expected_fields:
                        has_field = field in result
                        print(f"   ✅ Has {field}: {has_field}")
                        if not has_field:
                            print(f"   ❌ Missing field: {field}")
                else:
                    print(f"   ❌ Failed to test structure: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            # Test 2: Daily reading structure
            print("\n2. Daily Reading Structure:")
            try:
                response = requests.get(f"{BASE_URL}/daily-reading")
                if response.status_code == 200:
                    result = response.json()
                    expected_fields = ["cards", "answer", "question", "reading_type", "user_id"]
                    
                    for field in expected_fields:
                        has_field = field in result
                        print(f"   ✅ Has {field}: {has_field}")
                    
                    # Check card structure
                    cards = result.get("cards", [])
                    if cards:
                        card = cards[0]
                        card_fields = ["name", "arcana", "image_url", "upright", "position", 
                                     "position_keywords", "meaning"]
                        for field in card_fields:
                            has_field = field in card
                            print(f"   🃏 Card has {field}: {has_field}")
                else:
                    print(f"   ❌ Failed to test structure: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Error: {e}")

        def test_data_validation():
            """Test data validation and sanitization."""
            print("\n🔒 Testing Data Validation...")
            
            # Test 1: Invalid JSON in POST request
            print("\n1. Invalid JSON in POST request:")
            try:
                response = requests.post(f"{BASE_URL}/ask", 
                                       data="invalid json",
                                       headers={"Content-Type": "application/json"})
                print(f"   Status: {response.status_code}")
                print(f"   ✅ Handles invalid JSON: {response.status_code == 422}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            # Test 2: Missing Content-Type header
            print("\n2. Missing Content-Type header:")
            try:
                response = requests.post(f"{BASE_URL}/ask", 
                                       data='{"question": "test"}')
                print(f"   Status: {response.status_code}")
                print(f"   ✅ Handles missing Content-Type: {response.status_code in [422, 400]}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            # Test 3: SQL injection attempt
            print("\n3. SQL Injection Attempt:")
            try:
                malicious_question = "'; DROP TABLE users; --"
                response = requests.get(f"{BASE_URL}/predict", 
                                      params={"question": malicious_question})
                print(f"   Status: {response.status_code}")
                print(f"   ✅ Handles malicious input: {response.status_code == 200}")
            except Exception as e:
                print(f"   ❌ Error: {e}")

        def test_feedback_validation():
            """Test feedback endpoint validation."""
            print("\n📝 Testing Feedback Validation...")
            
            # Test 1: Invalid rating (out of range)
            print("\n1. Invalid Rating (out of range):")
            try:
                response = requests.post(f"{BASE_URL}/feedback", 
                                       json={
                                           "reading_id": "test_reading",
                                           "user_id": "test_user",
                                           "rating": 10,  # Assuming 1-5 scale
                                           "feedback_text": "Test feedback",
                                           "helpful": True
                                       })
                print(f"   Status: {response.status_code}")
                print(f"   ✅ Validates rating range: {response.status_code == 422}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            # Test 2: Missing required fields
            print("\n2. Missing Required Fields:")
            try:
                response = requests.post(f"{BASE_URL}/feedback", 
                                       json={
                                           "rating": 5,
                                           "feedback_text": "Test feedback"
                                           # Missing reading_id and user_id
                                       })
                print(f"   Status: {response.status_code}")
                print(f"   ✅ Validates required fields: {response.status_code == 422}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            # Test 3: Very long feedback text
            print("\n3. Very Long Feedback Text:")
            try:
                long_feedback = "This is a very long feedback text. " * 100
                response = requests.post(f"{BASE_URL}/feedback", 
                                       json={
                                           "reading_id": "test_reading",
                                           "user_id": "test_user",
                                           "rating": 5,
                                           "feedback_text": long_feedback,
                                           "helpful": True
                                       })
                print(f"   Status: {response.status_code}")
                print(f"   ✅ Handles long feedback: {response.status_code == 200}")
            except Exception as e:
                print(f"   ❌ Error: {e}")

        def test_performance():
            """Test performance and response times."""
            print("\n⚡ Testing Performance...")
            
            endpoints = [
                ("Health Check", "GET", "/health", None),
                ("Predict", "GET", "/predict", {"question": "Test question"}),
                ("Daily Reading", "GET", "/daily-reading", None),
                ("Custom Ask", "POST", "/ask", {"question": "Test question"}),
                ("Feedback", "POST", "/feedback", {
                    "reading_id": "test", "user_id": "test", "rating": 5, 
                    "feedback_text": "Test", "helpful": True
                })
            ]
            
            for name, method, endpoint, data in endpoints:
                print(f"\n{name} Performance:")
                try:
                    times = []
                    for i in range(3):  # Test 3 times
                        start_time = time.time()
                        
                        if method == "GET":
                            response = requests.get(f"{BASE_URL}{endpoint}", params=data)
                        else:
                            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
                        
                        end_time = time.time()
                        times.append(end_time - start_time)
                    
                    avg_time = sum(times) / len(times)
                    min_time = min(times)
                    max_time = max(times)
                    
                    print(f"   ✅ Average response time: {avg_time:.3f}s")
                    print(f"   ✅ Min response time: {min_time:.3f}s")
                    print(f"   ✅ Max response time: {max_time:.3f}s")
                    print(f"   ✅ Performance acceptable: {avg_time < 5.0}")
                    
                except Exception as e:
                    print(f"   ❌ Error: {e}")

        def test_user_id_handling():
            """Test user ID handling across endpoints."""
            print("\n👤 Testing User ID Handling...")
            
            test_user_id = "test_user_12345"
            
            # Test 1: User ID in predict endpoint
            print("\n1. User ID in Predict Endpoint:")
            try:
                response = requests.get(f"{BASE_URL}/predict", 
                                      params={"question": "Test", "user_id": test_user_id})
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ User ID preserved: {result.get('user_id') == test_user_id}")
                else:
                    print(f"   ❌ Failed: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            # Test 2: User ID in daily reading
            print("\n2. User ID in Daily Reading:")
            try:
                response = requests.get(f"{BASE_URL}/daily-reading", 
                                      params={"user_id": test_user_id})
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ User ID preserved: {result.get('user_id') == test_user_id}")
                else:
                    print(f"   ❌ Failed: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            # Test 3: User ID in custom ask
            print("\n3. User ID in Custom Ask:")
            try:
                response = requests.post(f"{BASE_URL}/ask", 
                                       json={"question": "Test", "user_id": test_user_id})
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ User ID preserved: {result.get('user_id') == test_user_id}")
                else:
                    print(f"   ❌ Failed: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Error: {e}")

        def test_question_id_generation():
            """Test question ID generation and uniqueness."""
            print("\n🆔 Testing Question ID Generation...")
            
            question_ids = []
            
            for i in range(5):
                print(f"\n{i+1}. Generate Question ID:")
                try:
                    response = requests.get(f"{BASE_URL}/predict", 
                                          params={"question": f"Test question {i}"})
                    if response.status_code == 200:
                        result = response.json()
                        question_id = result.get('question_id')
                        question_ids.append(question_id)
                        print(f"   ✅ Question ID generated: {question_id}")
                    else:
                        print(f"   ❌ Failed: {response.status_code}")
                except Exception as e:
                    print(f"   ❌ Error: {e}")
            
            # Check uniqueness
            unique_ids = set(question_ids)
            print(f"\n   ✅ Total IDs: {len(question_ids)}")
            print(f"   ✅ Unique IDs: {len(unique_ids)}")
            print(f"   ✅ All IDs unique: {len(question_ids) == len(unique_ids)}")

        # Update the run_all_tests function to include new tests
        def run_all_tests():
            """Run all test suites."""
            print("=" * 60)
            print("🚀 TarotAI API Test Suite")
            print("=" * 60)
            
            test_basic_endpoints()
            test_custom_ask_endpoint()
            test_discussion_functionality()
            test_advanced_endpoints()
            test_error_handling()
            test_caching()
            test_different_questions()
            
            # New comprehensive tests
            test_edge_cases()
            test_concurrent_requests()
            test_response_structure()
            test_data_validation()
            test_feedback_validation()
            test_performance()
            test_user_id_handling()
            test_question_id_generation()
            
            print("\n" + "=" * 60)
            print("✅ All tests completed!")
            print("=" * 60)
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 12. Missing required parameter
    print("\n12. Missing Required Parameter:")
    try:
        response = requests.get(f"{BASE_URL}/predict")  # No question parameter
        print(f"   Status: {response.status_code}")
        if response.status_code == 422:
            print(f"   ✅ Correctly validates required parameters")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 13. Test POST /ask with missing question
    print("\n13. POST /ask with missing question:")
    try:
        response = requests.post(f"{BASE_URL}/ask", json={})
        print(f"   Status: {response.status_code}")
        if response.status_code == 422:
            print(f"   ✅ Correctly validates required JSON fields")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 14. Test followup with non-existent discussion
    print("\n14. Followup with Non-existent Discussion:")
    try:
        response = requests.post(f"{BASE_URL}/followup", 
                               json={
                                   "discussion_id": "non_existent_discussion",
                                   "question": "This should fail",
                                   "user_id": "test_user"
                               })
        print(f"   Status: {response.status_code}")
        if response.status_code == 404:
            print(f"   ✅ Correctly returns 404 for non-existent discussion")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 15. Test get discussion with non-existent ID
    print("\n15. Get Non-existent Discussion:")
    try:
        response = requests.get(f"{BASE_URL}/discussion/non_existent")
        print(f"   Status: {response.status_code}")
        if response.status_code == 404:
            print(f"   ✅ Correctly returns 404 for non-existent discussion")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_caching():
    """Test caching functionality."""
    print("\n💾 Testing Caching...")
    
    # 16. Test daily reading caching
    print("\n16. Daily Reading Caching:")
    try:
        # First request
        start_time = time.time()
        response1 = requests.get(f"{BASE_URL}/daily-reading?user_id=cache_test")
        time1 = time.time() - start_time
        
        # Second request (should be cached)
        start_time = time.time()
        response2 = requests.get(f"{BASE_URL}/daily-reading?user_id=cache_test")
        time2 = time.time() - start_time
        
        if response1.status_code == 200 and response2.status_code == 200:
            result1 = response1.json()
            result2 = response2.json()
            
            print(f"   ✅ Both requests successful")
            print(f"   ✅ First request time: {time1:.3f}s")
            print(f"   ✅ Second request time: {time2:.3f}s")
            print(f"   ✅ Results identical: {result1 == result2}")
            if time2 < time1:
                print(f"   ✅ Caching working: Second request faster")
            else:
                print(f"   ⚠️  Caching may not be working optimally")
        else:
            print(f"   ❌ Caching test failed")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_different_questions():
    """Test different types of questions for prediction."""
    print("\n❓ Testing Different Question Types...")
    
    questions = [
        "What does my future hold?",
        "Will I find love this year?", 
        "Should I change my career?",
        "How can I improve my relationships?",
        "What is blocking my success?"
    ]
    
    for i, question in enumerate(questions, 17):
        print(f"\n{i}. Question: '{question}'")
        try:
            response = requests.get(f"{BASE_URL}/predict", 
                                  params={"question": question})
            if response.status_code == 200:
                result = response.json()
                answer = result.get('result', '')
                print(f"   ✅ Status: {response.status_code}")
                print(f"   ✅ Answer length: {len(answer)}")
                print(f"   📝 Preview: {answer[:80]}...")
            else:
                print(f"   ❌ Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def run_all_tests():
    """Run all test suites."""
    print("=" * 60)
    print("🚀 TarotAI API Test Suite")
    print("=" * 60)
    
    test_basic_endpoints()
    test_custom_ask_endpoint()
    test_discussion_functionality()  # New comprehensive test
    test_advanced_endpoints()
    test_caching()
    test_different_questions()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()