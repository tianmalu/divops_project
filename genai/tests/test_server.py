import requests
import json
import time

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
                print(f"   ✅ Has answer: {'answer' in result}")
                print(f"   ✅ Reading type: {result.get('reading_type', 'N/A')}")
                
                # Check card structure
                cards = result.get('cards', [])
                if cards:
                    first_card = cards[0]
                    print(f"   🃏 First Card: {first_card.get('name', 'N/A')}")
                    print(f"   🃏 Position: {first_card.get('position', 'N/A')}")
                
                answer = result.get('answer', '')
                print(f"   📝 Answer length: {len(answer)}")
                print(f"   📝 Question echoed: {result.get('question') == question}")
                
            else:
                print(f"   ❌ Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_advanced_endpoints():
    """Test advanced endpoints that require authentication."""
    print("\n🔐 Testing Advanced Endpoints...")
    
    # 5. Try to access authenticated endpoint without token
    print("\n5. Custom Reading (no auth):")
    try:
        response = requests.post(f"{BASE_URL}/reading", 
                               json={
                                   "question": "What should I focus on?",
                                   "spread_type": "three"
                               })
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print(f"   ✅ Correctly requires authentication")
        else:
            print(f"   ❌ Unexpected response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 6. Try to submit feedback without auth
    print("\n6. Feedback Submission (no auth):")
    try:
        response = requests.post(f"{BASE_URL}/feedback", 
                               json={
                                   "reading_id": "test_123",
                                   "user_id": "test_user",
                                   "rating": 5,
                                   "feedback_text": "Great reading!"
                               })
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print(f"   ✅ Correctly requires authentication")
        else:
            print(f"   ❌ Unexpected response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_error_handling():
    """Test error handling and edge cases."""
    print("\n⚠️  Testing Error Handling...")
    
    # 7. Invalid endpoint
    print("\n7. Invalid Endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/nonexistent")
        print(f"   Status: {response.status_code}")
        if response.status_code == 404:
            print(f"   ✅ Correctly returns 404")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 8. Missing required parameter
    print("\n8. Missing Required Parameter:")
    try:
        response = requests.get(f"{BASE_URL}/predict")  # No question parameter
        print(f"   Status: {response.status_code}")
        if response.status_code == 422:
            print(f"   ✅ Correctly validates required parameters")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 9. Test POST /ask with missing question
    print("\n9. POST /ask with missing question:")
    try:
        response = requests.post(f"{BASE_URL}/ask", json={})
        print(f"   Status: {response.status_code}")
        if response.status_code == 422:
            print(f"   ✅ Correctly validates required JSON fields")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_caching():
    """Test caching functionality."""
    print("\n💾 Testing Caching...")
    
    # 10. Test daily reading caching
    print("\n10. Daily Reading Caching:")
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
            print(f"   ✅ Caching working: {time2 < time1}")
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
    
    for i, question in enumerate(questions, 11):
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
    test_custom_ask_endpoint()  # New test function
    test_advanced_endpoints()
    test_error_handling()
    test_caching()
    test_different_questions()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()