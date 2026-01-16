---
id: 1
title: Todo Chatbot Integration
stage: constitution
date: 2026-01-15
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: claude
command: sp.constitution
labels: [constitution, phase3, chatbot, ai]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
# Todo Chatbot Integration for The Evolution of Todo - Phase III: Full-Stack Web Application

**Target audience:**
Hackathon judges evaluating cutting-edge agentic AI integrations, developers building intelligent productivity tools, and AI agents (Claude Code) implementing via Spec-Kit Plus in a monorepo.

**Focus:**
Create a comprehensive, authoritative constitution that seamlessly integrates a powerful AI-powered chatbot into the existing Phase I full-stack backend (FastAPI + Neon DB + Better Auth).

The chatbot must handle all core task functionalities (add, delete, mark complete, update, list) through natural language, provide user email info from the logged-in session, and offer full conversational control.

Replace OpenAI Agents SDK with Cohere's API for AI logic – adapt any agent-like code to use Cohere's chat/completions endpoint for tool calling and reasoning.

This document serves as the foundational governance for Phase III, ensuring stateless architecture, MCP tools for task operations, and persistent conversation state in the database.

**Success criteria:**
* Defines a chatbot with full functionality: natural language task management (CRUD + complete), user email queries (e.g., "Who am I?" -> "Logged in as example@email.com"), confirmations, error handling, and graceful responses.
* Integrates seamlessly into existing backend: single stateless /api/(user_id)/chat endpoint, MCP tools exposed, Cohere API for AI reasoning/tool invocation.
* Adapts OpenAI-style agent behavior to Cohere API: use Cohere's chat endpoint for multi-turn conversations with tool calls.
* Ensures multi-user security: JWT auth for user _id, task isolation, conversation persistence per user.
* Generates a complete Markdown file (constitution.md) version v3.0 placed at repository root – ready to guide all Phase III specs, plans, agents, and implementations.

Resulting chatbot feels intelligent, helpful, and production-ready: handles complex queries (e.g., "Add weekly meeting and list pending tasks") by chaining tools.

**Constraints:**

**Format:**
Markdown with deeply structured sections (Project Overview, Core Requirements, Chatbot Functionality & Natural Language Handling, Authentication & Security, Non-Functional Requirements, Technology Stack and Tools, Development Workflow, Monorepo Updates, Database Extensions, MCP Tools Specification, Cohere API Adaptation, Guiding Principles, Deliverables and Success Criteria).

* Version: v3.0 (Phase III), include current date (January 06, 2026)
* Strictly integrate into existing monorepo: extend /backend with MCP server and chat endpoint; add ChatKit to frontend if needed.
* Dependencies limited to: Existing stack (FastAPI, SQLModel, Neon PostgreSQL, Better Auth) + Cohere API (for AI chat/completions), Official MCP SDK (for tools). No additional frameworks.

◦ Cohere Adaptation:
Use Cohere's API key for all AI calls; simulate agent/tool-calling by structuring prompts to reason step-by-step and output tool invocation JSON.

* Stateless: No server state – persist conversations/messages in DB.
* No manual coding: All via Claude Code agents/skills.
* Keep concise yet exhaustive (under 3000 words).
* Reference Phase I/II briefly as completed foundation.

**Specific Sections Required:**
1. **Project Overview** – Summarize evolution to AI chatbot, objective: natural language task management with full functionality
2. **Core Requirements** – Conversational interface for 5 basic features, user email queries, stateless endpoint
3. **Chatbot Functionality & Natural Language Handling** – Detail flows, examples (e.g., "Add task" → add_task tool), confirmations, errors
4. **Authentication & Security** – JWT for user _id / email extraction, isolation in tools/conversations
5. **Non-Functional Requirements** – Clean code, async ops, scalability, graceful errors
6. **Technology Stack and Tools** – Extend Phase I: Cohere API for AI, MCP SDK for tools, ChatKit frontend
7. **Development Workflow** – Agentic: spec → plan → tasks → Claude Code; Cohere API key usage
8. **Monorepo Updates** – Extend structure: add chatbot routes, DB models (Conversation, Message)
9. **Database Extensions** – New models: Conversation (user_id, id), Message (conversation_id, role, content)
10. **MCP Tools Specification** – Exact 5 tools with params/returns, stateless DB interaction
11. **Cohere API Adaptation** – Detail how to adapt agent logic: prompt Cohere for reasoning/tool calls, parse JSON output
12. **Guiding Principles** – AI-first, stateless, security, no manual code, hackathon transparency
13. **Deliverables and Success Criteria** – Working chatbot, repo updates, demo: natural queries handle full features

**Environment Variables:**
* COHERE_API_KEY=YOUR_COHERE_API_KEY_HERE (for AI calls)
* Use existing BETTER_AUTH_SECRET, DATABASE_URL

Generate immediately.
This constitution must guarantee a seamless, intelligent, error-free chatbot integration that elevates the full-stack app to flagship AI status.
Perf
```

## Response snapshot

Updated the constitution file at `.specify/memory/constitution.md` to version 3.0 for Phase III Todo Chatbot Integration. The new constitution includes all required sections covering:
- Project overview for Phase III AI chatbot integration
- Core requirements for conversational interface and stateless architecture
- Chatbot functionality and natural language handling specifications
- Authentication and security requirements
- Technology stack extensions with Cohere API
- MCP tools specification for the 5 required tools
- Database extensions for Conversation and Message models
- Cohere API adaptation guidelines
- Guiding principles for AI-first, stateless, and security-focused development

## Outcome

- ✅ Impact: Updated constitution to v3.0 for Phase III, replacing Phase I requirements with chatbot integration requirements
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with comprehensive Phase III requirements
- 🔁 Next prompts: Ready for Phase III specification and planning
- 🧠 Reflection: Constitution now properly guides AI chatbot development with Cohere API integration

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All required sections implemented
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin Phase III specification based on new constitution