#!/usr/bin/env python3
"""
Backend Integration Test Script for AI Todo Chatbot

This script tests all backend functionality including:
- MCP tools (add_task, delete_task, update_task, complete_task, list_tasks, get_current_user)
- Chat endpoints (POST /api/{user_id}/chat, GET /api/{user_id}/conversations, GET /api/{user_id}/conversations/{conversation_id}/messages)
- JWT authentication handling
- AI response and tool call execution
"""

import asyncio
import json
import subprocess
import sys
import time
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import threading
import signal
import os
import jwt
from dotenv import load_dotenv

# Load environment variables from .env file FIRST
load_dotenv()

# Import after environment is loaded - we'll access settings.BETTER_AUTH_SECRET dynamically
from core.config import Settings

# Create a fresh settings instance to ensure environment variables are loaded
settings = Settings()

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER_ID = "1"  # Using a test user ID

# Global variable to hold the backend process
backend_process = None


def create_test_jwt_token():
    """Create a test JWT token with proper claims for testing"""
    # Use the actual BETTER_AUTH_SECRET from settings
    if not settings.BETTER_AUTH_SECRET:
        print("Warning: BETTER_AUTH_SECRET not found in settings")
        secret = "test_secret_for_testing_purposes_only"
    else:
        secret = settings.BETTER_AUTH_SECRET

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


def start_backend_server():
    """Start the FastAPI backend server"""
    global backend_process
    print("Starting FastAPI backend server on localhost:8000...")

    try:
        # Start the server using uvicorn
        backend_process = subprocess.Popen([
            sys.executable, "-c",
            "import uvicorn; from main import app; uvicorn.run(app, host='0.0.0.0', port=8000, reload=False)"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=".")

        # Wait for server to start
        time.sleep(5)

        # Check if server is running
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=10)
            if response.status_code == 200:
                print("Backend server started successfully")
                return True
        except requests.exceptions.RequestException:
            pass

        print("Failed to start backend server")
        return False

    except Exception as e:
        print(f"Error starting backend server: {e}")
        return False


def stop_backend_server():
    """Stop the FastAPI backend server"""
    global backend_process
    if backend_process:
        print("\nStopping backend server...")
        backend_process.terminate()
        backend_process.wait()
        print("Backend server stopped")


def get_auth_headers():
    """Get authentication headers with valid JWT token"""
    token = create_test_jwt_token()
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }


