# Research Findings: AI Todo Chatbot Integration

## Cohere API Integration Research

### Decision: Cohere Model Selection
**Chosen**: `command-r-plus`
**Rationale**: Superior reasoning and tool-use accuracy compared to command-r, essential for reliable task operation interpretation and execution.

**Alternatives considered**:
- command-r: Lower cost but reduced reasoning capability
- command: Basic model without advanced reasoning features

### Decision: Tool Call Parsing Strategy
**Chosen**: Strict JSON block extraction with validation
**Rationale**: Require Cohere to output valid JSON in structured format for reliable parsing and execution. Fallback mechanisms can cause inconsistent behavior.

**Alternatives considered**:
- Regex-based extraction: Less reliable, prone to false positives
- Natural language parsing: Too error-prone for production use

### Decision: Multi-Step Chaining Approach
**Chosen**: Loop until no tool call detected
**Rationale**: Execute tools iteratively, feeding results back to Cohere until final response is achieved. This handles complex queries like "List pending then delete the first" reliably.

**Alternatives considered**:
- Single Cohere call: Limited to simple operations
- Pre-defined maximum iterations: Less flexible for complex reasoning

### Decision: Conversation Persistence Strategy
**Chosen**: Optional conversation_id with new creation if not provided
**Rationale**: Supports both new conversations and resuming existing ones, providing flexibility for different use cases.

**Alternatives considered**:
- Always create new: Wastes resources, breaks continuity
- Single conversation per user: Limits flexibility for different topics

## MCP Tools Implementation Patterns

### Decision: Tool Schema Format
**Chosen**: JSON Schema compatible definitions
**Rationale**: Standard format that integrates well with Cohere's tool calling system and provides clear parameter validation.

**Example schema for add_task**:
```json
{
  "name": "add_task",
  "description": "Creates a new task with title and optional description",
  "parameters": {
    "type": "object",
    "properties": {
      "title": {"type": "string", "description": "The title of the task"},
      "description": {"type": "string", "description": "Optional description of the task"}
    },
    "required": ["title"]
  }
}
```

### Decision: Error Handling in Tools
**Chosen**: Structured error responses with success flags
**Rationale**: Provides clear feedback to both the AI system and end users about operation outcomes.

**Response format**:
```json
{
  "success": true/false,
  "message": "Descriptive message about the outcome",
  "data": { ... } // Optional data payload
}
```

## Conversation State Management

### Decision: Database Indexing Strategy
**Chosen**: Composite indexes on (user_id, created_at) for efficient retrieval
**Rationale**: Optimizes common queries for user's conversation history while maintaining performance.

**Additional indexes**:
- conversation_id on Message table for fast message lookup
- user_id on Conversation table for quick user isolation

### Decision: History Context Management
**Chosen**: Limit conversation history to last 20 messages for performance
**Rationale**: Balances context availability with API token limits and response performance.

**Fallback strategy**: Summarize older messages if deeper context is needed.

## Frontend Chat UI Patterns

### Decision: Chat Panel Layout
**Chosen**: Elegant slide-in from bottom-right with glassmorphic card
**Rationale**: Premium immersion that doesn't interfere with main UI while remaining easily accessible.

**Animation details**: Smooth 300ms transition with opacity and transform for polished feel.

### Decision: Message Rendering
**Chosen**: Markdown support for assistant responses
**Rationale**: Rich formatting (bold, italic, lists, code blocks) enhances professional feel and usability.

**User messages**: Plain text to maintain simplicity and security.

### Decision: Typing Indicator Style
**Chosen**: Subtle animated dots with fade effect
**Rationale**: Delightful yet unobtrusive, providing clear feedback during AI processing.

**Animation**: CSS-based for performance with smooth 1.4s cycle.

## Security & Authentication Patterns

### Decision: JWT Token Validation
**Chosen**: Middleware-based validation with user_id extraction
**Rationale**: Centralized security enforcement that's applied consistently across all endpoints.

**Implementation**: FastAPI dependency that validates token and extracts user identity.

### Decision: User Isolation Enforcement
**Chosen**: Database-level filtering by user_id in all queries
**Rationale**: Defense in depth approach where both application and database layers enforce isolation.

**Implementation**: SQLModel query filters applied automatically based on authenticated user.

## Testing & Validation Strategies

### Decision: Intelligence Validation Approach
**Chosen**: Diverse natural language test suite covering edge cases
**Rationale**: Ensures robust understanding across different phrasing and complex multi-step operations.

**Test categories**:
- Simple operations (add, delete, complete)
- Ambiguous references (delete by title vs ID)
- Multi-step chains (list then delete first)
- Identity queries ("Who am I?")

### Decision: Error Recovery Strategy
**Chosen**: Graceful degradation with user-friendly error messages
**Rationale**: Maintains user trust and provides clear guidance when operations fail.

**Implementation**: Catch exceptions and return helpful messages rather than technical errors.

## Performance Optimization Patterns

### Decision: Database Query Optimization
**Chosen**: Async operations with connection pooling
**Rationale**: Maintains responsiveness during database operations while scaling efficiently.

**Techniques**:
- Async SQLAlchemy sessions
- Connection pooling for Neon DB
- Proper indexing strategies

### Decision: API Token Management
**Chosen**: Environment variable with secure storage
**Rationale**: Standard security practice that protects API credentials.

**Implementation**: COHERE_API_KEY environment variable with validation at startup.

## Key Learnings & Implementation Notes

1. **Cohere Tool Calling**: Requires precise JSON schema definitions and consistent formatting for reliable operation
2. **State Management**: Database persistence is crucial for conversation continuity and reliability
3. **User Experience**: Micro-interactions and thoughtful animations significantly enhance perceived quality
4. **Security**: Multi-layered validation prevents cross-user data access and ensures compliance
5. **Performance**: Async operations and proper indexing are essential for responsive interactions