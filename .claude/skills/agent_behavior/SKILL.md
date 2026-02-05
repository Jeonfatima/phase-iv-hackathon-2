---
name: "agent-behavior-mapper"
description: "Translate natural language into MCP tool calls using OpenAI Agents SDK."
version: "1.0.0"
---

# Agent Behavior Skill

## When to Use
- Building conversational AI
- Mapping user intent to tools

## How It Works
1. Analyze user intent
2. Select correct MCP tool
3. Extract parameters
4. Call tool
5. Confirm action in response

## Rules
- Always confirm actions
- Handle missing info gracefully
- Never hallucinate task IDs

## Output
- Agent prompt
- Tool calling logic
