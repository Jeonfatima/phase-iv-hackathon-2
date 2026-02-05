---
name: "fastapi-rest-generator"
description: "Generate secure REST APIs using FastAPI, SQLModel, and JWT authentication."
version: "1.0.0"
---

# FastAPI REST Generator Skill

## When to Use
- Creating API endpoints
- Implementing CRUD routes
- JWT-secured services

## How It Works
1. Read API spec
2. Generate Pydantic models
3. Create route handlers
4. Enforce auth & user isolation
5. Handle errors properly

## Rules
- All routes under /api
- JWT required for all requests
- Filter data by authenticated user

## Output
- routes/*.py
- models.py
- auth middleware
