#!/usr/bin/env python3
"""
Test script to verify the chat endpoint validation fix
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from pydantic import ValidationError
from api.chat import ChatRequest


def test_empty_message_handling():
    """Test that empty messages are handled gracefully"""
    print("Testing ChatRequest model with empty message...")

    try:
        # Test with empty string
        req1 = ChatRequest(message="", conversation_id=1)
        print(f"  OK Empty string accepted: message='{req1.message}', conversation_id={req1.conversation_id}")

        # Test without message field (should use default)
        req2 = ChatRequest(conversation_id=2)
        print(f"  OK Missing message accepted: message='{req2.message}', conversation_id={req2.conversation_id}")

        # Test with valid message
        req3 = ChatRequest(message="Hello", conversation_id=3)
        print(f"  OK Valid message accepted: message='{req3.message}', conversation_id={req3.conversation_id}")

        # Test with whitespace-only message
        req4 = ChatRequest(message="   ", conversation_id=4)
        print(f"  OK Whitespace message accepted: message='{req4.message}', conversation_id={req4.conversation_id}")

        return True

    except ValidationError as e:
        print(f"  ERROR Validation error: {e}")
        return False
    except Exception as e:
        print(f"  ERROR Unexpected error: {e}")
        return False


def test_conversation_id_optional():
    """Test that conversation_id is optional"""
    print("\nTesting conversation_id optional behavior...")

    try:
        # Without conversation_id (should use None)
        req1 = ChatRequest(message="test")
        print(f"  OK Missing conversation_id accepted: message='{req1.message}', conversation_id={req1.conversation_id}")

        # With conversation_id
        req2 = ChatRequest(message="test", conversation_id=123)
        print(f"  OK With conversation_id accepted: message='{req2.message}', conversation_id={req2.conversation_id}")

        return True

    except ValidationError as e:
        print(f"  ERROR Validation error: {e}")
        return False
    except Exception as e:
        print(f"  ERROR Unexpected error: {e}")
        return False


def run_validation_tests():
    """Run all validation tests"""
    print("Running Chat Request Validation Fix Tests")
    print("=" * 50)

    results = []

    # Test 1: Empty message handling
    success1 = test_empty_message_handling()
    results.append(("Empty message handling", success1))

    # Test 2: Conversation ID optional
    success2 = test_conversation_id_optional()
    results.append(("Conversation ID optional", success2))

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
        print("\nALL TESTS PASSED! Chat validation fix is working correctly.")
        print("OK Empty messages are handled gracefully")
        print("OK Missing message field uses default value")
        print("OK conversation_id remains optional")
        return True
    else:
        print(f"\n{total - passed} tests failed.")
        return False


if __name__ == "__main__":
    success = run_validation_tests()
    sys.exit(0 if success else 1)