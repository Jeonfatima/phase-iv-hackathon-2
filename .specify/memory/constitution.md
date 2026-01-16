<!--
Sync Impact Report:
- Version change: 1.0.0 → 3.0.0
- Modified principles: All principles updated for Phase III
- Added sections: Chatbot Functionality, MCP Tools, Cohere API sections
- Removed sections: Phase I specific requirements
- Templates requiring updates: ✅ .specify/templates/plan-template.md, ✅ .specify/templates/spec-template.md, ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->

# Todo Chatbot Integration Constitution - Phase III: Full-Stack Web Application with AI

## Project Overview

The Evolution of Todo continues from Phase I (Console Application) and Phase II (Full-Stack Web) to Phase III, integrating a powerful AI-powered chatbot into the existing full-stack backend (FastAPI + Neon DB + Better Auth). The objective is to provide natural language task management with full CRUD functionality, enabling users to manage tasks through conversational interfaces while maintaining all existing features.

## Core Requirements

### I. Conversational Interface for Task Management
The chatbot must support all five core task operations through natural language: Add Task, Delete Task, Update Task, List Tasks, and Mark Task Complete/Incomplete. The interface must handle complex queries that chain multiple operations (e.g., "Add weekly meeting and list pending tasks").

### II. User Identity and Session Queries
The chatbot must respond to user identity queries such as "Who am I?" with the logged-in user's email address (e.g., "Logged in as example@email.com"), extracted securely from the authenticated session.

### III. Stateless Architecture
The system must be stateless with no server-side session storage. All conversation state must be persisted in the database using Conversation and Message models to maintain continuity across requests.

### IV. Cohere API Integration
Replace OpenAI Agents SDK with Cohere's API for all AI logic, adapting agent-like behavior to use Cohere's chat/completions endpoint for tool calling and reasoning. The system must structure prompts to reason step-by-step and output tool invocation JSON.

## Chatbot Functionality & Natural Language Handling

### Natural Language Processing
The chatbot must interpret natural language commands and map them to specific MCP tools. Examples include:
- "Add a task called 'Buy groceries'" → add_task tool with title "Buy groceries"
- "Delete task number 5" → delete_task tool with id 5
- "Mark task 3 as complete" → update_task tool with completed true
- "Show me my tasks" → list_tasks tool

### Confirmation and Error Handling
The system must provide clear confirmations for all operations (e.g., "Task 'Buy groceries' added successfully") and graceful error handling with informative messages when operations fail.

### Multi-Turn Conversations
The chatbot must maintain context across multiple exchanges, allowing users to reference previous statements or tasks without repeating information.

## Authentication & Security

### JWT-Based User Isolation
All endpoints must validate JWT tokens to extract user_id and ensure proper user isolation. Each user's tasks and conversations must be completely isolated from other users.

### Secure Session Management
User email information must be securely extracted from authenticated sessions without exposing sensitive data. The system must validate user permissions before performing any task operations.

### Conversation Privacy
Each user's conversation history must be accessible only to that user, with proper authentication checks on all conversation-related endpoints.

## Non-Functional Requirements

### Performance and Scalability
The system must handle concurrent users efficiently with asynchronous operations where possible. Response times should remain under 2 seconds for typical requests.

### Error Resilience
The system must gracefully handle network timeouts, database connection issues, and API failures from Cohere with appropriate fallback mechanisms and user notifications.

### Code Quality
All code must follow clean architecture principles with clear separation of concerns between authentication, business logic, database operations, and AI integration.

## Technology Stack and Tools

### Backend Extensions
Extend existing Phase I stack with:
- FastAPI for new chat endpoints
- SQLModel for Conversation and Message models
- Neon PostgreSQL for persistent storage
- Better Auth for user authentication
- Cohere API for AI reasoning and tool calling
- Official MCP SDK for tool integration

### Frontend Integration
Integrate ChatKit or similar component for conversational UI, maintaining consistency with existing frontend architecture.

## Development Workflow

