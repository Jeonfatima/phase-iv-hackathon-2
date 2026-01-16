# This module provides CRUD operations for conversation and message entities
# It re-exports the functionality from conversation_db_service

from .conversation_db_service import ConversationDBService, MessageDBService

# Aliases to match expected naming
create_conversation = ConversationDBService.create_conversation
get_conversation_by_id = ConversationDBService.get_conversation_by_id
get_conversations_for_user = ConversationDBService.get_conversations_for_user
update_conversation_timestamp = ConversationDBService.update_conversation_timestamp

create_message = MessageDBService.create_message
get_messages_for_conversation = MessageDBService.get_messages_for_conversation
get_latest_messages = MessageDBService.get_latest_messages

__all__ = [
    "create_conversation",
    "get_conversation_by_id",
    "get_conversations_for_user",
    "update_conversation_timestamp",
    "create_message",
    "get_messages_for_conversation",
    "get_latest_messages"
]