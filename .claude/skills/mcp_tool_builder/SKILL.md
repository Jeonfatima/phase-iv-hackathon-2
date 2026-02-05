---
name: "mcp-tool-builder"
description: "Create MCP tools that expose backend functionality to AI agents."
version: "1.0.0"
---

# MCP Tool Builder Skill

## When to Use
- Building AI tools
- Exposing task operations to agents
- Phase III chatbot work

## How It Works
1. Read MCP tool spec
2. Define input/output schemas
3. Implement stateless handlers
4. Connect to database
5. Return structured JSON

## Rules
- Tools must be stateless
- All state stored in DB
- Clear success/error responses

## Output
- mcp_server.py
- tool definitions
- handlers
