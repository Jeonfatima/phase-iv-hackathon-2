from typing import List, Optional
from sqlmodel import Session, select
from models.task import Task, TaskBase, TaskCreate, TaskUpdate
from models.user import User
from datetime import datetime, timezone


class TaskService:
    @staticmethod
    def create_task(session: Session, user_id: int, task_data: TaskCreate) -> Task:
        """
        Create a new task for the specified user
        """
        task = Task(
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
            user_id=user_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_all_tasks(session: Session, user_id: int) -> List[Task]:
        """
        Get all tasks for the specified user
        """
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
        return tasks

    @staticmethod
    def get_task_by_id(session: Session, user_id: int, task_id: int) -> Optional[Task]:
        """
        Get a specific task by ID for the specified user
        """
        statement = select(Task).where(Task.user_id == user_id, Task.id == task_id)
        task = session.exec(statement).first()
        return task

    @staticmethod
    def update_task(session: Session, user_id: int, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """
        Update a specific task by ID for the specified user
        """
        task = TaskService.get_task_by_id(session, user_id, task_id)
        if task:
            # Update only fields provided in task_data
            for field, value in task_data.model_dump(exclude_unset=True).items():
                if value is not None:
                    setattr(task, field, value)
            task.updated_at = datetime.now(timezone.utc)  # update timestamp
            session.add(task)
            session.commit()
            session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, user_id: int, task_id: int) -> bool:
        """
        Delete a specific task by ID for the specified user
        """
        task = TaskService.get_task_by_id(session, user_id, task_id)
        if task:
            session.delete(task)
            session.commit()
            return True
        return False

    @staticmethod
    def update_task_completion(session: Session, user_id: int, task_id: int, completed: bool) -> Optional[Task]:
        """
        Update the completion status of a specific task by ID for the specified user
        """
        task = TaskService.get_task_by_id(session, user_id, task_id)
        if task:
            task.completed = completed
            task.updated_at = datetime.now(timezone.utc)
            session.add(task)
            session.commit()
            session.refresh(task)
        return task
