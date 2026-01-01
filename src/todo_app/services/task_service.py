"""
Task service for managing tasks in memory.
"""
from typing import List, Optional
from ..models.task import Task


class TaskService:
    """
    Service class for managing tasks in memory.
    """
    def __init__(self):
        self._tasks = {}  # Dictionary to store tasks by ID
        self._next_id = 1  # Auto-increment ID counter

    def create_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Create a new task with a unique auto-incremented ID.

        Args:
            title: The task title (required)
            description: The task description (optional)

        Returns:
            The created Task object
        """
        # Validate input
        if not title or not title.strip():
            raise ValueError("Title cannot be empty or whitespace-only")

        if len(title) > 100:
            raise ValueError("Title must be 100 characters or less")

        if description and len(description) > 500:
            raise ValueError("Description must be 500 characters or less")

        # Create task with auto-incremented ID
        task = Task(
            id=self._next_id,
            title=title.strip(),
            description=description.strip() if description else None,
            completed=False
        )

        # Store task and increment ID counter
        self._tasks[task.id] = task
        self._next_id += 1

        return task

    def get_task_by_id(self, task_id: int) -> Task:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object

        Raises:
            ValueError: If the task ID does not exist
        """
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} does not exist")
        return self._tasks[task_id]

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            List of all Task objects, ordered by creation (ID)
        """
        return [self._tasks[tid] for tid in sorted(self._tasks.keys())]

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task:
        """
        Update an existing task.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            The updated Task object

        Raises:
            ValueError: If the task ID does not exist or if title is invalid
        """
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} does not exist")

        task = self._tasks[task_id]

        # Use existing values if not provided
        new_title = title if title is not None else task.title
        new_description = description if description is not None else task.description

        # Validate new values
        if new_title and (not new_title.strip() or len(new_title) > 100):
            if not new_title.strip():
                raise ValueError("Title cannot be empty or whitespace-only")
            else:
                raise ValueError("Title must be 100 characters or less")

        if new_description and len(new_description) > 500:
            raise ValueError("Description must be 500 characters or less")

        # Update task
        task.title = new_title.strip()
        task.description = new_description.strip() if new_description else new_description

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if it did not exist
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def toggle_task_completion(self, task_id: int) -> Task:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            The updated Task object with toggled completion status

        Raises:
            ValueError: If the task ID does not exist
        """
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} does not exist")

        task = self._tasks[task_id]
        task.completed = not task.completed
        return task