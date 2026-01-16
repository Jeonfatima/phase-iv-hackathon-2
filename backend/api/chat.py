from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Optional, Dict, Any
from pydantic import BaseModel
import logging

from auth.jwt_handler import JWTBearer
from services.chat_service import ChatService
from database.conversation_crud import get_conversation_by_id
from auth.conversation_access import verify_user_id_match


class ChatRequest(BaseModel):
    message: str = ""
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    message_id: int
    tool_calls: Optional[list] = None


router = APIRouter(prefix="/api/{user_id}", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    user_id: str,
    chat_request: ChatRequest,
    request: Request,
    token_data: dict = Depends(JWTBearer())
):
    """
    Main chat endpoint that processes natural language input and returns AI-generated responses
    """
    # Debug logging
    import logging
    logging.info(f"Chat endpoint called with user_id: {user_id}")
    logging.info(f"Chat request: {chat_request}")
    logging.info(f"Token data: {token_data}")

    # Validate that user_id is provided
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID is required"
        )

    # Verify that the user_id in the URL matches the user_id in the token
    verify_user_id_match(request, user_id)

    # Validate the message content
    validation_result = ChatService.validate_and_sanitize_message(chat_request.message)

    if not validation_result["valid"]:
        # Handle all validation issues gracefully instead of throwing 400
        # This includes empty messages, length issues, etc.
        sanitized_message = validation_result["sanitized_content"]

        # If message is still empty after validation, provide a default
        if not sanitized_message or not sanitized_message.strip():
            sanitized_message = "Hello"  # Default message to prevent empty content
    else:
        # Sanitize the message content
        sanitized_message = validation_result["sanitized_content"]

    # Process the user message through the chat service
    # For simple greetings, provide immediate response without AI
    lower_message = sanitized_message.lower().strip()
    if lower_message in ["hi", "hello", "hey", "hi!", "hello!", "hey!", "greetings", "good morning", "good afternoon", "good evening"]:
        # Return a simple greeting without processing through AI
        import random
        greetings = [
            "Hello! I'm your AI Todo Assistant. How can I help you today?",
            "Hi there! I'm here to help you manage your tasks. What would you like to do?",
            "Hey! I'm your personal AI assistant. Feel free to ask me to add, list, or manage your tasks!"
        ]
        response_text = random.choice(greetings)

        return ChatResponse(
            conversation_id=chat_request.conversation_id or -1,
            response=response_text,
            message_id=-1,
            tool_calls=[]
        )
    elif lower_message in ["who am i", "who are you", "what is this", "help", "what can you do"]:
        help_text = "I'm your AI Todo Assistant! I can help you:\n• Add tasks: 'Add a task to buy groceries'\n• List tasks: 'Show my tasks'\n• Delete tasks: 'Delete task 1'\n• Complete tasks: 'Mark task 2 as complete'\n• Update tasks: 'Change task 1 title to new title'"

        return ChatResponse(
            conversation_id=chat_request.conversation_id or -1,
            response=help_text,
            message_id=-1,
            tool_calls=[]
        )
    else:
        result = ChatService.process_user_message(
            user_id=user_id,
            user_message=sanitized_message,
            conversation_id=chat_request.conversation_id
        )

        if not result["success"]:
            # Log the error for debugging purposes
            error_detail = result.get("message", "Failed to process message")
            logging.error(f"Chat processing failed: {error_detail}")

            # Return a friendly fallback message instead of an error
            # This allows the UI to show a helpful message to the user
            return ChatResponse(
                conversation_id=chat_request.conversation_id or -1,
                response="Hi! Sorry, I cannot connect to my AI service for the moment. I can help you manage your tasks when I'm back online!",
                message_id=-1,
                tool_calls=[]
            )

    return ChatResponse(
        conversation_id=result["conversation_id"],
        response=result["response"],
        message_id=result["message_id"],
        tool_calls=result.get("tool_calls", [])
    )


# Additional endpoints for conversation management

@router.get("/conversations")
def get_user_conversations(
    user_id: str,
    request: Request,
    token_data: dict = Depends(JWTBearer())
):
    """
    Get all conversations for the specified user
    """
    # Verify that the user_id in the URL matches the user_id in the token
    verify_user_id_match(request, user_id)

    conversations = ChatService.get_user_conversations(user_id)
    return {"conversations": conversations, "total_count": len(conversations)}


@router.get("/conversations/{conversation_id}/messages")
def get_conversation_messages(
    user_id: str,
    conversation_id: int,
    request: Request,
    limit: int = 50,
    offset: int = 0,
    token_data: dict = Depends(JWTBearer())
):
    """
    Get all messages in a specific conversation
    """
    # Verify that the user_id in the URL matches the user_id in the token
    verify_user_id_match(request, user_id)

    # Verify conversation access
    from database.session import get_session_context
    with get_session_context() as session:
        from database.conversation_crud import get_conversation_by_id
        conversation = get_conversation_by_id(session, conversation_id)

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        if str(conversation.user_id) != str(user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only access your own conversations"
            )

    messages = ChatService.get_conversation_history(conversation_id, limit, offset)
    return {
        "messages": messages,
        "conversation_id": conversation_id
    }