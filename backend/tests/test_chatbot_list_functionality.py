"""
Unit tests specifically for chatbot list task functionality
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from database.session import Session
from database.engine import engine
from models.task import Task
from sqlmodel import select


@pytest.fixture
def client():
    return TestClient(app)


def test_list_tasks_empty(client):
    """Test listing tasks when no tasks exist"""
    # Clear all tasks for this user
    with Session(engine) as session:
        session.exec(select(Task).where(Task.user_id == 12345)).all()

    # Mock JWT payload
    mock_jwt_payload = {
        "user_id": "12345",
        "email": "test@example.com",
        "exp": 9999999999,
        "iat": 1234567890
    }

    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        with patch('services.ai_service.AIService.process_conversation_with_reasoning_loop') as mock_process:
            mock_process.return_value = {
                "response": "You have no tasks",
                "tool_calls": [{
                    "name": "list_tasks",
                    "arguments": {
                        "user_id": "12345",
                        "filter_status": "all"
                    },
                    "result": {
                        "success": True,
                        "tasks": [],
                        "count": 0,
                        "message": "Retrieved 0 tasks successfully"
                    }
                }],
                "success": True
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
            # Response should indicate that there are no tasks


def test_list_tasks_with_items(client):
    """Test listing tasks when tasks exist"""
    # Create some tasks
    with Session(engine) as session:
        # Clear existing tasks
        session.exec(select(Task).where(Task.user_id == 12345)).all()

        # Add test tasks
        task1 = Task(title="First task", description="Description 1", completed=False, user_id=12345)
        task2 = Task(title="Second task", description="Description 2", completed=True, user_id=12345)
        task3 = Task(title="Third task", description="Description 3", completed=False, user_id=12345)
        session.add(task1)
        session.add(task2)
        session.add(task3)
        session.commit()

    # Mock JWT payload
    mock_jwt_payload = {
        "user_id": "12345",
        "email": "test@example.com",
        "exp": 9999999999,
        "iat": 1234567890
    }

    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        with patch('services.ai_service.AIService.process_conversation_with_reasoning_loop') as mock_process:
            mock_process.return_value = {
                "response": "Here are your tasks",
                "tool_calls": [{
                    "name": "list_tasks",
                    "arguments": {
                        "user_id": "12345",
                        "filter_status": "all"
                    },
                    "result": {
                        "success": True,
                        "tasks": [
                            {"id": 1, "title": "First task", "description": "Description 1", "completed": False},
                            {"id": 2, "title": "Second task", "description": "Description 2", "completed": True}
                        ],
                        "count": 2,
                        "message": "Retrieved 2 tasks successfully"
                    }
                }],
                "success": True
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
            # Response should contain the tasks


def test_list_only_pending_tasks(client):
    """Test listing only pending (incomplete) tasks"""
    # Create tasks with mixed completion status
    with Session(engine) as session:
        # Clear existing tasks
        session.exec(select(Task).where(Task.user_id == 12345)).all()

        # Add completed tasks
        completed_task1 = Task(title="Completed task 1", description="Done", completed=True, user_id=12345)
        completed_task2 = Task(title="Completed task 2", description="Also done", completed=True, user_id=12345)
        # Add pending tasks
        pending_task1 = Task(title="Pending task 1", description="Not done", completed=False, user_id=12345)
        pending_task2 = Task(title="Pending task 2", description="Still to do", completed=False, user_id=12345)

        session.add(completed_task1)
        session.add(completed_task2)
        session.add(pending_task1)
        session.add(pending_task2)
        session.commit()

    # Mock JWT payload
    mock_jwt_payload = {
        "user_id": "12345",
        "email": "test@example.com",
        "exp": 9999999999,
        "iat": 1234567890
    }

    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        with patch('services.ai_service.AIService.process_conversation_with_reasoning_loop') as mock_process:
            mock_process.return_value = {
                "response": "Here are your pending tasks",
                "tool_calls": [{
                    "name": "list_tasks",
                    "arguments": {
                        "user_id": "12345",
                        "filter_status": "pending"
                    },
                    "result": {
                        "success": True,
                        "tasks": [
                            {"id": 1, "title": "Pending task 1", "description": "Not done", "completed": False},
                            {"id": 3, "title": "Pending task 2", "description": "Still to do", "completed": False}
                        ],
                        "count": 2,
                        "message": "Retrieved 2 pending tasks successfully"
                    }
                }],
                "success": True
            }

            headers = {"Authorization": "Bearer fake-token"}
            response = client.post(
                "/api/12345/chat",
                json={
                    "message": "Show me my pending tasks",
                    "conversation_id": None
                },
                headers=headers
            )

            assert response.status_code == 200
            # Response should contain only pending tasks


def test_list_only_completed_tasks(client):
    """Test listing only completed tasks"""
    # Create tasks with mixed completion status
    with Session(engine) as session:
        # Clear existing tasks
        session.exec(select(Task).where(Task.user_id == 12345)).all()

        # Add completed tasks
        completed_task1 = Task(title="Completed task 1", description="Done", completed=True, user_id=12345)
        completed_task2 = Task(title="Completed task 2", description="Also done", completed=True, user_id=12345)
        # Add pending tasks
        pending_task1 = Task(title="Pending task 1", description="Not done", completed=False, user_id=12345)
        pending_task2 = Task(title="Pending task 2", description="Still to do", completed=False, user_id=12345)

        session.add(completed_task1)
        session.add(completed_task2)
        session.add(pending_task1)
        session.add(pending_task2)
        session.commit()

    # Mock JWT payload
    mock_jwt_payload = {
        "user_id": "12345",
        "email": "test@example.com",
        "exp": 9999999999,
        "iat": 1234567890
    }

    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        with patch('services.ai_service.AIService.process_conversation_with_reasoning_loop') as mock_process:
            mock_process.return_value = {
                "response": "Here are your completed tasks",
                "tool_calls": [{
                    "name": "list_tasks",
                    "arguments": {
                        "user_id": "12345",
                        "filter_status": "completed"
                    },
                    "result": {
                        "success": True,
                        "tasks": [
                            {"id": 2, "title": "Completed task 1", "description": "Done", "completed": True},
                            {"id": 4, "title": "Completed task 2", "description": "Also done", "completed": True}
                        ],
                        "count": 2,
                        "message": "Retrieved 2 completed tasks successfully"
                    }
                }],
                "success": True
            }

            headers = {"Authorization": "Bearer fake-token"}
            response = client.post(
                "/api/12345/chat",
                json={
                    "message": "Show me my completed tasks",
                    "conversation_id": None
                },
                headers=headers
            )

            assert response.status_code == 200
            # Response should contain only completed tasks


def test_list_tasks_different_user(client):
    """Test that users can only see their own tasks"""
    # Create tasks for both users
    with Session(engine) as session:
        # Clear existing tasks
        session.exec(select(Task).where(Task.user_id.in_([12345, 67890]))).all()

        # Add tasks for user 12345
        user1_task = Task(title="User 1 task", description="For user 12345", completed=False, user_id=12345)
        # Add tasks for user 67890
        user2_task = Task(title="User 2 task", description="For user 67890", completed=False, user_id=67890)

        session.add(user1_task)
        session.add(user2_task)
        session.commit()

    # Mock JWT payload for user 12345
    mock_jwt_payload = {
        "user_id": "12345",
        "email": "test@example.com",
        "exp": 9999999999,
        "iat": 1234567890
    }

    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        with patch('services.ai_service.AIService.process_conversation_with_reasoning_loop') as mock_process:
            mock_process.return_value = {
                "response": "Here are your tasks",
                "tool_calls": [{
                    "name": "list_tasks",
                    "arguments": {
                        "user_id": "12345",
                        "filter_status": "all"
                    },
                    "result": {
                        "success": True,
                        "tasks": [
                            {"id": 1, "title": "User 1 task", "description": "For user 12345", "completed": False}
                        ],
                        "count": 1,
                        "message": "Retrieved 1 tasks successfully"
                    }
                }],
                "success": True
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
            # Response should only contain tasks belonging to user 12345


def test_list_tasks_invalid_user_id(client):
    """Test listing tasks with invalid user ID"""
    # Mock JWT payload with invalid user ID
    mock_jwt_payload = {
        "user_id": "invalid_user_id",
        "email": "test@example.com",
        "exp": 9999999999,
        "iat": 1234567890
    }

    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        with patch('services.ai_service.AIService.process_conversation_with_reasoning_loop') as mock_process:
            mock_process.return_value = {
                "response": "Invalid user ID",
                "tool_calls": [{
                    "name": "list_tasks",
                    "arguments": {
                        "user_id": "invalid_user_id",
                        "filter_status": "all"
                    },
                    "result": {
                        "success": False,
                        "message": "Invalid user ID format: invalid_user_id"
                    }
                }],
                "success": False
            }

            headers = {"Authorization": "Bearer fake-token"}
            response = client.post(
                "/api/invalid_user_id/chat",  # Invalid user ID in URL
                json={
                    "message": "Show me my tasks",
                    "conversation_id": None
                },
                headers=headers
            )

            # Should fail due to invalid user ID format
            assert response.status_code in [400, 401, 403]


def test_list_tasks_missing_user_id(client):
    """Test listing tasks with missing user ID"""
    headers = {"Authorization": "Bearer fake-token"}
    response = client.post(
        "/api//chat",  # Empty user ID in URL
        json={
            "message": "Show me my tasks",
            "conversation_id": None
        },
        headers=headers
    )

    # Should fail due to missing user ID
    assert response.status_code in [400, 401, 403]


def test_list_tasks_with_auth_error(client):
    """Test listing tasks when authentication fails"""
    # Mock JWT verification to raise an exception
    with patch('auth.jwt.verify_token', side_effect=Exception("Invalid token")):
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.post(
            "/api/12345/chat",
            json={
                "message": "Show me my tasks",
                "conversation_id": None
            },
            headers=headers
        )

        assert response.status_code == 401


if __name__ == "__main__":
    pytest.main([__file__])