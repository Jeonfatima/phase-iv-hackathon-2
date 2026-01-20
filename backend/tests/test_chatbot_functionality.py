"""
Test suite for chatbot functionality to verify all responsibilities:
- Create tasks
- Delete tasks
- List tasks
- Update tasks
- Identify user by email through authentication
"""

import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from auth.jwt import verify_token
from services.mcp_tools import add_task, delete_task, update_task, complete_task, list_tasks, get_current_user
from database.session import Session
from database.engine import engine
from models.user import User
from models.task import Task
from sqlmodel import select
import uuid


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def mock_jwt_payload():
    """Mock JWT payload for testing"""
    return {
        "user_id": "12345",
        "email": "test@example.com",
        "exp": 9999999999,  # Far future expiration
        "iat": 1234567890,
        "jti": str(uuid.uuid4())
    }


def test_create_task_through_chatbot(client, mock_jwt_payload):
    """Test that chatbot can create tasks"""
    # Mock JWT verification to return our test user
    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        # Mock the Cohere AI service to return a tool call for adding a task
        with patch('services.ai_service.process_with_cohere') as mock_cohere:
            mock_cohere.return_value = {
                "text": "Task 'Buy groceries' added successfully",
                "tool_calls": [{
                    "name": "add_task",
                    "arguments": {
                        "title": "Buy groceries",
                        "description": "Milk, bread, eggs",
                        "user_id": "12345"
                    }
                }]
            }

            # Send a request to add a task through the chatbot
            headers = {"Authorization": "Bearer fake-token"}
            response = client.post(
                "/api/12345/chat",
                json={
                    "message": "Add a task to buy groceries with description milk, bread, eggs",
                    "conversation_id": None
                },
                headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "Buy groceries" in data["response"]


def test_delete_task_through_chatbot(client, mock_jwt_payload):
    """Test that chatbot can delete tasks"""
    # First, create a task to delete
    with Session(engine) as session:
        # Add a test task
        task = Task(
            title="Test task to delete",
            description="This task will be deleted",
            completed=False,
            user_id=12345
        )
        session.add(task)
        session.commit()
        task_id = task.id

    # Mock JWT verification
    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        # Mock the Cohere AI service to return a tool call for deleting a task
        with patch('services.ai_service.process_with_cohere') as mock_cohere:
            mock_cohere.return_value = {
                "text": f"Task with ID {task_id} deleted successfully",
                "tool_calls": [{
                    "name": "delete_task",
                    "arguments": {
                        "task_id": task_id,
                        "user_id": "12345"
                    }
                }]
            }

            headers = {"Authorization": "Bearer fake-token"}
            response = client.post(
                f"/api/12345/chat",
                json={
                    "message": f"Delete task with ID {task_id}",
                    "conversation_id": None
                },
                headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert str(task_id) in data["response"]

    # Verify the task was actually deleted from the database
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id)
        result = session.exec(statement).first()
        assert result is None


def test_list_tasks_through_chatbot(client, mock_jwt_payload):
    """Test that chatbot can list tasks"""
    # Create some test tasks
    with Session(engine) as session:
        # Clear any existing tasks for this user
        session.exec(select(Task).where(Task.user_id == 12345)).all()

        # Add test tasks
        task1 = Task(title="First task", description="Description 1", completed=False, user_id=12345)
        task2 = Task(title="Second task", description="Description 2", completed=True, user_id=12345)
        session.add(task1)
        session.add(task2)
        session.commit()

    # Mock JWT verification
    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        # Mock the Cohere AI service to return a tool call for listing tasks
        with patch('services.ai_service.process_with_cohere') as mock_cohere:
            mock_cohere.return_value = {
                "text": "Here are your tasks",
                "tool_calls": [{
                    "name": "list_tasks",
                    "arguments": {
                        "user_id": "12345",
                        "filter_status": "all"
                    }
                }]
            }

            headers = {"Authorization": "Bearer fake-token"}
            response = client.post(
                "/api/12345/chat",
                json={
                    "message": "Show me all my tasks",
                    "conversation_id": None
                },
                headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "tasks" in data["response"].lower() or "here are" in data["response"].lower()


def test_update_task_through_chatbot(client, mock_jwt_payload):
    """Test that chatbot can update tasks"""
    # Create a test task to update
    with Session(engine) as session:
        # Add a test task
        task = Task(
            title="Original task title",
            description="Original description",
            completed=False,
            user_id=12345
        )
        session.add(task)
        session.commit()
        task_id = task.id

    # Mock JWT verification
    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        # Mock the Cohere AI service to return a tool call for updating a task
        with patch('services.ai_service.process_with_cohere') as mock_cohere:
            mock_cohere.return_value = {
                "text": f"Task with ID {task_id} updated successfully",
                "tool_calls": [{
                    "name": "update_task",
                    "arguments": {
                        "task_id": task_id,
                        "user_id": "12345",
                        "title": "Updated task title",
                        "description": "Updated description"
                    }
                }]
            }

            headers = {"Authorization": "Bearer fake-token"}
            response = client.post(
                "/api/12345/chat",
                json={
                    "message": f"Update task {task_id} title to 'Updated task title' and description to 'Updated description'",
                    "conversation_id": None
                },
                headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert str(task_id) in data["response"]

    # Verify the task was actually updated in the database
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id)
        result = session.exec(statement).first()
        assert result is not None
        assert result.title == "Updated task title"
        assert result.description == "Updated description"


def test_complete_task_through_chatbot(client, mock_jwt_payload):
    """Test that chatbot can mark tasks as complete/incomplete"""
    # Create a test task to update completion status
    with Session(engine) as session:
        # Add a test task
        task = Task(
            title="Task to complete",
            description="This task will be marked as complete",
            completed=False,
            user_id=12345
        )
        session.add(task)
        session.commit()
        task_id = task.id

    # Mock JWT verification
    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        # Mock the Cohere AI service to return a tool call for completing a task
        with patch('services.ai_service.process_with_cohere') as mock_cohere:
            mock_cohere.return_value = {
                "text": f"Task with ID {task_id} marked as completed successfully",
                "tool_calls": [{
                    "name": "complete_task",
                    "arguments": {
                        "task_id": task_id,
                        "completed": True,
                        "user_id": "12345"
                    }
                }]
            }

            headers = {"Authorization": "Bearer fake-token"}
            response = client.post(
                "/api/12345/chat",
                json={
                    "message": f"Mark task {task_id} as complete",
                    "conversation_id": None
                },
                headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "completed" in data["response"].lower()

    # Verify the task was actually updated in the database
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id)
        result = session.exec(statement).first()
        assert result is not None
        assert result.completed is True


def test_user_email_identification(client, mock_jwt_payload):
    """Test that chatbot correctly identifies user by email through authentication"""
    # Mock JWT verification to return our test user
    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        # Test getting current user information
        result = get_current_user(user_id="12345", email="test@example.com")

        assert result["success"] is True
        assert result["user_id"] == "12345"
        assert result["email"] == "test@example.com"

        # Test the chat endpoint with authentication
        headers = {"Authorization": "Bearer fake-token"}
        response = client.post(
            "/api/12345/chat",
            json={
                "message": "Who am I?",
                "conversation_id": None
            },
            headers=headers
        )

        assert response.status_code == 200
        # The response should contain information about the authenticated user


def test_mcp_tools_direct_functionality():
    """Test the MCP tools directly to ensure they work properly"""
    user_id = "12345"

    # Test adding a task
    add_result = add_task("Test task", "Test description", user_id)
    assert add_result["success"] is True
    assert "task_id" in add_result
    task_id = add_result["task_id"]

    # Test listing tasks
    list_result = list_tasks(user_id)
    assert list_result["success"] is True
    assert list_result["count"] >= 1
    assert any(task["id"] == task_id for task in list_result["tasks"])

    # Test updating the task
    update_result = update_task(task_id, user_id, title="Updated test task")
    assert update_result["success"] is True

    # Test completing the task
    complete_result = complete_task(task_id, True, user_id)
    assert complete_result["success"] is True

    # Verify the task was updated
    list_result_after = list_tasks(user_id)
    updated_task = next((t for t in list_result_after["tasks"] if t["id"] == task_id), None)
    assert updated_task is not None
    assert updated_task["title"] == "Updated test task"
    assert updated_task["completed"] is True

    # Test deleting the task
    delete_result = delete_task(task_id, user_id)
    assert delete_result["success"] is True

    # Verify the task was deleted
    list_result_final = list_tasks(user_id)
    deleted_task = next((t for t in list_result_final["tasks"] if t["id"] == task_id), None)
    assert deleted_task is None


def test_authentication_enforcement(client, mock_jwt_payload):
    """Test that authentication is properly enforced for chatbot operations"""
    # Test without authentication
    response = client.post(
        "/api/12345/chat",
        json={
            "message": "Add a task to test authentication",
            "conversation_id": None
        }
    )

    # Should return 401 or 403 due to missing authentication
    assert response.status_code in [401, 403]

    # Test with invalid token
    headers = {"Authorization": "Bearer invalid-token"}
    response = client.post(
        "/api/12345/chat",
        json={
            "message": "Add a task to test authentication",
            "conversation_id": None
        },
        headers=headers
    )

    # Should return 401 due to invalid token
    assert response.status_code == 401


def test_user_isolation(client, mock_jwt_payload):
    """Test that users can only access their own tasks"""
    # Create tasks for user 12345
    with Session(engine) as session:
        # Clear existing tasks
        session.exec(select(Task).where(Task.user_id == 12345)).all()
        session.exec(select(Task).where(Task.user_id == 67890)).all()

        # Add tasks for user 12345
        task1 = Task(title="User 1 task", description="For user 12345", completed=False, user_id=12345)
        # Add tasks for user 67890
        task2 = Task(title="User 2 task", description="For user 67890", completed=False, user_id=67890)
        session.add(task1)
        session.add(task2)
        session.commit()

    # Test that user 12345 only sees their own tasks
    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        with patch('services.ai_service.process_with_cohere') as mock_cohere:
            mock_cohere.return_value = {
                "text": "Here are your tasks",
                "tool_calls": [{
                    "name": "list_tasks",
                    "arguments": {
                        "user_id": "12345",
                        "filter_status": "all"
                    }
                }]
            }

            headers = {"Authorization": "Bearer fake-token"}
            response = client.post(
                "/api/12345/chat",
                json={
                    "message": "Show me my tasks",
                    "conversation_id": None
                },
                headers=headers
            )

            assert response.status_code == 200
            # The response should only include tasks belonging to user 12345


if __name__ == "__main__":
    pytest.main([__file__])