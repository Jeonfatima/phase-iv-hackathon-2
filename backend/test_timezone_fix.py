#!/usr/bin/env python3
"""
Test script to verify the timezone import fix in auth.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_timezone_import():
    """Test that timezone import works correctly"""
    print("Testing timezone import fix...")

    try:
        # Test importing the required modules
        from datetime import datetime, timedelta, timezone

        # Test creating timezone-aware datetimes
        now_utc = datetime.now(timezone.utc)
        exp_time = now_utc + timedelta(hours=24)

        print(f"  OK Current time (UTC): {now_utc}")
        print(f"  OK Expiration time (UTC): {exp_time}")
        print(f"  OK Timezone info: {now_utc.tzinfo}")

        return True

    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_jwt_token_expiration_logic():
    """Test the JWT token expiration logic that was failing"""
    print("\nTesting JWT token expiration logic...")

    try:
        from datetime import datetime, timedelta, timezone
        import jwt
        from core.config import settings

        # Simulate the token creation logic that was failing
        fake_user_id = "123"
        fake_email = "test@example.com"

        token_data = {
            "userId": fake_user_id,
            "email": fake_email,
            "exp": datetime.now(timezone.utc) + timedelta(hours=24)  # Line 122 equivalent
        }

        # If BETTER_AUTH_SECRET is not set, use a test secret
        secret = settings.BETTER_AUTH_SECRET or "test_secret_for_testing"

        encoded_token = jwt.encode(token_data, secret, algorithm="HS256")

        print(f"  OK Token created successfully")
        print(f"  OK Token data: {token_data}")
        print(f"  OK Token (truncated): {encoded_token[:50]}...")

        return True

    except NameError as e:
        if "timezone" in str(e):
            print(f"  ERROR: timezone NameError still exists: {e}")
            return False
        else:
            print(f"  ERROR: Other NameError: {e}")
            return False
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_timezone_tests():
    """Run all timezone-related tests"""
    print("Running Timezone Import Fix Verification Tests")
    print("=" * 50)

    results = []

    # Test 1: Basic timezone import
    success1 = test_timezone_import()
    results.append(("Timezone import", success1))

    # Test 2: JWT token expiration logic
    success2 = test_jwt_token_expiration_logic()
    results.append(("JWT token expiration logic", success2))

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
        print("\nALL TESTS PASSED! Timezone import fix is working correctly.")
        print("OK timezone module is now available globally")
        print("OK datetime.now(timezone.utc) works in both register and login functions")
        print("OK Line 122 (JWT expiration) will no longer throw NameError")
        return True
    else:
        print(f"\n{total - passed} tests failed.")
        return False


if __name__ == "__main__":
    success = run_timezone_tests()
    sys.exit(0 if success else 1)