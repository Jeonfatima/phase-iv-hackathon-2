from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from enum import Enum


class RoleType(str, Enum):
    user = "user"
    assistant = "assistant"
    tool = "tool"


class ConversationBase(SQLModel):
    user_id: str  # Links to authenticated user


class Conversation(ConversationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Links to authenticated user
    created_at: datetime = Field(default=None, index=True)
    updated_at: datetime = Field(default=None, index=True)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")


class MessageBase(SQLModel):
    conversation_id: int
    role: RoleType
    content: str


class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    role: RoleType
    content: str = Field(max_length=10000)
    timestamp: datetime = Field(default=None, index=True)

    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")


__all__ = ["Conversation", "Message", "RoleType"]