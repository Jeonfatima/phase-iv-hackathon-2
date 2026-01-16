# Quickstart Guide: AI Todo Chatbot Integration

## Prerequisites

- Python 3.11+ with pip
- Node.js 18+ with npm/yarn
- Cohere API Key (contact admin or use provided key: YOUR_COHERE_API_KEY_HERE)
- PostgreSQL database (Neon DB recommended)
- Better Auth configured for user authentication

## Setup Instructions

### 1. Environment Configuration

Copy the example environment file and add your Cohere API key:

```bash
# Backend setup
cd backend
cp .env.example .env
```

Edit the `.env` file to include:

```env
COHERE_API_KEY=YOUR_COHERE_API_KEY_HERE
DATABASE_URL=your_database_url_here
BETTER_AUTH_SECRET=your_auth_secret_here
```

### 2. Backend Installation

```bash
cd backend
pip install -r requirements.txt
pip install cohere-toolkit  # For Cohere integration
```

### 3. Frontend Installation

```bash
cd frontend
npm install
# or
yarn install
```

### 4. Database Setup

Run the database migrations to create the new Conversation and Message tables:

```bash
cd backend
# Create new models for conversations
python -c "
from sqlmodel import SQLModel
from models.conversation import Conversation, Message
from database.session import engine

# Create tables
SQLModel.metadata.create_all(engine)
print('Conversation and Message tables created successfully!')
"
```

## Running the Application

### 1. Start Backend Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 2. Start Frontend Server

```bash
cd frontend
npm run dev
# or
yarn dev
```

## Using the AI Chatbot

### 1. Access the Chat Interface

1. Navigate to your application in a browser
2. Look for the floating chatbot button in the bottom-right corner
3. Click the button to open the chat panel

### 2. Natural Language Commands

Try these example commands:

```
"Add a task to buy groceries"
"Delete task number 3"
"Mark task 'Call mom' as complete"
"Show me my pending tasks"
"Who am I?"
"List all my tasks and add a new one called 'Finish report'"
```

### 3. API Direct Usage

You can also interact with the chat API directly:

```bash
# Replace {user_id} with the actual user ID
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy milk",
    "conversation_id": null
  }'
```

## Key Features

### MCP-Style Tools Available

The AI chatbot has access to these tools:

1. **add_task**: Creates new tasks
2. **delete_task**: Removes tasks by ID
3. **update_task**: Modifies task properties
4. **complete_task**: Toggles task completion status
5. **list_tasks**: Shows user's tasks with optional filtering
6. **get_current_user**: Returns user's email and ID

### Conversation Persistence

- All conversations are saved to the database
- Conversation history persists across sessions
- Users can resume previous conversations

### Security Features

- JWT-based authentication required
- User isolation - users can only access their own data
- Input validation and sanitization

## Troubleshooting

### Common Issues

**Issue**: Chatbot not responding
**Solution**: Check that COHERE_API_KEY is properly set in environment variables

**Issue**: Database connection errors
**Solution**: Verify DATABASE_URL is correct and database is accessible

**Issue**: Unauthorized access errors
**Solution**: Ensure JWT token is valid and properly formatted in authorization header

**Issue**: Tool calls not executing
**Solution**: Check backend logs for tool execution errors

### API Endpoints

- `POST /api/{user_id}/chat` - Main chat interaction endpoint
- `GET /api/users/{user_id}/conversations` - List user's conversations
- `GET /api/conversations/{id}/messages` - Get messages for a conversation

## Development

### Adding New Tools

To add new MCP-style tools:

1. Define the tool function in `backend/services/mcp_tools.py`
2. Register the tool in the tools registry
3. Update the tool schema for Cohere
4. Test the tool through the chat interface

### Customizing the UI

The chat interface components are located in:
- `frontend/src/components/ChatBotButton.tsx`
- `frontend/src/components/ChatPanel.tsx`
- `frontend/src/components/MessageBubble.tsx`

### Environment Variables Reference

- `COHERE_API_KEY`: Required for AI functionality
- `DATABASE_URL`: Database connection string
- `BETTER_AUTH_SECRET`: Authentication secret
- `DEBUG`: Enable debug mode (true/false)