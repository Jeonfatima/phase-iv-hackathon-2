#!/usr/bin/env python3
"""
Direct test to isolate the conversation endpoint issue
"""

import os
from dotenv import load_dotenv
from core.config import Settings

# Load environment variables
load_dotenv()

# Create fresh settings instance
settings = Settings()

# Test database session and conversation retrieval directly
def test_conversation_db():
    print("Testing database connection and conversation retrieval...")

    try:
        # Import after settings are loaded
        from database.session import get_session
        from database.conversation_crud import get_conversations_for_user

        print("Imports successful")

        # Test creating a session and retrieving conversations
        from database.session import get_session_context
        with get_session_context() as session:
            print("Session created successfully")

            # Try to get conversations for a test user
            user_id = "1"
            conversations = get_conversations_for_user(session, user_id)
            print(f"Successfully retrieved {len(conversations)} conversations")

            return True

    except Exception as e:
        print(f"Error in database test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chat_service():
    print("\nTesting ChatService...")

    try:
        from services.chat_service import ChatService

        # Test the get_user_conversations method directly
        user_id = "1"
        conversations = ChatService.get_user_conversations(user_id)
        print(f"ChatService.get_user_conversations returned: {conversations}")

        return True

    except Exception as e:
        print(f"Error in ChatService test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Direct test of conversation functionality...")

    db_success = test_conversation_db()
    service_success = test_chat_service()

    print(f"\nResults:")
    print(f"Database test: {'PASS' if db_success else 'FAIL'}")
    print(f"Chat service test: {'PASS' if service_success else 'FAIL'}")