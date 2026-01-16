from typing import Dict, Any, List, Optional
from database.conversation_crud import (
    create_conversation, get_conversation_by_id, get_conversations_for_user,
    create_message, get_messages_for_conversation, get_latest_messages
)
from database.session import get_session_context
from models.conversation import RoleType
from .ai_service import AIService


class ChatService:
    """
    Service class for handling chat operations including conversation management
    and message history
    """

    @staticmethod
    def create_new_conversation(user_id: str) -> Dict[str, Any]:
        """
        Create a new conversation for a user

        Args:
            user_id: The ID of the user creating the conversation

        Returns:
            Dictionary with conversation details
        """
        with get_session_context() as session:
            conversation = create_conversation(session, user_id)
            # Prepare and return the data within the session context to avoid DetachedInstanceError
            return {
                "id": conversation.id,
                "user_id": conversation.user_id,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat()
            }

    @staticmethod
    def get_conversation(conversation_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a conversation by its ID

        Args:
            conversation_id: The ID of the conversation to retrieve

        Returns:
            Dictionary with conversation details or None if not found
        """
        with get_session_context() as session:
            conversation = get_conversation_by_id(session, conversation_id)

            if conversation:
                return {
                    "id": conversation.id,
                    "user_id": conversation.user_id,
                    "created_at": conversation.created_at.isoformat(),
                    "updated_at": conversation.updated_at.isoformat()
                }
            return None

    @staticmethod
    def get_user_conversations(user_id: str) -> List[Dict[str, Any]]:
        """
        Get all conversations for a specific user

        Args:
            user_id: The ID of the user

        Returns:
            List of conversation dictionaries
        """
        with get_session_context() as session:
            conversations = get_conversations_for_user(session, user_id)

            result = []
            for conv in conversations:
                result.append({
                    "id": conv.id,
                    "user_id": conv.user_id,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat()
                })
            return result

    @staticmethod
    def save_user_message(conversation_id: int, content: str) -> Dict[str, Any]:
        """
        Save a user message to the conversation

        Args:
            conversation_id: The ID of the conversation
            content: The message content

        Returns:
            Dictionary with message details
        """
        with get_session_context() as session:
            message = create_message(session, conversation_id, RoleType.user, content)

            return {
                "id": message.id,
                "conversation_id": message.conversation_id,
                "role": message.role.value,
                "content": message.content,
                "timestamp": message.timestamp.isoformat()
            }

    @staticmethod
    def save_assistant_message(conversation_id: int, content: str) -> Dict[str, Any]:
        """
        Save an assistant message to the conversation

        Args:
            conversation_id: The ID of the conversation
            content: The message content

        Returns:
            Dictionary with message details
        """
        with get_session_context() as session:
            message = create_message(session, conversation_id, RoleType.assistant, content)

            return {
                "id": message.id,
                "conversation_id": message.conversation_id,
                "role": message.role.value,
                "content": message.content,
                "timestamp": message.timestamp.isoformat()
            }

    @staticmethod
    def save_tool_message(conversation_id: int, content: str) -> Dict[str, Any]:
        """
        Save a tool message to the conversation

        Args:
            conversation_id: The ID of the conversation
            content: The message content

        Returns:
            Dictionary with message details
        """
        with get_session_context() as session:
            message = create_message(session, conversation_id, RoleType.tool, content)

            return {
                "id": message.id,
                "conversation_id": message.conversation_id,
                "role": message.role.value,
                "content": message.content,
                "timestamp": message.timestamp.isoformat()
            }

    @staticmethod
    def get_conversation_history(conversation_id: int, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get conversation history with proper ordering

        Args:
            conversation_id: The ID of the conversation
            limit: Maximum number of messages to return
            offset: Number of messages to skip

        Returns:
            List of message dictionaries in chronological order
        """
        with get_session_context() as session:
            messages = get_messages_for_conversation(session, conversation_id, limit, offset)

            result = []
            for msg in messages:
                result.append({
                    "id": msg.id,
                    "conversation_id": msg.conversation_id,
                    "role": msg.role.value,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                })
            return result

    @staticmethod
    def get_recent_context(conversation_id: int, limit: int = 20) -> List[Dict[str, str]]:
        """
        Get recent messages for AI context in reasoning

        Args:
            conversation_id: The ID of the conversation
            limit: Maximum number of recent messages to return

        Returns:
            List of message dictionaries in the format expected by AI service
        """
        with get_session_context() as session:
            messages = get_latest_messages(session, conversation_id, limit)

            result = []
            for msg in messages:
                result.append({
                    "role": msg.role.value,
                    "content": msg.content
                })
            return result

    @staticmethod
    def process_user_message(
        user_id: str,
        user_message: str,
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Process a user message through the AI service and save the conversation

        Args:
            user_id: The ID of the user
            user_message: The message from the user
            conversation_id: Optional existing conversation ID, creates new if None

        Returns:
            Dictionary with response and conversation details
        """
        # Create or get conversation
        if conversation_id is None:
            conversation = ChatService.create_new_conversation(user_id)
            conversation_id = conversation["id"]
        else:
            conversation = ChatService.get_conversation(conversation_id)
            if not conversation:
                return {
                    "success": False,
                    "message": f"Conversation with ID {conversation_id} not found"
                }

        # Save user message
        user_msg = ChatService.save_user_message(conversation_id, user_message)

        # Get conversation history for context
        conversation_history = ChatService.get_recent_context(conversation_id, limit=20)

        # Process with AI service
        ai_result = AIService.process_conversation_with_reasoning_loop(
            user_message=user_message,
            user_id=user_id,
            conversation_history=conversation_history
        )

        if not ai_result["success"]:
            return ai_result

        # Save assistant response
        assistant_msg = ChatService.save_assistant_message(
            conversation_id,
            ai_result["response"]
        )

        return {
            "success": True,
            "conversation_id": conversation_id,
            "response": ai_result["response"],
            "tool_calls": ai_result["tool_calls"],
            "message_id": assistant_msg["id"]
        }

    @staticmethod
    def validate_and_sanitize_message(content: str) -> Dict[str, Any]:
        """
        Validate and sanitize user message content

        Args:
            content: The raw message content

        Returns:
            Dictionary with validation result and sanitized content
        """
        if not content or not content.strip():
            return {
                "valid": False,
                "sanitized_content": "",
                "message": "Message content cannot be empty"
            }

        # Basic sanitization - remove excessive whitespace
        sanitized_content = content.strip()

        # Check length limits
        if len(sanitized_content) > 1000:
            return {
                "valid": False,
                "sanitized_content": sanitized_content[:1000],
                "message": "Message too long, limited to 1000 characters"
            }

        return {
            "valid": True,
            "sanitized_content": sanitized_content,
            "message": "Message is valid"
        }


__all__ = ["ChatService"]