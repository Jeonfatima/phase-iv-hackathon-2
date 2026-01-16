# Phase II – Todo Full-Stack Web Application

A modern, multi-user todo application with authentication and persistent storage, built with Next.js, FastAPI, and PostgreSQL.

## 🚀 Features

- **Multi-user support** - Each user has their own secure todo list
- **Full CRUD operations** - Create, Read, Update, Delete, and toggle completion status
- **Secure authentication** - JWT-based authentication with Better Auth
- **Responsive design** - Works on desktop, tablet, and mobile devices
- **Real-time updates** - Changes reflect immediately in the UI
- **Persistent storage** - Todos stored securely in PostgreSQL database
- **AI-Powered Chatbot** - Natural language task management with Cohere AI integration
- **Glassmorphic UI** - Premium chat interface with smooth animations and modern design

## 🛠 Tech Stack

- **Frontend:** Next.js 16+ (App Router), TypeScript, Tailwind CSS, Framer Motion
- **Backend:** Python FastAPI, Cohere AI, SQLModel
- **Database:** Neon Serverless PostgreSQL
- **ORM:** SQLModel
- **Authentication:** Better Auth (JWT)
- **Styling:** Tailwind CSS
- **AI Integration:** Cohere command-r-plus model with tool calling

## 📁 Project Structure

```
├── frontend/                 # Next.js frontend application
│   ├── app/                  # App Router pages
│   ├── components/           # Reusable UI components
│   ├── lib/                  # Utility functions and services
│   └── styles/               # Global styles
├── backend/                  # FastAPI backend application
│   ├── main.py               # Application entry point
│   ├── requirements.txt      # Python dependencies
│   ├── database/             # Database connection and setup
│   │   ├── engine.py         # Database engine
│   │   └── session.py        # Session management
│   ├── models/               # SQLModel database models
│   │   ├── task.py           # Task model
│   │   └── conversation.py   # Conversation and Message models
│   ├── services/             # Business logic services
│   │   ├── task_service.py   # Task operations
│   │   ├── mcp_tools.py      # AI tools for task operations
│   │   ├── ai_service.py     # Cohere AI integration
│   │   └── chat_service.py   # Chat conversation management
│   ├── api/                  # API route definitions
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── task_router.py    # Task management endpoints
│   │   └── chat.py           # AI Chatbot endpoints
│   ├── core/                 # Core configuration
│   │   └── config.py         # Configuration settings
│   └── README.md             # Backend setup instructions
├── specs/                    # Specification documents
│   ├── overview.md           # Project overview
│   ├── architecture.md       # System architecture
│   ├── features/             # Feature specifications
│   ├── api/                  # API specifications
│   ├── database/             # Database specifications
│   └── ui/                   # UI specifications
├── .env.example             # Environment variables example
├── README.md                # This file
└── CLAUDE.md                # Claude Code development guidelines
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+ for backend
- PostgreSQL (or Neon Serverless account)
- Cohere API Key for AI features

### AI Chatbot Setup

1. Get your Cohere API key from [Cohere Console](https://dashboard.cohere.ai/api-keys)
2. Add it to your backend `.env` file:
   ```env
   COHERE_API_KEY=your-cohere-api-key-here
   ```

### Setup Instructions

#### 1. Clone the repository
```bash
git clone <repository-url>
cd hackathon-II-todo
```

#### 2. Set up the Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the environment example and configure:
```bash
cp .env.example .env
```

5. Update the `.env` file with your configuration:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todoapp
DEBUG=true
```

6. Run the application:
```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --port 8000
```

#### 3. Access the Application

- Backend API: [http://localhost:8000](http://localhost:8000)
- Backend API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health Check: [http://localhost:8000/health](http://localhost:8000/health)
- DB Health: [http://localhost:8000/db-health](http://localhost:8000/db-health)

## 🔐 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todoapp
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
BETTER_AUTH_URL=http://localhost:8000
JWT_EXPIRATION=24h
DEBUG=true
```

## 🔐 Authentication & Authorization

### Better Auth Integration
The application integrates with Better Auth for secure JWT-based authentication with user isolation:

- **Frontend Authentication**: Users register/login through Better Auth frontend components
- **JWT Verification**: Backend verifies JWT tokens issued by Better Auth
- **Protected Endpoints**: All task endpoints require valid JWT tokens from Better Auth
- **User Isolation**: Users can only access their own tasks

### Task Endpoints with Authorization
- `POST /api/{user_id}/tasks` - Create task for user
- `GET /api/{user_id}/tasks` - Get all tasks for user
- `GET /api/{user_id}/tasks/{task_id}` - Get specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Update completion status

### AI Chatbot Endpoints with Authorization
- `POST /api/{user_id}/chat` - Send message to AI assistant and receive response
- `GET /api/{user_id}/conversations` - Get all conversations for user
- `GET /api/{user_id}/conversations/{conversation_id}/messages` - Get messages in conversation

### Authorization Flow
1. User authenticates through Better Auth frontend and receives JWT token
2. Frontend includes JWT token in Authorization header: `Bearer <token>`
3. Backend verifies token signature using `BETTER_AUTH_SECRET`
4. Backend extracts user ID from token (either `userId` or `sub` field)
5. Backend validates URL user_id matches token user_id
6. Returns 401 for invalid/missing tokens, 403 for user mismatches

### Important Notes
- Backend does NOT handle user registration/login/passwords
- Authentication is managed entirely by Better Auth
- Backend only verifies tokens and enforces authorization

## 🤖 AI Chatbot Usage

The AI Chatbot enables natural language task management. Simply click the chat button in the bottom-right corner and speak to your todo list conversationally:

- "Add a task to buy groceries" - Creates a new task
- "Show me my pending tasks" - Lists all incomplete tasks
- "Mark task 3 as complete" - Updates task completion status
- "Delete the meeting task" - Removes a specific task
- "Who am I?" - Returns your user information

The AI understands complex requests and can chain multiple operations together.

## 🧪 Running Tests

### Backend Tests
```bash
cd backend
python -m pytest
```

## 🚀 Deployment

### Backend Deployment
1. Set up your production database (Neon Serverless recommended)
2. Configure environment variables for production
3. Deploy using your preferred Python hosting solution (Heroku, Vercel, etc.)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/feature-name`
3. Make your changes
4. Commit your changes: `git commit -m 'Add some feature'`
5. Push to the branch: `git push origin feature/feature-name`
6. Open a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, please open an issue in the GitHub repository.