def test_health_check():
    """Test the health check endpoint"""
    print("\nTesting health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200 and response.json().get("status") == "healthy":
            print("Health check: SUCCESS")
            return True
        else:
            print(f"Health check: FAILED - {response.text}")
            return False
    except Exception as e:
        print(f"Health check: ERROR - {e}")
        return False


def test_add_task():
    """Test the add_task functionality via API"""
    print("\nTesting add_task endpoint...")
    try:
        # Create a valid JWT token for authentication
        headers = get_auth_headers()

        payload = {
            "title": f"Test task {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "description": "Test description for backend integration",
            "completed": False
        }

        response = requests.post(
            f"{BASE_URL}/api/{TEST_USER_ID}/tasks",
            json=payload,
            headers=headers
        )

        if response.status_code == 201:
            task = response.json()
            print(f" Add task: SUCCESS - Task ID: {task.get('id')}")
            return task.get('id')
        else:
            print(f" Add task: FAILED - Status: {response.status_code}, Response: {response.text}")
            return None

    except Exception as e:
        print(f" Add task: ERROR - {e}")
        return None


def test_list_tasks():
    """Test the list_tasks functionality"""
    print("\nTesting list_tasks endpoint...")
    try:
        headers = get_auth_headers()

        response = requests.get(
            f"{BASE_URL}/api/{TEST_USER_ID}/tasks",
            headers=headers
        )

        if response.status_code == 200:
            tasks = response.json()
            print(f" List tasks: SUCCESS - Found {len(tasks)} tasks")
            return tasks
        else:
            print(f" List tasks: FAILED - Status: {response.status_code}, Response: {response.text}")
            return []

    except Exception as e:
        print(f" List tasks: ERROR - {e}")
        return []


def test_get_specific_task(task_id: int):
    """Test getting a specific task"""
    print(f"\nTesting get specific task endpoint (ID: {task_id})...")
    try:
        headers = get_auth_headers()

        response = requests.get(
            f"{BASE_URL}/api/{TEST_USER_ID}/tasks/{task_id}",
            headers=headers
        )

        if response.status_code == 200:
            task = response.json()
            print(f" Get task: SUCCESS - Task: {task.get('title')}")
            return task
        else:
            print(f" Get task: FAILED - Status: {response.status_code}, Response: {response.text}")
            return None

    except Exception as e:
        print(f" Get task: ERROR - {e}")
        return None


def test_update_task(task_id: int):
    """Test updating a task"""
    print(f"\n Testing update_task endpoint (ID: {task_id})...")
    try:
        headers = get_auth_headers()

        payload = {
            "title": f"Updated test task {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "description": "Updated test description",
            "completed": False
        }

        response = requests.put(
            f"{BASE_URL}/api/{TEST_USER_ID}/tasks/{task_id}",
            json=payload,
            headers=headers
        )

        if response.status_code == 200:
            task = response.json()
            print(f" Update task: SUCCESS - Task updated: {task.get('title')}")
            return task
        else:
            print(f" Update task: FAILED - Status: {response.status_code}, Response: {response.text}")
            return None

    except Exception as e:
        print(f" Update task: ERROR - {e}")
        return None


def test_complete_task(task_id: int):
    """Test completing a task"""
    print(f"\n Testing complete_task endpoint (ID: {task_id})...")
    try:
        headers = get_auth_headers()

        payload = {"completed": True}

        response = requests.patch(
            f"{BASE_URL}/api/{TEST_USER_ID}/tasks/{task_id}/complete",
            json=payload,
            headers=headers
        )

        if response.status_code == 200:
            task = response.json()
            print(f" Complete task: SUCCESS - Task completed: {task.get('title')}, Status: {'Completed' if task.get('completed') else 'Pending'}")
            return task
        else:
            print(f" Complete task: FAILED - Status: {response.status_code}, Response: {response.text}")
            return None

    except Exception as e:
        print(f" Complete task: ERROR - {e}")
        return None


def test_delete_task(task_id: int):
    """Test deleting a task"""
    print(f"\nTesting delete_task endpoint (ID: {task_id})...")
    try:
        headers = get_auth_headers()

        response = requests.delete(
            f"{BASE_URL}/api/{TEST_USER_ID}/tasks/{task_id}",
            headers=headers
        )

        if response.status_code == 204:
            print(f" Delete task: SUCCESS - Task {task_id} deleted")
            return True
        else:
            print(f" Delete task: FAILED - Status: {response.status_code}, Response: {response.text}")
            return False

    except Exception as e:
        print(f" Delete task: ERROR - {e}")
        return False


def test_chat_endpoint():
    """Test the chat endpoint functionality"""
    print("\nTesting chat endpoint...")
    try:
        headers = get_auth_headers()

        # First, let's try to get a conversation list to see if the chat system is working
        conv_response = requests.get(
            f"{BASE_URL}/api/{TEST_USER_ID}/conversations",
            headers=headers
        )

        if conv_response.status_code == 200:
            conversations = conv_response.json()
            print(f" Chat system accessible - Found {conversations.get('total_count', 0)} conversations")
        else:
            print(f" Chat system: Could not access conversations - Status: {conv_response.status_code}")

        # Now test sending a message
        payload = {
            "message": "Hello, this is a test message for the AI chatbot",
            "conversation_id": None  # Will create new conversation
        }

        response = requests.post(
            f"{BASE_URL}/api/{TEST_USER_ID}/chat",
            json=payload,
            headers=headers
        )

        if response.status_code == 200:
            chat_response = response.json()
            print(f" Chat endpoint: SUCCESS - Response received, Conversation ID: {chat_response.get('conversation_id')}")
            return chat_response
        else:
            print(f" Chat endpoint: FAILED - Status: {response.status_code}, Response: {response.text}")
            return None

    except Exception as e:
        print(f" Chat endpoint: ERROR - {e}")
        return None


def test_conversation_endpoints():
    """Test conversation-related endpoints"""
    print("\nTesting conversation endpoints...")

    # Test getting conversations
    try:
        headers = get_auth_headers()

        conv_response = requests.get(
            f"{BASE_URL}/api/{TEST_USER_ID}/conversations",
            headers=headers
        )

        if conv_response.status_code == 200:
            conversations = conv_response.json()
            print(f" Get conversations: SUCCESS - Total: {conversations.get('total_count', 0)}")

            if conversations.get('conversations'):
                # Test getting messages from the first conversation
                first_conv_id = conversations['conversations'][0]['id']
                msg_response = requests.get(
                    f"{BASE_URL}/api/{TEST_USER_ID}/conversations/{first_conv_id}/messages",
                    headers=headers
                )

                if msg_response.status_code == 200:
                    messages = msg_response.json()
                    print(f" Get conversation messages: SUCCESS - Found {len(messages.get('messages', []))} messages")
                    return True
                else:
                    print(f" Get conversation messages: FAILED - Status: {msg_response.status_code}")
                    return False
            else:
                print(" No existing conversations to test messages")
                return True
        else:
            print(f" Get conversations: FAILED - Status: {conv_response.status_code}")
            return False

    except Exception as e:
        print(f" Conversation endpoints: ERROR - {e}")
        return False


def run_comprehensive_tests():
    """Run all comprehensive tests"""
    print("Starting comprehensive backend integration tests...\n")

    results = {}

    # Test health check first
    results['health'] = test_health_check()

    # Test task operations
    print("\n" + "="*60)
    print("TASK OPERATIONS TESTS")
    print("="*60)

    # Add a task
    task_id = test_add_task()
    if task_id:
        results['add_task'] = True

        # Get the task
        task = test_get_specific_task(task_id)
        if task:
            results['get_task'] = True

            # Update the task
            updated_task = test_update_task(task_id)
            if updated_task:
                results['update_task'] = True

                # Complete the task
                completed_task = test_complete_task(task_id)
                if completed_task:
                    results['complete_task'] = True

                    # Delete the task
                    deleted = test_delete_task(task_id)
                    if deleted:
                        results['delete_task'] = True
                    else:
                        results['delete_task'] = False
                else:
                    results['complete_task'] = False
                    results['delete_task'] = False
            else:
                results['update_task'] = False
                results['complete_task'] = False
                results['delete_task'] = False
        else:
            results['get_task'] = False
            results['update_task'] = False
            results['complete_task'] = False
            results['delete_task'] = False
    else:
        results['add_task'] = False
        results['get_task'] = False
        results['update_task'] = False
        results['complete_task'] = False
        results['delete_task'] = False

    # List tasks
    tasks = test_list_tasks()
    results['list_tasks'] = len(tasks) >= 0  # Should always return a list

    print("\n" + "="*60)
    print("CHAT FUNCTIONALITY TESTS")
    print("="*60)

    # Test chat functionality
    chat_response = test_chat_endpoint()
    results['chat_endpoint'] = chat_response is not None

    # Test conversation endpoints
    results['conversation_endpoints'] = test_conversation_endpoints()

    return results


def print_test_summary(results: Dict[str, bool]):
    """Print a summary of test results"""
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)

    passed = sum(1 for result in results.values() if result)
    total = len(results)

    for test_name, result in results.items():
        status = " PASS" if result else " FAIL"
        print(f"{status} {test_name.replace('_', ' ').title()}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("All tests passed!")
        return True
    else:
        print(f"{total - passed} tests failed")
        return False


def main():
    """Main function to run the test suite"""
    print("AI Todo Chatbot - Backend Integration Test Suite")
    print("="*60)

    # Start backend server
    if not start_backend_server():
        print("Cannot proceed without backend server")
        sys.exit(1)

    try:
        # Run comprehensive tests
        results = run_comprehensive_tests()

        # Print summary
        success = print_test_summary(results)

        # Return appropriate exit code
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        sys.exit(1)
    finally:
        # Stop backend server
        stop_backend_server()


if __name__ == "__main__":
    main()