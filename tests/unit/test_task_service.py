"""
Unit tests for the TaskService.
"""
import pytest
from src.todo_app.services.task_service import TaskService
from src.todo_app.models.task import Task


class TestTaskService:
    """Test cases for the TaskService."""

    def test_create_task_success(self):
        """Test creating a task successfully."""
        service = TaskService()
        task = service.create_task("Test Task", "Test Description")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_create_task_minimal(self):
        """Test creating a task with minimal parameters."""
        service = TaskService()
        task = service.create_task("Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description is None
        assert task.completed is False

    def test_create_task_auto_increment_id(self):
        """Test that task IDs are auto-incremented."""
        service = TaskService()
        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2")

        assert task1.id == 1
        assert task2.id == 2

    def test_create_task_title_required(self):
        """Test that title is required for task creation."""
        service = TaskService()
        with pytest.raises(ValueError, match="Title cannot be empty or whitespace-only"):
            service.create_task("")

    def test_create_task_title_whitespace_only(self):
        """Test that title cannot be whitespace only."""
        service = TaskService()
        with pytest.raises(ValueError, match="Title cannot be empty or whitespace-only"):
            service.create_task("   ")

    def test_create_task_title_max_length(self):
        """Test that title cannot exceed 100 characters."""
        service = TaskService()
        long_title = "A" * 101
        with pytest.raises(ValueError, match="Title must be 100 characters or less"):
            service.create_task(long_title)

    def test_create_task_description_max_length(self):
        """Test that description cannot exceed 500 characters."""
        service = TaskService()
        long_description = "A" * 501
        with pytest.raises(ValueError, match="Description must be 500 characters or less"):
            service.create_task("Test Task", long_description)

    def test_get_task_by_id_success(self):
        """Test getting a task by ID successfully."""
        service = TaskService()
        created_task = service.create_task("Test Task")

        retrieved_task = service.get_task_by_id(created_task.id)
        assert retrieved_task.id == created_task.id
        assert retrieved_task.title == created_task.title
        assert retrieved_task.description == created_task.description
        assert retrieved_task.completed == created_task.completed

    def test_get_task_by_id_not_found(self):
        """Test getting a non-existent task raises an error."""
        service = TaskService()
        with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
            service.get_task_by_id(999)

    def test_get_all_tasks_empty(self):
        """Test getting all tasks when none exist."""
        service = TaskService()
        tasks = service.get_all_tasks()

        assert len(tasks) == 0

    def test_get_all_tasks_multiple(self):
        """Test getting all tasks."""
        service = TaskService()
        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2")
        task3 = service.create_task("Task 3")

        tasks = service.get_all_tasks()

        assert len(tasks) == 3
        assert tasks[0].id == task1.id
        assert tasks[1].id == task2.id
        assert tasks[2].id == task3.id

    def test_update_task_success(self):
        """Test updating a task successfully."""
        service = TaskService()
        original_task = service.create_task("Original Title", "Original Description")

        updated_task = service.update_task(original_task.id, "New Title", "New Description")

        assert updated_task.id == original_task.id
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        assert updated_task.completed == original_task.completed  # Should not change

    def test_update_task_partial(self):
        """Test updating only title or description."""
        service = TaskService()
        original_task = service.create_task("Original Title", "Original Description")

        # Update only title
        updated_task = service.update_task(original_task.id, title="New Title")
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"

        # Reset and update only description
        service = TaskService()
        original_task = service.create_task("Original Title", "Original Description")
        updated_task = service.update_task(original_task.id, description="New Description")
        assert updated_task.title == "Original Title"
        assert updated_task.description == "New Description"

    def test_update_task_not_found(self):
        """Test updating a non-existent task raises an error."""
        service = TaskService()
        with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
            service.update_task(999, "New Title")

    def test_update_task_title_validation(self):
        """Test that title validation applies during update."""
        service = TaskService()
        original_task = service.create_task("Original Title")

        with pytest.raises(ValueError, match="Title cannot be empty or whitespace-only"):
            service.update_task(original_task.id, title="   ")

        with pytest.raises(ValueError, match="Title must be 100 characters or less"):
            service.update_task(original_task.id, title="A" * 101)

    def test_delete_task_success(self):
        """Test deleting a task successfully."""
        service = TaskService()
        task = service.create_task("Test Task")

        result = service.delete_task(task.id)
        assert result is True

        # Verify the task no longer exists
        with pytest.raises(ValueError):
            service.get_task_by_id(task.id)

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task returns False."""
        service = TaskService()
        result = service.delete_task(999)
        assert result is False

    def test_toggle_task_completion(self):
        """Test toggling task completion status."""
        service = TaskService()
        task = service.create_task("Test Task")

        # Initially False
        assert task.completed is False

        # Toggle to True
        toggled_task = service.toggle_task_completion(task.id)
        assert toggled_task.completed is True

        # Toggle back to False
        toggled_task = service.toggle_task_completion(task.id)
        assert toggled_task.completed is False

    def test_toggle_task_completion_not_found(self):
        """Test toggling completion of non-existent task raises an error."""
        service = TaskService()
        with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
            service.toggle_task_completion(999)