from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    username: Optional[str] = Field(default=None, unique=True, nullable=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None)

__all__ = ["User", "UserBase"]