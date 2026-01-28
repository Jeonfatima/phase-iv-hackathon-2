# API Contracts: Todo Chatbot Application

## Overview
This document defines the API contracts for the Todo Chatbot application that will be deployed to Kubernetes. These contracts ensure consistent communication between frontend and backend services within the containerized environment.

## Base Configuration

### Service Endpoints in Kubernetes
```yaml
Backend Service:
  name: "backend-service"
  type: "ClusterIP"
  port: 80
  targetPort: 8000
  environment: "production"  # When running in Kubernetes

Frontend Service:
  name: "frontend-service"
  type: "ClusterIP"
  port: 80
  targetPort: 3000
```

### Environment-Specific Variables
```yaml
Environment Variables in Kubernetes:
  BACKEND_API_URL: "http://backend-service:80"  # Internal service communication
  FRONTEND_URL: "http://frontend-service:80"    # For ingress routing
  DATABASE_URL: "postgresql://..."              # From Kubernetes secret
  COHERE_API_KEY: "..."                        # From Kubernetes secret
  BETTER_AUTH_SECRET: "..."                    # From Kubernetes secret
```

## API Specifications

### Authentication API

#### POST /auth/token
**Description**: Authenticate user and return JWT token

**Request**:
```yaml
Path: /auth/token
Method: POST
Headers:
  Content-Type: application/x-www-form-urlencoded
Body:
  username: string (email format)
  password: string (encrypted)
```

**Response**:
```yaml
Success (200):
  Headers:
    Content-Type: application/json
  Body:
    access_token: string (JWT token)
    token_type: string (bearer)

Error (401):
  Headers:
    Content-Type: application/json
  Body:
    detail: string (error message)
```

**Kubernetes Specifics**:
- Available at: `http://backend-service:80/auth/token`
- Protected by Kubernetes NetworkPolicy
- Health check: `/auth/health`

### User Management API

#### GET /users/me
**Description**: Get current authenticated user details

**Request**:
```yaml
Path: /users/me
Method: GET
Headers:
  Authorization: Bearer {token}
```

**Response**:
```yaml
Success (200):
  Headers:
    Content-Type: application/json
  Body:
    id: string (UUID)
    email: string (email format)
    is_active: boolean

Error (401):
  Headers:
    Content-Type: application/json
  Body:
    detail: string (error message)
```

**Kubernetes Specifics**:
- Available at: `http://backend-service:80/users/me`
- Requires authentication token from Kubernetes secret

### Task Management API

#### GET /tasks
**Description**: Retrieve all tasks for authenticated user

**Request**:
```yaml
Path: /tasks
Method: GET
Headers:
  Authorization: Bearer {token}
```

**Response**:
```yaml
Success (200):
  Headers:
    Content-Type: application/json
  Body:
    tasks:
      - id: string (UUID)
        title: string
        description: string
        completed: boolean
        created_at: string (ISO 8601 datetime)
        updated_at: string (ISO 8601 datetime)
        user_id: string (UUID)

Error (401):
  Headers:
    Content-Type: application/json
  Body:
    detail: string (error message)
```

**Kubernetes Specifics**:
- Available at: `http://backend-service:80/tasks`
- Connected to Neon PostgreSQL database via Kubernetes secret

#### POST /tasks
**Description**: Create a new task

**Request**:
```yaml
Path: /tasks
Method: POST
Headers:
  Authorization: Bearer {token}
  Content-Type: application/json
Body:
  title: string (required)
  description: string (optional)
```

**Response**:
```yaml
Success (201):
  Headers:
    Content-Type: application/json
  Body:
    id: string (UUID)
    title: string
    description: string
    completed: boolean
    created_at: string (ISO 8601 datetime)
    updated_at: string (ISO 8601 datetime)
    user_id: string (UUID)

Error (400):
  Headers:
    Content-Type: application/json
  Body:
    detail: string (validation error)

Error (401):
  Headers:
    Content-Type: application/json
  Body:
    detail: string (authentication error)
```

**Kubernetes Specifics**:
- Available at: `http://backend-service:80/tasks`
- Persistent storage via external Neon database

#### PUT /tasks/{task_id}
**Description**: Update an existing task

