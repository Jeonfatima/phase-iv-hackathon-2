from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int  # Foreign key to user
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None)


__all__ = ["Task", "TaskBase", "TaskCreate", "TaskUpdate"]