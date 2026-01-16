# Data Model: AI Todo Chatbot Integration

## Entity Definitions

### Conversation Entity
**Purpose**: Stores conversation metadata linking user to their chat sessions

**Fields**:
- `id`: Integer (Primary Key, Auto-increment)
- `user_id`: String (Foreign Key to authenticated user, indexed)
- `created_at`: DateTime (Timestamp when conversation started, indexed)
- `updated_at`: DateTime (Timestamp of last activity, indexed)

**Relationships**:
- One-to-Many: Conversation → Messages (via conversation_id foreign key)
- ManyToOne: Conversation ← User (via user_id foreign key)

**Validation Rules**:
- user_id must exist in authentication system
- created_at defaults to current timestamp
- updated_at updates on any conversation activity

**State Transitions**:
- Created: When new conversation starts
- Active: When messages are exchanged
- Dormant: After period of inactivity (for cleanup purposes)

### Message Entity
**Purpose**: Stores individual message exchanges within conversations

**Fields**:
- `id`: Integer (Primary Key, Auto-increment)
- `conversation_id`: Integer (Foreign Key to Conversation, indexed)
- `role`: String (Enum: "user", "assistant", "tool", required)
- `content`: Text (Message content, max 10000 characters)
- `timestamp`: DateTime (When message was created, indexed)

**Relationships**:
- ManyToOne: Message ← Conversation (via conversation_id foreign key)
- One-to-Many: Message → Tool Results (via message_id foreign key, optional)

**Validation Rules**:
- conversation_id must exist
- role must be one of allowed values
- content length limited to prevent abuse
- timestamp defaults to current time

### Task Entity (Extended)
**Purpose**: Existing task entity extended with AI interaction metadata

**Additional Fields**:
- `last_interaction_id`: Integer (Foreign Key to Message, optional)
- `ai_generated`: Boolean (Flag for tasks created via AI)

**Relationships**:
- ManyToOne: Task ← Message (via last_interaction_id, optional)

## Database Schema

### SQLModel Definitions

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Links to authenticated user
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    role: str = Field(sa_column_kwargs={"check": "role IN ('user', 'assistant', 'tool')"})
    content: str = Field(max_length=10000)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")
```

## Indexing Strategy

### Primary Indexes
- Conversation.id: Primary key index (auto-created)
- Message.id: Primary key index (auto-created)

### Secondary Indexes
- Conversation.user_id: Enables fast user-specific queries
- Conversation.created_at: Optimizes chronological sorting
- Conversation.updated_at: Facilitates conversation lifecycle management
- Message.conversation_id: Enables fast conversation-message joins
- Message.timestamp: Optimizes chronological message retrieval
- Message.role: Improves role-based filtering performance

### Composite Indexes
- (user_id, created_at): Optimal for user's conversation history retrieval
- (conversation_id, timestamp): Optimal for conversation message history

## Constraints and Validation

### Database Constraints
- NOT NULL constraints on required fields
- Check constraints on enum fields (role values)
- Foreign key constraints for referential integrity
- Length constraints on text fields to prevent abuse

### Business Logic Constraints
- User isolation: All queries must filter by user_id
- Conversation ownership: Users can only access their own conversations
- Message ordering: Messages retrieved in chronological order by timestamp

## Migration Strategy

### Phase 1: Schema Creation
1. Create Conversation table with basic structure
2. Create Message table with basic structure
3. Establish foreign key relationships
4. Apply indexes for performance

### Phase 2: Data Population
1. Existing conversations (if applicable) can be created retroactively
2. New conversations created automatically with first message
3. Historical data migration (if needed) in batches

### Phase 3: Validation
1. Verify foreign key constraints
2. Test user isolation mechanisms
3. Validate performance with indexes
4. Confirm data integrity

## Performance Considerations

### Query Optimization
- Use LIMIT clauses for message history retrieval
- Implement pagination for long conversations
- Cache frequently accessed conversation metadata
- Batch operations for bulk message insertion

### Storage Efficiency
- Compress message content when possible
- Archive old conversations to separate tables
- Implement TTL (Time To Live) for cleanup
- Regular maintenance for index optimization

## Security Measures

### Access Control
- Row-level security via user_id filtering
- Parameterized queries to prevent injection
- Input validation for all user-provided content
- Rate limiting to prevent abuse

### Data Protection
- Encrypt sensitive fields if necessary
- Log access attempts for audit trail
- Sanitize content before display
- Implement retention policies

## API Integration Points

### Conversation Management
- GET /api/users/{user_id}/conversations: List user's conversations
- POST /api/users/{user_id}/conversations: Start new conversation
- GET /api/conversations/{conversation_id}: Retrieve conversation with messages

### Message Operations
- POST /api/conversations/{conversation_id}/messages: Add message
- GET /api/conversations/{conversation_id}/messages: List conversation messages
- DELETE /api/messages/{message_id}: Remove message (admin only)

## Backup and Recovery

### Backup Strategy
- Daily backups of conversation and message data
- Point-in-time recovery for transactional consistency
- Off-site storage for disaster recovery

### Recovery Procedures
- Automated restore procedures for database failure
- Validation of restored data integrity
- Notification system for backup failures