**Request**:
```yaml
Path: /tasks/{task_id}
Method: PUT
Headers:
  Authorization: Bearer {token}
  Content-Type: application/json
Path Parameters:
  task_id: string (UUID)
Body:
  title: string (optional)
  description: string (optional)
  completed: boolean (optional)
```

**Response**:
```yaml
Success (200):
  Headers:
    Content-Type: application/json
  Body:
    id: string (UUID)
    title: string
    description: string
    completed: boolean
    created_at: string (ISO 8601 datetime)
    updated_at: string (ISO 8601 datetime)
    user_id: string (UUID)

Error (401):
  Headers:
    Content-Type: application/json
  Body:
    detail: string (authentication error)

Error (404):
  Headers:
    Content-Type: application/json
  Body:
    detail: string (task not found)
```

#### DELETE /tasks/{task_id}
**Description**: Delete a task

**Request**:
```yaml
Path: /tasks/{task_id}
Method: DELETE
Headers:
  Authorization: Bearer {token}
Path Parameters:
  task_id: string (UUID)
```

**Response**:
```yaml
Success (204):
  Headers:
    Content-Type: application/json
  Body: (empty)

Error (401):
  Headers:
    Content-Type: application/json
  Body:
    detail: string (authentication error)

Error (404):
  Headers:
    Content-Type: application/json
  Body:
    detail: string (task not found)
```

### AI Chatbot API

#### POST /chat
**Description**: Send a message to the AI chatbot and receive a response

**Request**:
```yaml
Path: /chat
Method: POST
Headers:
  Authorization: Bearer {token}
  Content-Type: application/json
Body:
  message: string (required)
  context: object (optional) - additional context for the chat
```

**Response**:
```yaml
Success (200):
  Headers:
    Content-Type: application/json
  Body:
    response: string (AI-generated response)
    timestamp: string (ISO 8601 datetime)
    context: object (updated context)

Error (401):
  Headers:
    Content-Type: application/json
  Body:
    detail: string (authentication error)

Error (503):
  Headers:
    Content-Type: application/json
  Body:
    detail: string (AI service unavailable)
```

**Kubernetes Specifics**:
- Available at: `http://backend-service:80/chat`
- Requires COHERE_API_KEY from Kubernetes secret
- May require higher resource limits due to AI processing

## Health Check Endpoints

### GET /health
**Description**: Overall application health check

**Request**:
```yaml
Path: /health
Method: GET
```

**Response**:
```yaml
Success (200):
  Headers:
    Content-Type: application/json
  Body:
    status: string ("healthy")
    timestamp: string (ISO 8601 datetime)
    services:
      database: boolean
      cohere_api: boolean
```

### GET /ready
**Description**: Readiness probe for Kubernetes

**Request**:
```yaml
Path: /ready
Method: GET
```

**Response**:
```yaml
Success (200):
  Headers:
    Content-Type: application/json
  Body:
    status: string ("ready")

Error (503):
  Headers:
    Content-Type: application/json
  Body:
    status: string ("not ready")
    reason: string (reason for not being ready)
```

### GET /startup
**Description**: Startup probe for Kubernetes

**Request**:
```yaml
Path: /startup
Method: GET
```

**Response**:
```yaml
Success (200):
  Headers:
    Content-Type: application/json
  Body:
    status: string ("started")
```

## Service Communication Contract

### Internal Communication
Services within the Kubernetes cluster communicate using internal DNS names:

```yaml
Frontend to Backend:
  URL: http://backend-service:80
  Protocol: HTTP/1.1
  Timeout: 30 seconds
  Retry Policy: Exponential backoff, max 3 retries

Database Connection:
  Host: (from DATABASE_URL secret)
  Port: 5432 (for PostgreSQL)
  SSL: Required
  Connection Pool: 10 connections
```

### Security Requirements
1. All API endpoints require authentication except health checks
2. JWT tokens must be validated by the backend
3. All secrets must be retrieved from Kubernetes secrets
4. Network communication within the cluster should be secured with NetworkPolicy

## Error Handling Contract

### Standard Error Format
All error responses follow this format:

```yaml
{
  "detail": string,
  "timestamp": string (ISO 8601 datetime),
  "error_code": string (optional)
}
```

### Common HTTP Status Codes
- 200: Success
- 201: Created
- 204: No Content
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Validation Error
- 500: Internal Server Error
- 503: Service Unavailable