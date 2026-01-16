---
id: 1
title: AI Todo Chatbot Integration
stage: spec
date: 2026-01-15
surface: agent
model: Claude Sonnet 4.5
feature: 001-ai-chatbot-integration
branch: 001-ai-chatbot-integration
user: claude
command: sp.specify
labels: [ai, chatbot, todo, natural-language, cohere]
links:
  spec: ../specs/001-ai-chatbot-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-ai-chatbot-integration/spec.md
 - specs/001-ai-chatbot-integration/checklists/requirements.md
tests:
 - none
---

## Prompt

```text
AI Todo Chatbot Integration for The Evolution of Todo - Phase III: Full-Stack Web Application

**Target audience:** Hackathon judges seeking groundbreaking, production-grade AI integrations; developers building flagship intelligent productivity apps; and AI agents delivering flawless execution via Claude Code.

**Focus:** Define exhaustive, zero-ambiguity, flagship-level specifications for integrating a powerful, natural-language AI Todo Chatbot into the existing full-stack application (Next.js frontend + FastAPI backend + Neon DB + Better Auth). The chatbot must have full control over all core task operations (add, delete, update, mark complete, list) and user information (e.g., "Who am I?" -> reply with logged-in email), using Cohere API (not OpenAI/Gemini) for all AI reasoning and tool calling. Adapt agent-style logic from the provided OpenAI Agents SDK example to Cohere's chat/completions endpoint.

The chatbot UI must be beautifully integrated into the existing premium frontend with a floating chatbot icon/button that opens a stunning, responsive chat panel—maintaining visual harmony with the flagship UI.

**Success Criteria:**
- Delivers a truly intelligent, delightful chatbot that feels like a personal AI assistant—understanding natural language perfectly, confirming actions, handling errors gracefully, and providing rich responses.
- Achieves seamless, secure integration: single stateless POST `/api/{user_id}/chat` endpoint in existing FastAPI backend, Cohere-powered reasoning with tool calling, full conversation persistence in Neon DB.
- Adapts the provided OpenAI Agents SDK example code to Cohere API: use Cohere chat endpoint with structured prompt engineering for step-by-step reasoning and JSON tool call output.
- Exposes 5 MCP-style tools (`add_task`, `delete_task`, `update_task`, `complete_task`, `list_tasks`) + 1 bonus tool (`get_current_user`) that returns logged-in email.
- Integrates a beautiful chatbot UI in frontend: floating circular button (bottom-right, premium glassmorphic style), slide-in/full-panel chat window, message bubbles matching theme, typing indicators, send button with SVG.
- Ensures perfect multi-user isolation: JWT auth → user_id/email extraction → all tools and conversation history scoped to user.
- Generates a complete Markdown file (`vl_chatbot.spec.md`) in `specs/features/` and `specs/api/`—so comprehensive that agents can implement a world-class, production-ready AI chatbot with zero ambiguity.

**Resulting Experience:** Users can manage their entire todo list conversationally while enjoying the flagship visual design.

**Constraints:**
- **Format:** Markdown with ultra-structured sections (Metadata, Chatbot Vision & User Experience, Cohere API Adaptation Strategy, MCP-Style Tools Specification, Database Extensions for Conversations, Backend Chat Endpoint, Frontend Chatbot UI Integration, Natural Language Examples & Flows, Security & User Isolation, Error Handling & Confirmations, TypeScript/Frontend Types, Acceptance Criteria, Detailed Wireframes & Interaction Flows).
- **Version:** v1.0 (include current date: January 06, 2026)
- **AI Provider:** Cohere API only (via `COHERE_API_KEY`) — no OpenAI, Gemini, or other models.
- **Tools:** Adept agent logic using Cohere chat completions; prompts crafted to reason step-by-step, output structured JSON for tool calls, parse and execute.
- **Dependencies:** Existing stack + Cohere Python library; no OpenAI Agents SDK.
- **Frontend Integration:** Add chatbot trigger button (floating option, premium design), beautiful chat panel (glassmorphic, themed bubbles, scrollable history), real-time message streaming if possible.
- **Stateless Backend:** No server-held conversation state — persist everything in DB (`Conversation` + `Message` models). Use async operations throughout backend.
- **Specs Length:** Keep visionary yet surgically implementable (under 4000 words).

**Specific Requirements:**

1. **Cohere API Adaptation**
   - Replace OpenAI Agents SDK with direct Cohere chat calls.
   - Prompt engineering: instruct Cohere to think step-by-step, identify intent, output JSON tool call if needed, or respond directly.
   - Parse Cohere response for tool invocation (JSON block), execute tool, feed result back if multi-step needed.

2. **MCP-Style Tools (6 total)**
   - `add_task`, `delete_task`, `update_task`, `complete_task`, `list_tasks`
   - `get_current_user` → returns `{ "email": str, "user_id": str }`

3. **Database Extensions**
   - `Conversation`: id, user_id, created_at
   - `Message`: id, conversation_id, role ("user"/"assistant"), content, created_at

4. **Backend Endpoint**
   - POST `/api/{user_id}/chat`
   - Body: `{ conversation_id (optional), message: str }`
   - Response: `{ conversation_id, response: str, tool_calls: array (optional) }`

5. **Frontend UI**
   - Floating chatbot button (bottom-right, emerald accent, subtle pulse animation)
   - Slide-in chat panel (glassmorphic card, dark/light theme aware)
   - Message bubbles: user (right,
```

## Response snapshot

Created comprehensive specification for the AI Todo Chatbot Integration (Phase III). The specification includes:

- Detailed user scenarios and testing requirements
- Cohere API adaptation strategy to replace OpenAI dependencies
- MCP-style tools specification for the 6 required tools
- Database extension requirements for Conversation and Message models
- Backend endpoint design for the stateless chat API
- Frontend UI integration with floating button and glassmorphic design
- Natural language processing examples and flows
- Security and user isolation requirements
- Error handling and confirmation strategies
- TypeScript type definitions for frontend
- Acceptance criteria and measurable success outcomes

The specification is ready for the planning phase and contains all necessary information for implementation.

## Outcome

- ✅ Impact: Created comprehensive spec for AI chatbot integration with all required sections
- 🧪 Tests: none
- 📁 Files: Created spec.md and requirements checklist in specs/001-ai-chatbot-integration/
- 🔁 Next prompts: Ready for /sp.plan to create implementation plan
- 🧠 Reflection: Specification covers all aspects of the AI chatbot integration with clear requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All required sections implemented
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin planning phase with /sp.plan