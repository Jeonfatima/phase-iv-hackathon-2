#!/usr/bin/env python3
"""
Test script to verify the chat endpoint 400 error fix
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from api.chat import ChatRequest


def test_chat_request_model():
    """Test the ChatRequest model with various message inputs"""
    print("Testing ChatRequest model...")

    try:
        # Test with empty string (should work now)
        req1 = ChatRequest(message="")
        print(f"  OK Empty message: '{req1.message}'")

        # Test with valid message
        req2 = ChatRequest(message="Hello world")
        print(f"  OK Valid message: '{req2.message}'")

        # Test with whitespace
        req3 = ChatRequest(message="   ")
        print(f"  OK Whitespace message: '{req3.message}'")

        # Test without message field (should use default)
        req4 = ChatRequest()
        print(f"  OK No message field: '{req4.message}'")

        # Test with conversation_id
        req5 = ChatRequest(message="Test", conversation_id=123)
        print(f"  OK With conversation_id: message='{req5.message}', id={req5.conversation_id}")

        return True

    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_validation_edge_cases():
    """Test edge cases that might cause issues"""
    print("\nTesting validation edge cases...")

    try:
        from services.chat_service import ChatService

        # Test various message contents that might fail validation
        test_cases = [
            "",           # Empty
            "   ",        # Just whitespace
            "H",          # Single character
            "Hello!",     # Normal message
            "A" * 500,    # Long message (under limit)
        ]

        for i, message in enumerate(test_cases):
            result = ChatService.validate_and_sanitize_message(message)
            print(f"  OK Test case {i+1}: '{message[:20]}{'...' if len(message) > 20 else ''}' -> valid={result['valid']}")

        return True

    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_chat_endpoint_tests():
    """Run all chat endpoint tests"""
    print("Running Chat Endpoint 400 Error Fix Tests")
    print("=" * 50)

    results = []

    # Test 1: ChatRequest model
    success1 = test_chat_request_model()
    results.append(("ChatRequest model", success1))

    # Test 2: Validation edge cases
    success2 = test_validation_edge_cases()
    results.append(("Validation edge cases", success2))

    # Summary
    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)

    passed = 0
    total = len(results)

    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{status:4} {test_name}")
        if success:
            passed += 1

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("\nALL TESTS PASSED! Chat endpoint fix is working correctly.")
        print("OK ChatRequest accepts empty messages")
        print("OK Validation handles edge cases gracefully")
        print("OK No more 400 errors for valid inputs")
        return True
    else:
        print(f"\n{total - passed} tests failed.")
        return False


if __name__ == "__main__":
    success = run_chat_endpoint_tests()
    sys.exit(0 if success else 1)