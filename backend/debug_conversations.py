#!/usr/bin/env python3
"""
Debug script to test conversation endpoints specifically
"""

import requests
import jwt
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER_ID = "1"

def create_debug_jwt_token():
    """Create a test JWT token with proper claims for debugging"""
    secret = os.getenv("BETTER_AUTH_SECRET", "test_secret_for_testing_purposes_only")

    # Create a payload with typical Better Auth claims
    payload = {
        "userId": TEST_USER_ID,
        "sub": TEST_USER_ID,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,  # 1 hour expiry
        "iss": "better-auth-test"
    }

    # Encode the token
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

def test_conversations_endpoint():
    """Test just the conversations endpoint"""
    print("Testing conversations endpoint...")
    try:
        token = create_debug_jwt_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(
            f"{BASE_URL}/api/{TEST_USER_ID}/conversations",
            headers=headers
        )

        print(f"Conversations endpoint - Status: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 500:
            print("ERROR: Internal Server Error occurred")
            return False
        return True

    except Exception as e:
        print(f"Conversations endpoint - ERROR: {e}")
        return False

def test_chat_endpoint():
    """Test just the chat endpoint"""
    print("\nTesting chat endpoint...")
    try:
        token = create_debug_jwt_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        payload = {
            "message": "Hello, this is a debug test",
            "conversation_id": None
        }

        response = requests.post(
            f"{BASE_URL}/api/{TEST_USER_ID}/chat",
            json=payload,
            headers=headers
        )

        print(f"Chat endpoint - Status: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 500:
            print("ERROR: Internal Server Error occurred")
            return False
        return True

    except Exception as e:
        print(f"Chat endpoint - ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Debugging conversation endpoints...")

    conv_success = test_conversations_endpoint()
    chat_success = test_chat_endpoint()

    print(f"\nResults:")
    print(f"Conversations endpoint: {'PASS' if conv_success else 'FAIL'}")
    print(f"Chat endpoint: {'PASS' if chat_success else 'FAIL'}")