# Implementation Plan: AI Todo Chatbot Integration

**Branch**: `001-ai-chatbot-integration` | **Date**: 2026-01-16 | **Spec**: [AI Todo Chatbot Integration Spec](./spec.md)
**Input**: Feature specification from `/specs/001-ai-chatbot-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a Cohere-powered AI chatbot that enables natural language task management for the todo application. The system will provide MCP-style tools for task operations (add, delete, update, complete, list) and user identity queries, with persistent conversation history stored in the database. The frontend will feature a premium glassmorphic chat interface integrated seamlessly with the existing design.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/JavaScript, Next.js 14+
**Primary Dependencies**: FastAPI, SQLModel, Cohere API, Better Auth, Neon PostgreSQL
**Storage**: Neon PostgreSQL database with Conversation and Message models
**Testing**: pytest for backend, Jest/React Testing Library for frontend
**Target Platform**: Web application (Next.js frontend + FastAPI backend)
**Project Type**: Full-stack web application with AI integration
**Performance Goals**: <3 seconds response time for 90% of requests, 95% intent recognition accuracy
**Constraints**: <200ms p95 latency for database operations, stateless backend architecture, secure JWT authentication
**Scale/Scope**: Single tenant per user, conversation history persistence, multi-user isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **Constitution Compliance**: Implementation follows all requirements in constitution.md including Cohere API integration, MCP tools, and stateless architecture
- ✅ **Security Requirements**: JWT authentication and user isolation will be implemented as required
- ✅ **Database Extensions**: Conversation and Message models will be created as specified
- ✅ **Cohere Integration**: Will replace OpenAI with Cohere API as required
- ✅ **Frontend Integration**: Glassmorphic chat UI will be implemented as specified
- ✅ **No Manual Coding**: All work will be performed through Claude Code agents

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-chatbot-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── conversation.py    # Conversation and Message SQLModel definitions
│   │   └── __init__.py
│   ├── services/
│   │   ├── ai_service.py      # Cohere integration and reasoning loop
│   │   ├── chat_service.py    # Conversation management
│   │   ├── mcp_tools.py       # MCP-style tools for task operations
│   │   └── __init__.py
│   └── api/
│       └── chat.py            # Chat endpoint implementation
└── tests/
    └── test_chat.py

frontend/
├── src/
│   ├── components/
│   │   ├── ChatBotButton.tsx  # Floating chatbot button
│   │   ├── ChatPanel.tsx      # Main chat panel UI
│   │   └── MessageBubble.tsx  # Individual message display
│   ├── hooks/
│   │   └── useChat.ts         # Chat state management
│   └── services/
│       └── chatService.ts     # API communication layer
└── types/
    └── chat.ts                # Chat-related TypeScript interfaces
```

**Structure Decision**: Full-stack web application with backend API endpoints and frontend UI components. Backend extends existing structure with new models, services, and API routes. Frontend adds new components for chat interface.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Phase 0: Research & Discovery

### Research Tasks

1. **Cohere API Integration Research**
   - Best practices for tool calling with Cohere
   - Prompt engineering for structured JSON output
   - Error handling and retry strategies

2. **MCP Tools Implementation Patterns**
   - Standardized tool schema definitions
   - JSON parsing and validation strategies
   - Multi-step reasoning loop implementation

3. **Conversation State Management**
   - Database design for conversation persistence
   - Message ordering and retrieval strategies
   - History context management for AI

4. **Frontend Chat UI Patterns**
   - Glassmorphic design implementation with Tailwind
   - Real-time messaging with React hooks
   - Responsive design for mobile compatibility

### Expected Outcomes

- Research.md documenting Cohere integration patterns
- Tool schema definitions and JSON parsing strategies
- Database model designs for conversation persistence
- Frontend component architecture for chat interface

## Phase 1: Design & Architecture

### Data Model Design

1. **Conversation Model**
   - Primary key: id
   - Foreign key: user_id (from JWT authentication)
   - Timestamps: created_at, updated_at

2. **Message Model**
   - Primary key: id
   - Foreign key: conversation_id
   - Fields: role (user/assistant/tool), content, timestamp

3. **Relationships**
   - One-to-many: Conversation to Messages
   - User isolation via user_id foreign key

### API Contract Design

1. **POST /api/{user_id}/chat**
   - Request: `{ conversation_id?: number, message: string }`
   - Response: `{ conversation_id: number, response: string, tool_calls?: array }`
   - Authentication: JWT token validation
   - Authorization: User isolation via user_id

2. **Tool Schema Definitions**
   - add_task: { title: string, description?: string }
   - delete_task: { task_id: number }
   - update_task: { task_id: number, title?: string, description?: string, completed?: boolean }
   - complete_task: { task_id: number, completed: boolean }
   - list_tasks: { filter?: "all"|"pending"|"completed" }
   - get_current_user: {}

### System Architecture

1. **Authentication Layer**
   - JWT validation middleware
   - User identity extraction
   - Permission verification

2. **AI Service Layer**
   - Cohere client initialization
   - Prompt construction with conversation history
   - Tool calling loop implementation
   - Response formatting

3. **Data Access Layer**
   - Conversation and Message CRUD operations
   - User isolation enforcement
   - Transaction management

## Phase 2: Implementation Strategy

### Backend Implementation Order

1. **Database Models** (Day 1 AM)
   - Conversation and Message SQLModel definitions
   - Database migration setup
   - Basic CRUD operations

2. **MCP Tools** (Day 1 PM)
   - Task operation tools (add, delete, update, complete, list)
   - User identity tool
   - Tool schema definitions

3. **AI Service** (Day 2 AM)
   - Cohere client integration
   - Prompt engineering for reasoning
   - Tool calling loop implementation

4. **Chat Endpoint** (Day 2 PM)
   - Authentication middleware
   - Conversation management
   - API contract implementation

### Frontend Implementation Order

1. **UI Components** (Day 2 PM)
   - Chat panel with glassmorphic design
   - Message bubbles with distinct styling
   - Floating chat button

2. **State Management** (Day 3 AM)
   - Chat session state
   - Message history management
   - Loading states

3. **API Integration** (Day 3 AM)
   - Chat service for API communication
   - Error handling and retries
   - Real-time message updates

### Integration & Testing (Day 3 PM)

1. **End-to-end testing**
   - Natural language command processing
   - Conversation persistence
   - User isolation verification

2. **Performance validation**
   - Response time measurements
   - Database query optimization
   - Memory usage monitoring

## Phase 3: Validation & Delivery

### Quality Assurance

1. **Functional Testing**
   - All natural language commands work correctly
   - Multi-step operations execute properly
   - User identity queries return correct data

2. **Security Testing**
   - JWT authentication validates properly
   - Cross-user data access prevented
   - API keys protected from exposure

3. **Performance Testing**
   - Response times meet requirements
   - Database queries optimized
   - Memory usage acceptable

### Deployment Preparation

1. **Environment Configuration**
   - COHERE_API_KEY setup
   - Database connection strings
   - Authentication secrets

2. **Documentation Updates**
   - README.md with setup instructions
   - API documentation
   - Usage examples

3. **Demo Preparation**
   - Sample conversations prepared
   - Edge case demonstrations
   - Performance benchmarks documented

### Success Criteria Validation

- ✅ Natural language commands result in correct task operations 95%+ of the time
- ✅ Chatbot responds to user queries within 3 seconds for 90% of requests
- ✅ All conversation history persists correctly in database
- ✅ Perfect multi-user isolation with no cross-user data access
- ✅ Premium glassmorphic UI matching design standards
- ✅ Error handling provides clear, helpful feedback