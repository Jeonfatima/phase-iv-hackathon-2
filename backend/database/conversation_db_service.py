from datetime import datetime
from sqlmodel import Session, select, and_
from typing import List, Optional
from models.conversation import Conversation, Message


class ConversationDBService:
    """Database service for conversation-related operations"""

    @staticmethod
    def create_conversation(session: Session, user_id: str) -> Conversation:
        """Create a new conversation for a user"""
        from datetime import datetime
        conversation = Conversation(
            user_id=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(conversation)
        session.flush()  # Ensure ID is generated without committing
        session.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation_by_id(session: Session, conversation_id: int) -> Optional[Conversation]:
        """Get a conversation by its ID"""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return session.exec(statement).first()

    @staticmethod
    def get_conversations_for_user(session: Session, user_id: str) -> List[Conversation]:
        """Get all conversations for a specific user"""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return session.exec(statement).all()

    @staticmethod
    def update_conversation_timestamp(session: Session, conversation_id: int) -> bool:
        """Update the updated_at timestamp for a conversation"""
        conversation = ConversationDBService.get_conversation_by_id(session, conversation_id)
        if conversation:
            # Update the timestamp using SQLAlchemy core to avoid Pydantic validation issues
            from sqlalchemy import update
            stmt = update(Conversation).where(Conversation.id == conversation_id).values(updated_at=datetime.now())
            session.exec(stmt)
            return True
        return False


class MessageDBService:
    """Database service for message-related operations"""

    @staticmethod
    def create_message(
        session: Session,
        conversation_id: int,
        role: str,
        content: str
    ) -> Message:
        """Create a new message in a conversation"""
        from datetime import datetime
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            timestamp=datetime.now()
        )
        session.add(message)
        session.flush()  # Ensure ID is generated without committing
        session.refresh(message)
        return message

    @staticmethod
    def get_messages_for_conversation(
        session: Session,
        conversation_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[Message]:
        """Get messages for a specific conversation with pagination"""
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp).offset(offset).limit(limit)
        return session.exec(statement).all()

    @staticmethod
    def get_latest_messages(
        session: Session,
        conversation_id: int,
        limit: int = 20
    ) -> List[Message]:
        """Get the latest messages for context in AI reasoning"""
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp.desc()).limit(limit)
        messages = session.exec(statement).all()
        # Return in chronological order
        return list(reversed(messages))