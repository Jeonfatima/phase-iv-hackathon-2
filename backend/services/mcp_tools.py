from typing import Dict, Any, Optional
from models.task import TaskCreate
from services.task_service import TaskService
from sqlmodel import Session
from database.session import get_session


def add_task(title: str, description: Optional[str] = None, user_id: str = None) -> Dict[str, Any]:
    """
    Creates a new task with title and optional description

    Args:
        title: The title of the task
        description: Optional description of the task
        user_id: The ID of the user creating the task

    Returns:
        Dictionary with success status, task_id, and message
    """
    try:
        # Validate inputs
        if not title or not title.strip():
            return {
                "success": False,
                "message": "Task title is required and cannot be empty"
            }

        if not user_id:
            return {
                "success": False,
                "message": "User ID is required to create a task"
            }

        # Convert user_id to int if it's a string representation of an integer
        try:
            user_id_int = int(user_id)
        except ValueError:
            return {
                "success": False,
                "message": f"Invalid user ID format: {user_id}"
            }

        # Create task data
        task_data = TaskCreate(
            title=title.strip(),
            description=description.strip() if description else None,
            completed=False
        )

        # Create database session and add task
        from database.session import Session
        from database.engine import engine
        with Session(engine) as session:
            task = TaskService.create_task(session, user_id_int, task_data)

        return {
            "success": True,
            "task_id": task.id,
            "message": f"Task '{task.title}' added successfully"
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to add task: {str(e)}"
        }


def delete_task(task_id: int, user_id: str = None) -> Dict[str, Any]:
    """
    Deletes an existing task by its ID

    Args:
        task_id: The ID of the task to delete
        user_id: The ID of the user attempting to delete the task

    Returns:
        Dictionary with success status and message
    """
    try:
        if not user_id:
            return {
                "success": False,
                "message": "User ID is required to delete a task"
            }

        # Convert user_id to int if it's a string representation of an integer
        try:
            user_id_int = int(user_id)
        except ValueError:
            return {
                "success": False,
                "message": f"Invalid user ID format: {user_id}"
            }

        # Validate task_id
        if not isinstance(task_id, int) or task_id <= 0:
            return {
                "success": False,
                "message": f"Invalid task ID: {task_id}"
            }

        # Create database session and delete task
        from database.session import Session
        from database.engine import engine
        with Session(engine) as session:
            success = TaskService.delete_task(session, user_id_int, task_id)

        if success:
            return {
                "success": True,
                "message": f"Task with ID {task_id} deleted successfully"
            }
        else:
            return {
                "success": False,
                "message": f"Task with ID {task_id} not found or does not belong to user"
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to delete task: {str(e)}"
        }


