"""
Unit tests for the Task model.
"""
import pytest
from src.todo_app.models.task import Task


class TestTaskModel:
    """Test cases for the Task model."""

    def test_task_creation_valid(self):
        """Test creating a valid task."""
        task = Task(id=1, title="Test Task", description="Test Description", completed=False)
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_task_creation_minimal(self):
        """Test creating a task with minimal required fields."""
        task = Task(id=1, title="Test Task")
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description is None
        assert task.completed is False

    def test_task_title_required(self):
        """Test that title is required."""
        with pytest.raises(ValueError, match="Title cannot be empty or whitespace-only"):
            Task(id=1, title="")

    def test_task_title_whitespace_only(self):
        """Test that title cannot be whitespace only."""
        with pytest.raises(ValueError, match="Title cannot be empty or whitespace-only"):
            Task(id=1, title="   ")

    def test_task_title_max_length(self):
        """Test that title cannot exceed 100 characters."""
        long_title = "A" * 101
        with pytest.raises(ValueError, match="Title must be 100 characters or less"):
            Task(id=1, title=long_title)

    def test_task_description_max_length(self):
        """Test that description cannot exceed 500 characters."""
        long_description = "A" * 501
        with pytest.raises(ValueError, match="Description must be 500 characters or less"):
            Task(id=1, title="Test", description=long_description)

    def test_task_id_must_be_positive(self):
        """Test that ID must be a positive integer."""
        with pytest.raises(ValueError, match="ID must be a positive integer"):
            Task(id=0, title="Test Task")

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            Task(id=-1, title="Test Task")

    def test_task_title_stripped(self):
        """Test that title is automatically stripped of whitespace."""
        task = Task(id=1, title="  Test Task  ", description="  Test Description  ")
        assert task.title == "Test Task"
        assert task.description == "Test Description"

    def test_task_completed_default_false(self):
        """Test that completed defaults to False."""
        task = Task(id=1, title="Test Task")
        assert task.completed is False