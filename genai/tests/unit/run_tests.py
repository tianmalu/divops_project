#!/usr/bin/env python3
"""
Test Runner for TarotAI GenAI Service
Runs all test suites and provides comprehensive test results
"""

import sys
import os
from datetime import datetime

# Add the genai directory to the Python path to find app module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def run_all_tests():
    """Run all test suites"""
    print("🔍 TarotAI GenAI Service - Comprehensive Test Suite")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    test_results = {}
    
    # Test 1: Prompt Tests
    print("📝 Running Prompt Tests...")
    try:
        from test_prompt import run_all_tests as run_prompt_tests
        test_results['prompt'] = run_prompt_tests()
    except Exception as e:
        print(f"❌ Prompt tests failed to run: {e}")
        test_results['prompt'] = False
    
    print("\n" + "-" * 60 + "\n")
    
    # Test 2: Layout Tests
    print("🃏 Running Layout Tests...")
    try:
        from test_layout import run_all_tests as run_layout_tests
        test_results['layout'] = run_layout_tests()
    except Exception as e:
        print(f"❌ Layout tests failed to run: {e}")
        test_results['layout'] = False
    
    print("\n" + "-" * 60 + "\n")
    
    # Test 3: Model Tests
    print("🏗️ Running Model Tests...")
    try:
        from test_models import run_all_tests as run_model_tests
        test_results['models'] = run_model_tests()
    except Exception as e:
        print(f"❌ Model tests failed to run: {e}")
        test_results['models'] = False
    
    print("\n" + "-" * 60 + "\n")
    
    # Test 4: RAG Tests
    print("🤖 Running RAG Engine Tests...")
    try:
        from test_rag import run_all_tests as run_rag_tests
        test_results['rag'] = run_rag_tests()
    except Exception as e:
        print(f"❌ RAG tests failed to run: {e}")
        test_results['rag'] = False
    
    print("\n" + "-" * 60 + "\n")
    
    # Test 5: Feedback Tests
    print("💬 Running Feedback Tests...")
    try:
        from test_feedback import run_all_tests as run_feedback_tests
        test_results['feedback'] = run_feedback_tests()
    except Exception as e:
        print(f"❌ Feedback tests failed to run: {e}")
        test_results['feedback'] = False
    
    print("\n" + "=" * 60)
    
    # Summary
    print("\n📊 TEST SUITE SUMMARY")
    print("=" * 60)
    
    total_suites = len(test_results)
    passed_suites = sum(1 for result in test_results.values() if result)
    failed_suites = total_suites - passed_suites
    
    print(f"Total Test Suites: {total_suites}")
    print(f"Passed: {passed_suites}")
    print(f"Failed: {failed_suites}")
    print()
    
    # Detailed results
    for suite_name, result in test_results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{suite_name.capitalize()} Tests: {status}")
    
    print()
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Overall result
    if all(test_results.values()):
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("The TarotAI GenAI service is ready for deployment.")
        return True
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("Please review the failed tests above and fix the issues.")
        return False

def run_individual_test(test_name):
    """Run a specific test suite"""
    test_name = test_name.lower()
    
    if test_name == 'prompt':
        from test_prompt import run_all_tests
        return run_all_tests()
    elif test_name == 'layout':
        from test_layout import run_all_tests
        return run_all_tests()
    elif test_name == 'models':
        from test_models import run_all_tests
        return run_all_tests()
    elif test_name == 'rag':
        from test_rag import run_all_tests
        return run_all_tests()
    elif test_name == 'feedback':
        from test_feedback import run_all_tests
        return run_all_tests()
    else:
        print(f"Unknown test suite: {test_name}")
        print("Available test suites: prompt, layout, models, rag, feedback")
        return False

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) > 1:
        # Run specific test suite
        test_name = sys.argv[1]
        print(f"Running {test_name} tests...")
        success = run_individual_test(test_name)
        if success:
            print(f"\n✅ {test_name} tests passed!")
        else:
            print(f"\n❌ {test_name} tests failed!")
    else:
        # Run all tests
        success = run_all_tests()
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