### Agentic Development Process
Follow the spec → plan → tasks → Claude Code workflow with all development performed through Claude Code agents and Spec-Kit Plus skills. No manual coding is permitted.

### Cohere API Key Management
Use the provided COHERE_API_KEY=YOUR_COHERE_API_KEY_HERE for all AI calls, with proper environment variable management.

### Testing and Validation
Implement comprehensive testing for all new functionality including authentication, conversation persistence, and AI integration.

## Monorepo Updates

### Backend Extensions
Extend the /backend directory with:
- New chat endpoint at /api/{user_id}/chat
- MCP server implementation for tool exposure
- Conversation and Message model definitions
- Cohere API integration services

### Database Model Extensions
Add new models to maintain conversation state:
- Conversation model with user_id and id fields
- Message model with conversation_id, role, and content fields

## Database Extensions

### Conversation Model
```python
class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str  # Links to authenticated user
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Message Model
```python
class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")
    role: str  # "user", "assistant", "tool"
    content: str  # The message content
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

## MCP Tools Specification

### 1. add_task Tool
- **Purpose**: Add a new task to the user's task list
- **Parameters**: { "title": "string", "description": "string" }
- **Returns**: { "success": "boolean", "task_id": "int", "message": "string" }

### 2. delete_task Tool
- **Purpose**: Delete an existing task from the user's task list
- **Parameters**: { "task_id": "int" }
- **Returns**: { "success": "boolean", "message": "string" }

### 3. update_task Tool
- **Purpose**: Update an existing task's properties
- **Parameters**: { "task_id": "int", "title": "string?", "description": "string?", "completed": "boolean?" }
- **Returns**: { "success": "boolean", "message": "string" }

### 4. list_tasks Tool
- **Purpose**: Retrieve all tasks for the current user
- **Parameters**: { "filter": "string?" } // "all", "pending", "completed"
- **Returns**: { "tasks": "array", "count": "int" }

### 5. get_current_user_email Tool
- **Purpose**: Retrieve the current user's email from authenticated session
- **Parameters**: {}
- **Returns**: { "email": "string", "user_id": "string" }

## Cohere API Adaptation

### Reasoning and Tool Calling
Structure prompts to Cohere to encourage step-by-step reasoning and JSON-formatted tool invocation. The system should parse Cohere's responses to extract tool call information and execute the appropriate MCP tools.

### Multi-Turn Conversation Management
Maintain conversation history by retrieving and storing messages in the database. Pass relevant conversation context to Cohere to maintain continuity across exchanges.

### Response Formatting
Process Cohere's responses to format them appropriately for the chat interface while preserving the natural conversational flow.

## Guiding Principles

### AI-First Design
Prioritize AI integration as the primary interaction method while maintaining traditional API endpoints as secondary options.

### Stateless Architecture
No server-side session state; all conversation persistence occurs in the database to ensure scalability and reliability.

### Security-First Approach
Implement robust authentication and user isolation as the highest priority, ensuring no cross-user data leakage.

### No Manual Coding
All implementation must be performed through Claude Code agents and Spec-Kit Plus skills without any direct manual code changes.

### Hackathon Transparency
Maintain clear documentation and code structure suitable for judge evaluation of agentic AI integration quality.

## Deliverables and Success Criteria

### Working Chatbot
A fully functional AI-powered chatbot that responds to natural language commands for all task operations and user identity queries.

### Repository Updates
Complete integration into the existing monorepo structure with proper documentation and code organization.

### Demo Capability
Demonstrate natural language queries that correctly handle full task management functionality (add, delete, update, list, complete) and user identification.

### Production-Ready Code
Clean, well-documented code with proper error handling, security measures, and performance considerations.

## Governance

This constitution supersedes all other practices and development guidelines for Phase III implementation. Amendments require explicit documentation and approval process. All pull requests and code reviews must verify constitution compliance. Specifications serve as the authoritative source for all implementation decisions.

**Version**: 3.0.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-15