def update_task(
    task_id: int,
    user_id: str = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Updates properties of an existing task

    Args:
        task_id: The ID of the task to update
        user_id: The ID of the user attempting to update the task
        title: New title for the task (optional)
        description: New description for the task (optional)
        completed: New completion status for the task (optional)

    Returns:
        Dictionary with success status and message
    """
    try:
        if not user_id:
            return {
                "success": False,
                "message": "User ID is required to update a task"
            }

        # Convert user_id to int if it's a string representation of an integer
        try:
            user_id_int = int(user_id)
        except ValueError:
            return {
                "success": False,
                "message": f"Invalid user ID format: {user_id}"
            }

        # Validate task_id
        if not isinstance(task_id, int) or task_id <= 0:
            return {
                "success": False,
                "message": f"Invalid task ID: {task_id}"
            }

        # At least one field must be provided for update
        if all(field is None for field in [title, description, completed]):
            return {
                "success": False,
                "message": "At least one field (title, description, or completed) must be provided for update"
            }

        # Create update data
        from models.task import TaskUpdate
        update_data = {}
        if title is not None:
            update_data["title"] = title.strip() if title else ""
        if description is not None:
            update_data["description"] = description.strip() if description else None
        if completed is not None:
            update_data["completed"] = completed

        task_update = TaskUpdate(**update_data)

        # Create database session and update task
        from database.session import Session
        from database.engine import engine
        with Session(engine) as session:
            updated_task = TaskService.update_task(session, user_id_int, task_id, task_update)

        if updated_task:
            return {
                "success": True,
                "message": f"Task with ID {task_id} updated successfully"
            }
        else:
            return {
                "success": False,
                "message": f"Task with ID {task_id} not found or does not belong to user"
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to update task: {str(e)}"
        }


def complete_task(task_id: int, completed: bool, user_id: str = None) -> Dict[str, Any]:
    """
    Marks a task as complete or incomplete

    Args:
        task_id: The ID of the task to update
        completed: Whether the task should be marked as completed
        user_id: The ID of the user attempting to update the task

    Returns:
        Dictionary with success status and message
    """
    try:
        if not user_id:
            return {
                "success": False,
                "message": "User ID is required to update task completion status"
            }

        # Convert user_id to int if it's a string representation of an integer
        try:
            user_id_int = int(user_id)
        except ValueError:
            return {
                "success": False,
                "message": f"Invalid user ID format: {user_id}"
            }

        # Validate task_id
        if not isinstance(task_id, int) or task_id <= 0:
            return {
                "success": False,
                "message": f"Invalid task ID: {task_id}"
            }

        # Validate completed parameter
        if not isinstance(completed, bool):
            return {
                "success": False,
                "message": f"Completed parameter must be a boolean, got {type(completed).__name__}"
            }

        # Create database session and update task completion
        from database.session import Session
        from database.engine import engine
        with Session(engine) as session:
            updated_task = TaskService.update_task_completion(session, user_id_int, task_id, completed)

        if updated_task:
            status_text = "completed" if completed else "incomplete"
            return {
                "success": True,
                "message": f"Task with ID {task_id} marked as {status_text} successfully"
            }
        else:
            return {
                "success": False,
                "message": f"Task with ID {task_id} not found or does not belong to user"
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to update task completion status: {str(e)}"
        }


def list_tasks(user_id: str = None, filter_status: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieves all tasks for the current user with optional filtering

    Args:
        user_id: The ID of the user whose tasks to retrieve
        filter_status: Optional filter for task status ("all", "pending", "completed")

    Returns:
        Dictionary with success status, tasks list, and count
    """
    try:
        if not user_id:
            return {
                "success": False,
                "message": "User ID is required to list tasks",
                "tasks": [],
                "count": 0
            }

        # Convert user_id to int if it's a string representation of an integer
        try:
            user_id_int = int(user_id)
        except ValueError:
            return {
                "success": False,
                "message": f"Invalid user ID format: {user_id}",
                "tasks": [],
                "count": 0
            }

        # Validate filter_status if provided
        if filter_status and filter_status not in ["all", "pending", "completed"]:
            return {
                "success": False,
                "message": f"Invalid filter status: {filter_status}. Must be 'all', 'pending', or 'completed'",
                "tasks": [],
                "count": 0
            }

        # Create database session and get tasks
        from database.session import Session
        from database.engine import engine
        with Session(engine) as session:
            tasks = TaskService.get_all_tasks(session, user_id_int)

        # Apply filter if specified
        if filter_status == "pending":
            tasks = [task for task in tasks if not task.completed]
        elif filter_status == "completed":
            tasks = [task for task in tasks if task.completed]
        # If filter_status is "all" or None, return all tasks

        # Convert tasks to dictionaries for JSON serialization
        tasks_list = []
        for task in tasks:
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": task.user_id,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }
            tasks_list.append(task_dict)

        return {
            "success": True,
            "tasks": tasks_list,
            "count": len(tasks_list),
            "message": f"Retrieved {len(tasks_list)} tasks successfully"
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to list tasks: {str(e)}",
            "tasks": [],
            "count": 0
        }


def get_current_user(user_id: str = None, email: str = None) -> Dict[str, Any]:
    """
    Returns the current user's email and ID from authentication

    Args:
        user_id: The ID of the current user
        email: The email of the current user (if available)

    Returns:
        Dictionary with user email and ID
    """
    try:
        # This would normally come from the authentication system
        # For now, we'll return the user info that's provided
        if not user_id:
            return {
                "success": False,
                "message": "User ID is required to get user information",
                "email": None,
                "user_id": None
            }

        # In a real implementation, we would fetch user details from the database
        # For now, we'll return the provided information
        return {
            "success": True,
            "email": email or "unknown@example.com",  # Placeholder - in reality this would come from auth
            "user_id": user_id,
            "message": f"Current user information retrieved for user ID: {user_id}"
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to get user information: {str(e)}",
            "email": None,
            "user_id": None
        }


__all__ = ["add_task", "delete_task", "update_task", "complete_task", "list_tasks", "get_current_user"]