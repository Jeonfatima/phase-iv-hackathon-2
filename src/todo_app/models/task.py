"""
Task model representing a single todo item.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo item with id, title, description, and completion status.

    Attributes:
        id: Unique integer identifier for the task
        title: Required string title (max 100 characters)
        description: Optional string description (max 500 characters)
        completed: Boolean indicating completion status (default False)
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self):
        """Validate the task after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty or whitespace-only")

        if len(self.title) > 100:
            raise ValueError("Title must be 100 characters or less")

        if self.description and len(self.description) > 500:
            raise ValueError("Description must be 500 characters or less")

        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("ID must be a positive integer")

        # Clean up whitespace
        self.title = self.title.strip()
        if self.description:
            self.description = self.description.strip()