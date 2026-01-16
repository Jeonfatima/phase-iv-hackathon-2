from fastapi import HTTPException, status, Request
from typing import Dict
from models.conversation import Conversation
from database.conversation_crud import get_conversation_by_id
from sqlmodel import Session
from database.session import get_session


def verify_conversation_access(
    request: Request,
    conversation_id: int,
    db_session: Session
) -> Conversation:
    """
    Verify that the current user has access to the specified conversation
    """
    # Get the current user from the request state
    if not hasattr(request.state, 'user'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )

    token_data = request.state.user
    token_user_id_str = token_data.get("userId") or token_data.get("sub")
    if not token_user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID"
        )

    # Get the conversation
    conversation = get_conversation_by_id(db_session, conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    # Verify that the user owns this conversation
    if str(conversation.user_id) != str(token_user_id_str):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own conversations"
        )

    return conversation


def verify_user_id_match(
    request: Request,
    url_user_id: str
) -> bool:
    """
    Verify that the user_id in the URL matches the user_id in the JWT token
    """
    # Get the current user from the request state
    if not hasattr(request.state, 'user'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )

    token_data = request.state.user
    token_user_id_str = token_data.get("userId") or token_data.get("sub")
    if not token_user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID"
        )

    # Compare user IDs
    if str(token_user_id_str) != str(url_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources"
        )

    return True