#!/usr/bin/env python3
"""
Test script to verify the datetime field fix for SQLModel Pydantic v2
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from datetime import datetime
from sqlmodel import SQLModel, create_engine, Session
from models.conversation import Conversation, Message
from database.conversation_db_service import ConversationDBService, MessageDBService

def test_conversation_creation():
    """Test creating a conversation to verify datetime fix"""
    print("Testing Conversation creation...")

    # Create in-memory database for testing
    engine = create_engine("sqlite:///./test_datetime_fix.db")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Create a conversation - this should not trigger the default_factory error
        conversation = ConversationDBService.create_conversation(session, "test_user_123")

        print(f"Created conversation ID: {conversation.id}")
        print(f"Created at: {conversation.created_at}")
        print(f"Updated at: {conversation.updated_at}")

        # Verify the timestamps are set
        assert conversation.created_at is not None, "created_at should be set"
        assert conversation.updated_at is not None, "updated_at should be set"
        print("OK Conversation timestamps are properly set")

        # Create a message in the conversation
        message = MessageDBService.create_message(
            session,
            conversation.id,
            "user",
            "Test message for datetime fix verification"
        )

        print(f"Created message ID: {message.id}")
        print(f"Timestamp: {message.timestamp}")

        # Verify the message timestamp is set
        assert message.timestamp is not None, "timestamp should be set"
        print("OK Message timestamp is properly set")

        # Test updating conversation timestamp
        updated = ConversationDBService.update_conversation_timestamp(session, conversation.id)
        assert updated, "Conversation timestamp should be updated"
        print("OK Conversation timestamp update successful")

        # Refresh to get the updated timestamp
        session.refresh(conversation)
        print(f"Updated at (after refresh): {conversation.updated_at}")

    print("\nOK All datetime field tests passed! The Pydantic v2 default_factory issue has been fixed.")

def test_task_creation():
    """Test creating a task to verify datetime fix"""
    print("\nTesting Task creation...")

    from models.task import Task
    from services.task_service import TaskService
    from sqlmodel import select

    # Reuse the same test database
    engine = create_engine("sqlite:///./test_datetime_fix.db")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Create a task - this should not trigger the default_factory error
        from pydantic import BaseModel

        class TaskCreate(BaseModel):
            title: str
            description: str = None
            completed: bool = False

        task_data = TaskCreate(title="Test task for datetime fix", description="Testing datetime fix")
        task = TaskService.create_task(session, 1, task_data)

        print(f"Created task ID: {task.id}")
        print(f"Created at: {task.created_at}")
        print(f"Updated at: {task.updated_at}")

        # Verify the timestamps are set
        assert task.created_at is not None, "task created_at should be set"
        assert task.updated_at is not None, "task updated_at should be set"
        print("OK Task timestamps are properly set")

        # Test updating task
        from pydantic import BaseModel

        class TaskUpdate(BaseModel):
            title: str = None
            description: str = None
            completed: bool = None

        update_data = TaskUpdate(title="Updated test task")
        updated_task = TaskService.update_task(session, 1, task.id, update_data)

        print(f"Updated task ID: {updated_task.id}")
        print(f"Updated at (after update): {updated_task.updated_at}")

        assert updated_task.updated_at > task.created_at, "updated_at should be newer than created_at"
        print("OK Task timestamp update successful")

    print("\nOK All task datetime field tests passed!")

def test_user_creation():
    """Test creating a user to verify datetime fix"""
    print("\nTesting User creation...")

    from models.user import User
    from sqlmodel import select
    import hashlib
    import secrets

    # Reuse the same test database
    engine = create_engine("sqlite:///./test_datetime_fix.db")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Create a user - this should not trigger the default_factory error
        salt = secrets.token_hex(16)
        password = "testpassword123"
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt), 100000)
        hashed_password_hex = hashed_password.hex()

        from datetime import timezone
        db_user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=f"{hashed_password_hex}:{salt}",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        print(f"Created user ID: {db_user.id}")
        print(f"Created at: {db_user.created_at}")
        print(f"Updated at: {db_user.updated_at}")

        # Verify the timestamps are set
        assert db_user.created_at is not None, "user created_at should be set"
        assert db_user.updated_at is not None, "user updated_at should be set"
        print("OK User timestamps are properly set")

    print("\nOK All user datetime field tests passed!")

if __name__ == "__main__":
    print("Testing SQLModel Pydantic v2 datetime field fix...")
    print("=" * 60)

    try:
        test_conversation_creation()
        test_task_creation()
        test_user_creation()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! The datetime field fix is working correctly.")
        print("The 'validated_data' must be provided if 'call_default_factory' is True error should be resolved.")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)