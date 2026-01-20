"""
Unit tests specifically for chatbot delete task functionality
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


def test_delete_existing_task(client):
    """Test deleting an existing task via chatbot"""
    # Create a task to delete
    with Session(engine) as session:
        task = Task(
            title="Task to delete",
            description="This will be deleted",
            completed=False,
            user_id=12345
        )
        session.add(task)
        session.commit()
        task_id = task.id

    # Mock JWT payload
    mock_jwt_payload = {
        "user_id": "12345",
        "email": "test@example.com",
        "exp": 9999999999,
        "iat": 1234567890
    }

    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
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
                "/api/12345/chat",
                json={
                    "message": f"Delete task {task_id}",
                    "conversation_id": None
                },
                headers=headers
            )

            assert response.status_code == 200
            assert str(task_id) in response.json()["response"]

    # Verify task was deleted
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id)
        result = session.exec(statement).first()
        assert result is None


def test_delete_nonexistent_task(client):
    """Test deleting a non-existent task via chatbot"""
    nonexistent_task_id = 999999

    # Mock JWT payload
    mock_jwt_payload = {
        "user_id": "12345",
        "email": "test@example.com",
        "exp": 9999999999,
        "iat": 1234567890
    }

    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        with patch('services.ai_service.process_with_cohere') as mock_cohere:
            mock_cohere.return_value = {
                "text": f"Task with ID {nonexistent_task_id} not found",
                "tool_calls": [{
                    "name": "delete_task",
                    "arguments": {
                        "task_id": nonexistent_task_id,
                        "user_id": "12345"
                    }
                }]
            }

            headers = {"Authorization": "Bearer fake-token"}
            response = client.post(
                "/api/12345/chat",
                json={
                    "message": f"Delete task {nonexistent_task_id}",
                    "conversation_id": None
                },
                headers=headers
            )

            assert response.status_code == 200
            # Response should indicate that the task wasn't found


def test_delete_other_users_task(client):
    """Test that a user cannot delete another user's task"""
    # Create a task for a different user
    with Session(engine) as session:
        task = Task(
            title="Another user's task",
            description="This belongs to another user",
            completed=False,
            user_id=67890  # Different user
        )
        session.add(task)
        session.commit()
        task_id = task.id

    # Mock JWT payload for original user
    mock_jwt_payload = {
        "user_id": "12345",
        "email": "test@example.com",
        "exp": 9999999999,
        "iat": 1234567890
    }

    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        with patch('services.ai_service.process_with_cohere') as mock_cohere:
            mock_cohere.return_value = {
                "text": f"Task with ID {task_id} not found or does not belong to user",
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
                "/api/12345/chat",
                json={
                    "message": f"Delete task {task_id}",
                    "conversation_id": None
                },
                headers=headers
            )

            assert response.status_code == 200
            # Response should indicate that the task doesn't belong to the user


def test_delete_task_invalid_user_id_format(client):
    """Test deleting task with invalid user ID format"""
    # Mock JWT payload
    mock_jwt_payload = {
        "user_id": "invalid_user_id",
        "email": "test@example.com",
        "exp": 9999999999,
        "iat": 1234567890
    }

    with patch('auth.jwt.verify_token', return_value=mock_jwt_payload):
        with patch('services.ai_service.process_with_cohere') as mock_cohere:
            mock_cohere.return_value = {
                "text": "Invalid user ID format",
                "tool_calls": [{
                    "name": "delete_task",
                    "arguments": {
                        "task_id": 1,
                        "user_id": "invalid_user_id"
                    }
                }]
            }

            headers = {"Authorization": "Bearer fake-token"}
            response = client.post(
                "/api/invalid_user_id/chat",  # Invalid user ID in URL as well
                json={
                    "message": "Delete task 1",
                    "conversation_id": None
                },
                headers=headers
            )

            # Should fail due to invalid user ID format in URL
            assert response.status_code in [400, 401, 403]


def test_delete_task_missing_user_id(client):
    """Test deleting task with missing user ID"""
    headers = {"Authorization": "Bearer fake-token"}
    response = client.post(
        "/api//chat",  # Empty user ID in URL
        json={
            "message": "Delete task 1",
            "conversation_id": None
        },
        headers=headers
    )

    # Should fail due to missing user ID
    assert response.status_code in [400, 401, 403]


if __name__ == "__main__":
    pytest.main([__file__])