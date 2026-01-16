#!/usr/bin/env python3
"""
Test script to verify that all DetachedInstanceError fixes are working correctly
in the chat service.
"""

import sys
import os
import tempfile
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from sqlmodel import SQLModel, create_engine
from database.session import get_session_context
from database.engine import engine
from models.conversation import Conversation, Message
from database.conversation_db_service import ConversationDBService, MessageDBService
from services.chat_service import ChatService
from models.conversation import RoleType


def test_create_new_conversation():
    """Test Case 1: Create a new conversation"""
    print("Test Case 1: Creating new conversation...")

    try:
        # Create conversation
        user_id = "test_user_123"
        conversation_data = ChatService.create_new_conversation(user_id)

        # Verify the data is returned correctly
        assert "id" in conversation_data, "Conversation ID should be in returned data"
        assert "user_id" in conversation_data, "User ID should be in returned data"
        assert "created_at" in conversation_data, "Created at should be in returned data"
        assert "updated_at" in conversation_data, "Updated at should be in returned data"

        print(f"  OK Created conversation with ID: {conversation_data['id']}")
        print(f"  OK User ID: {conversation_data['user_id']}")
        print(f"  OK Created at: {conversation_data['created_at']}")
        print(f"  OK Updated at: {conversation_data['updated_at']}")

        # Verify we can access the id without DetachedInstanceError
        conversation_id = conversation_data["id"]
        print(f"  OK Successfully accessed conversation.id: {conversation_id}")

        return True, conversation_data

    except Exception as e:
        print(f"  ERROR Error in create_new_conversation: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_add_message_to_conversation(conversation_data):
    """Test Case 2: Add a message to an existing conversation"""
    print("\nTest Case 2: Adding message to conversation...")

    try:
        if not conversation_data:
            print("  ❌ Cannot test - no conversation data available")
            return False

        conversation_id = conversation_data["id"]

        # Test saving a user message
        user_message_data = ChatService.save_user_message(conversation_id, "Hello, this is a test message")

        assert "id" in user_message_data, "Message ID should be in returned data"
        assert "conversation_id" in user_message_data, "Conversation ID should be in returned data"
        assert user_message_data["role"] == "user", "Role should be 'user'"
        assert user_message_data["content"] == "Hello, this is a test message", "Content should match"

        print(f"  OK Saved user message with ID: {user_message_data['id']}")
        print(f"  OK Conversation ID: {user_message_data['conversation_id']}")
        print(f"  OK Role: {user_message_data['role']}")
        print(f"  OK Content: {user_message_data['content']}")

        # Test saving an assistant message
        assistant_message_data = ChatService.save_assistant_message(conversation_id, "Hello! I received your message.")

        assert "id" in assistant_message_data, "Assistant message ID should be in returned data"
        assert assistant_message_data["role"] == "assistant", "Role should be 'assistant'"
        assert assistant_message_data["content"] == "Hello! I received your message.", "Content should match"

        print(f"  OK Saved assistant message with ID: {assistant_message_data['id']}")
        print(f"  OK Role: {assistant_message_data['role']}")
        print(f"  OK Content: {assistant_message_data['content']}")

        return True

    except Exception as e:
        print(f"  ERROR Error in add_message_to_conversation: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_conversation_history(conversation_data):
    """Test Case 3: Get conversation history and recent context"""
    print("\nTest Case 3: Getting conversation history and context...")

    try:
        if not conversation_data:
            print("  ❌ Cannot test - no conversation data available")
            return False

        conversation_id = conversation_data["id"]

        # Get conversation history
        history = ChatService.get_conversation_history(conversation_id)

        print(f"  OK Retrieved {len(history)} messages from history")

        for i, msg in enumerate(history):
            assert "id" in msg, f"Message {i} should have ID"
            assert "conversation_id" in msg, f"Message {i} should have conversation_id"
            assert "role" in msg, f"Message {i} should have role"
            assert "content" in msg, f"Message {i} should have content"
            assert "timestamp" in msg, f"Message {i} should have timestamp"

            print(f"    Message {i+1}: ID={msg['id']}, Role={msg['role']}, Content='{msg['content'][:30]}...'")

        # Get recent context (for AI reasoning)
        recent_context = ChatService.get_recent_context(conversation_id)

        print(f"  OK Retrieved {len(recent_context)} messages for AI context")

        for i, ctx in enumerate(recent_context):
            assert "role" in ctx, f"Context {i} should have role"
            assert "content" in ctx, f"Context {i} should have content"

            print(f"    Context {i+1}: Role={ctx['role']}, Content='{ctx['content'][:30]}...'")

        return True

    except Exception as e:
        print(f"  ERROR Error in get_conversation_history: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_conversation(conversation_data):
    """Test getting conversation by ID"""
    print("\nAdditional Test: Getting conversation by ID...")

    try:
        if not conversation_data:
            print("  ❌ Cannot test - no conversation data available")
            return False

        original_conversation_id = conversation_data["id"]

        # Get conversation by ID
        retrieved_conversation = ChatService.get_conversation(original_conversation_id)

        assert retrieved_conversation is not None, "Conversation should be found"
        assert retrieved_conversation["id"] == original_conversation_id, "IDs should match"

        print(f"  OK Retrieved conversation: ID={retrieved_conversation['id']}")
        print(f"  OK User ID: {retrieved_conversation['user_id']}")
        print(f"  OK Created at: {retrieved_conversation['created_at']}")
        print(f"  OK Updated at: {retrieved_conversation['updated_at']}")

        return True

    except Exception as e:
        print(f"  ERROR Error in get_conversation: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multiple_requests_same_conversation(conversation_data):
    """Test Case 4: Multiple requests in the same conversation"""
    print("\nTest Case 4: Multiple requests in same conversation...")

    try:
        if not conversation_data:
            print("  ❌ Cannot test - no conversation data available")
            return False

        conversation_id = conversation_data["id"]

        # Add multiple messages to simulate conversation flow
        for i in range(3):
            # User message
            user_msg = ChatService.save_user_message(conversation_id, f"User message {i+1}")
            print(f"  OK Added user message {i+1}: ID={user_msg['id']}")

            # Assistant response
            assistant_msg = ChatService.save_assistant_message(conversation_id, f"Assistant response {i+1}")
            print(f"  OK Added assistant response {i+1}: ID={assistant_msg['id']}")

        # Verify we can still get the full history
        history = ChatService.get_conversation_history(conversation_id)
        print(f"  OK Final history has {len(history)} messages")

        # Verify conversation still accessible
        conv = ChatService.get_conversation(conversation_id)
        assert conv is not None, "Conversation should still be accessible"
        print(f"  OK Conversation still accessible: ID={conv['id']}")

        return True

    except Exception as e:
        print(f"  ERROR Error in multiple_requests_same_conversation: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_comprehensive_verification():
    """Run all verification tests"""
    print("Running Comprehensive DetachedInstanceError Fix Verification")
    print("=" * 60)

    results = []

    # Test Case 1: Create new conversation
    success1, conversation_data = test_create_new_conversation()
    results.append(("Create new conversation", success1))

    # Test Case 2: Add messages
    if success1:
        success2 = test_add_message_to_conversation(conversation_data)
        results.append(("Add messages to conversation", success2))
    else:
        results.append(("Add messages to conversation", False))
        success2 = False

    # Test Case 3: Get history and context
    if success1:
        success3 = test_get_conversation_history(conversation_data)
        results.append(("Get conversation history and context", success3))
    else:
        results.append(("Get conversation history and context", False))
        success3 = False

    # Additional test: Get conversation by ID
    if success1:
        success4 = test_get_conversation(conversation_data)
        results.append(("Get conversation by ID", success4))
    else:
        results.append(("Get conversation by ID", False))
        success4 = False

    # Test Case 4: Multiple requests
    if success1:
        success5 = test_multiple_requests_same_conversation(conversation_data)
        results.append(("Multiple requests in same conversation", success5))
    else:
        results.append(("Multiple requests in same conversation", False))
        success5 = False

    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION RESULTS SUMMARY")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{status:4} {test_name}")
        if success:
            passed += 1

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("\nALL TESTS PASSED! DetachedInstanceError fixes are working correctly.")
        print("OK Conversations can be created and accessed safely")
        print("OK Messages can be saved and retrieved without detachment issues")
        print("OK History and context retrieval works properly")
        print("OK Multiple requests in same conversation work correctly")
        return True
    else:
        print(f"\nERROR {total - passed} tests failed. Some DetachedInstanceError issues remain.")
        return False


if __name__ == "__main__":
    success = run_comprehensive_verification()
    sys.exit(0 if success else 1)