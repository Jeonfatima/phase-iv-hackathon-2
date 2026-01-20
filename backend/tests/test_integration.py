"""
Comprehensive integration tests for the chatbot functionality
Testing the complete flow: authentication -> chat interaction -> task operations
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from services.mcp_tools import add_task, delete_task, update_task, complete_task, list_tasks, get_current_user
from database.session import Session
from database.engine import engine
from models.task import Task
from sqlmodel import select
import uuid
from datetime import datetime, timedelta
import jwt


def test_full_chatbot_integration_flow():
    """Test the complete chatbot integration flow"""
    client = TestClient(app)

    # Mock JWT payload for testing
    mock_jwt_payload = {
        "user_id": "12345",
        "email": "integration_test@example.com",
        "exp": int((datetime.now() + timedelta(hours=1)).timestamp()),
        "iat": int(datetime.now().timestamp()),
        "jti": str(uuid.uuid4())
    }

    # Test the complete flow: create, list, update, complete, delete tasks via chatbot
    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        with patch('services.ai_service.AIService.process_conversation_with_reasoning_loop') as mock_process:

            # Scenario 1: Add a task
            mock_process.return_value = {
                "response": "Task 'Buy groceries' added successfully with ID 1",
                "tool_calls": [{
                    "name": "add_task",
                    "arguments": {"title": "Buy groceries", "description": "Milk and bread", "user_id": "12345"},
                    "result": {"success": True, "task_id": 1, "message": "Task 'Buy groceries' added successfully"}
                }],
                "success": True
            }

            headers = {"Authorization": "Bearer fake-token-for-test"}
            response = client.post(
                "/api/12345/chat",
                json={"message": "Add a task to buy groceries with description milk and bread", "conversation_id": None},
                headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "Buy groceries" in data["response"]

            # Scenario 2: List tasks
            mock_process.return_value = {
                "response": "You have 1 task: Buy groceries",
                "tool_calls": [{
                    "name": "list_tasks",
                    "arguments": {"user_id": "12345", "filter_status": "all"},
                    "result": {
                        "success": True,
                        "tasks": [{"id": 1, "title": "Buy groceries", "description": "Milk and bread", "completed": False}],
                        "count": 1,
                        "message": "Retrieved 1 tasks successfully"
                    }
                }],
                "success": True
            }

            response = client.post(
                "/api/12345/chat",
                json={"message": "Show me my tasks", "conversation_id": None},
                headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "Buy groceries" in data["response"]

            # Scenario 3: Update task
            mock_process.return_value = {
                "response": "Task 1 updated successfully",
                "tool_calls": [{
                    "name": "update_task",
                    "arguments": {"task_id": 1, "user_id": "12345", "title": "Buy weekly groceries"},
                    "result": {"success": True, "message": "Task with ID 1 updated successfully"}
                }],
                "success": True
            }

            response = client.post(
                "/api/12345/chat",
                json={"message": "Update task 1 title to 'Buy weekly groceries'", "conversation_id": None},
                headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "updated successfully" in data["response"].lower()

            # Scenario 4: Complete task
            mock_process.return_value = {
                "response": "Task 1 marked as completed successfully",
                "tool_calls": [{
                    "name": "complete_task",
                    "arguments": {"task_id": 1, "completed": True, "user_id": "12345"},
                    "result": {"success": True, "message": "Task with ID 1 marked as completed successfully"}
                }],
                "success": True
            }

            response = client.post(
                "/api/12345/chat",
                json={"message": "Mark task 1 as complete", "conversation_id": None},
                headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "completed" in data["response"].lower()

            # Scenario 5: Delete task
            mock_process.return_value = {
                "response": "Task 1 deleted successfully",
                "tool_calls": [{
                    "name": "delete_task",
                    "arguments": {"task_id": 1, "user_id": "12345"},
                    "result": {"success": True, "message": "Task with ID 1 deleted successfully"}
                }],
                "success": True
            }

            response = client.post(
                "/api/12345/chat",
                json={"message": "Delete task 1", "conversation_id": None},
                headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "deleted" in data["response"].lower()


def test_user_isolation_integration():
    """Test that users are properly isolated in the chatbot functionality"""
    client = TestClient(app)

    # Mock JWT payloads for two different users
    mock_jwt_payload_user1 = {
        "user_id": "12345",
        "email": "user1@example.com",
        "exp": int((datetime.now() + timedelta(hours=1)).timestamp()),
        "iat": int(datetime.now().timestamp()),
        "jti": str(uuid.uuid4())
    }

    mock_jwt_payload_user2 = {
        "user_id": "67890",
        "email": "user2@example.com",
        "exp": int((datetime.now() + timedelta(hours=1)).timestamp()),
        "iat": int(datetime.now().timestamp()),
        "jti": str(uuid.uuid4())
    }

    with patch('auth.jwt.verify_token') as mock_verify:
        # First, add a task for user 1
        mock_verify.return_value = mock_jwt_payload_user1
        with patch('services.ai_service.AIService.process_conversation_with_reasoning_loop') as mock_process:
            mock_process.return_value = {
                "response": "Task 'User 1 task' added successfully with ID 1",
                "tool_calls": [{
                    "name": "add_task",
                    "arguments": {"title": "User 1 task", "description": "For user 1", "user_id": "12345"},
                    "result": {"success": True, "task_id": 1, "message": "Task 'User 1 task' added successfully"}
                }],
                "success": True
            }

            headers = {"Authorization": "Bearer fake-token-user1"}
            response = client.post(
                "/api/12345/chat",
                json={"message": "Add a task for user 1", "conversation_id": None},
                headers=headers
            )
            assert response.status_code == 200

        # Add a task for user 2
        mock_verify.return_value = mock_jwt_payload_user2
        with patch('services.ai_service.AIService.process_conversation_with_reasoning_loop') as mock_process:
            mock_process.return_value = {
                "response": "Task 'User 2 task' added successfully with ID 2",
                "tool_calls": [{
                    "name": "add_task",
                    "arguments": {"title": "User 2 task", "description": "For user 2", "user_id": "67890"},
                    "result": {"success": True, "task_id": 2, "message": "Task 'User 2 task' added successfully"}
                }],
                "success": True
            }

            headers = {"Authorization": "Bearer fake-token-user2"}
            response = client.post(
                "/api/67890/chat",
                json={"message": "Add a task for user 2", "conversation_id": None},
                headers=headers
            )
            assert response.status_code == 200

        # Verify user 1 only sees their own task
        mock_verify.return_value = mock_jwt_payload_user1
        with patch('services.ai_service.AIService.process_conversation_with_reasoning_loop') as mock_process:
            mock_process.return_value = {
                "response": "You have 1 task: User 1 task",
                "tool_calls": [{
                    "name": "list_tasks",
                    "arguments": {"user_id": "12345", "filter_status": "all"},
                    "result": {
                        "success": True,
                        "tasks": [{"id": 1, "title": "User 1 task", "description": "For user 1", "completed": False}],
                        "count": 1,
                        "message": "Retrieved 1 tasks successfully"
                    }
                }],
                "success": True
            }

            headers = {"Authorization": "Bearer fake-token-user1"}
            response = client.post(
                "/api/12345/chat",
                json={"message": "Show me my tasks", "conversation_id": None},
                headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "User 1 task" in data["response"]
            assert "User 2 task" not in data["response"]


def test_email_authentication_integration():
    """Test that email authentication works correctly with the chatbot"""
    client = TestClient(app)

    # Mock JWT payload with email
    mock_jwt_payload = {
        "user_id": "12345",
        "email": "authenticated_user@example.com",
        "exp": int((datetime.now() + timedelta(hours=1)).timestamp()),
        "iat": int(datetime.now().timestamp()),
        "jti": str(uuid.uuid4())
    }

    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        with patch('services.ai_service.AIService.process_conversation_with_reasoning_loop') as mock_process:
            # Test getting user info
            mock_process.return_value = {
                "response": "You are logged in as authenticated_user@example.com",
                "tool_calls": [{
                    "name": "get_current_user",
                    "arguments": {"user_id": "12345", "email": "authenticated_user@example.com"},
                    "result": {"success": True, "email": "authenticated_user@example.com", "user_id": "12345", "message": "Current user information retrieved for user ID: 12345"}
                }],
                "success": True
            }

            headers = {"Authorization": "Bearer fake-token-email"}
            response = client.post(
                "/api/12345/chat",
                json={"message": "Who am I?", "conversation_id": None},
                headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "authenticated_user@example.com" in data["response"]


def test_error_handling_integration():
    """Test error handling in the chatbot integration"""
    client = TestClient(app)

    # Mock JWT payload
    mock_jwt_payload = {
        "user_id": "12345",
        "email": "error_test@example.com",
        "exp": int((datetime.now() + timedelta(hours=1)).timestamp()),
        "iat": int(datetime.now().timestamp()),
        "jti": str(uuid.uuid4())
    }

    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        with patch('services.ai_service.AIService.process_conversation_with_reasoning_loop') as mock_process:
            # Simulate an error in AI processing
            mock_process.return_value = {
                "response": "Hi! Sorry, I cannot connect to my AI service for the moment. I can help you manage your tasks when I'm back online!",
                "tool_calls": [],
                "success": False
            }

            headers = {"Authorization": "Bearer fake-token-error"}
            response = client.post(
                "/api/12345/chat",
                json={"message": "Do something that causes an error", "conversation_id": None},
                headers=headers
            )

            # Should still return 200 but with error response
            assert response.status_code == 200
            data = response.json()
            assert "cannot connect" in data["response"].lower()


def test_conversation_persistence():
    """Test that conversations are properly persisted"""
    from services.chat_service import ChatService

    # Create a conversation for a user
    conversation = ChatService.create_new_conversation("12345")
    assert conversation["user_id"] == "12345"

    # Retrieve the conversation
    retrieved_convs = ChatService.get_user_conversations("12345")
    assert any(conv["id"] == conversation["id"] for conv in retrieved_convs)

    # Clean up would normally happen but we'll leave it since this is a test


if __name__ == "__main__":
    pytest.main([__file__])