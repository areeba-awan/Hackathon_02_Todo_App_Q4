---
id: 002
title: AI Chatbot Implementation Plan
stage: plan
date_iso: 2026-02-19
surface: agent
model: Qwen Code
feature: 003-ai-chatbot-cohere
branch: 003-ai-chatbot-cohere
user: Areeba awan
command: /sp.plan
labels:
  - ai-chatbot
  - cohere
  - plan
  - phase-iii
  - implementation
links:
  spec: specs/003-ai-chatbot-cohere/spec.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/003-ai-chatbot-cohere/plan.md
  - specs/003-ai-chatbot-cohere/research.md
  - specs/003-ai-chatbot-cohere/data-model.md
  - specs/003-ai-chatbot-cohere/quickstart.md
  - specs/003-ai-chatbot-cohere/contracts/chat-api.yaml
  - specs/003-ai-chatbot-cohere/contracts/mcp-tools.yaml
tests_yaml: []
---

# AI Chatbot Implementation Plan

## User Input
```
/sp.plan You are creating an implementation plan for integrating an AI-powered Todo Chatbot into an existing full-stack Todo application.

The system already includes:
- Next.js frontend
- Backend API (Node/Express or FastAPI)
- Neon PostgreSQL
- Better Auth authentication
- RESTful task endpoints

The chatbot must use:
- OpenAI Agents SDK
- Cohere API (instead of Gemini)
- Secure backend tool execution
- Frontend chatbot UI integration

-------------------------------------------------
PHASE 1 – AI INFRASTRUCTURE SETUP
-------------------------------------------------

1. Install required dependencies:
   - agents SDK
   - Cohere SDK (if required)
   - dotenv
   - HTTP client (axios/httpx)

2. Add environment variables:
   COHERE_API_KEY=
   BETTER_AUTH_SECRET=
   NEON_DATABASE_URL=

3. Create backend folder structure:

   /ai
      agent.py (or agent.ts)
      tools.py
      config.py
   /services
   /controllers
   /routes

4. Configure Cohere provider inside Agents SDK:
   - Replace Gemini provider
   - Use COHERE_API_KEY
   - Set temperature 0.3–0.5
   - Enable structured tool calling

-------------------------------------------------
PHASE 2 – TOOL IMPLEMENTATION
-------------------------------------------------

1. Define function tools:
   - add_task
   - list_tasks
   - complete_task
   - delete_task
   - update_task

2. Each tool must:
   - Validate authenticated user
   - Call existing backend service layer
   - Return structured JSON
   - Handle DB errors

3. Ensure tools never:
   - Fabricate task IDs
   - Access cross-user data

-------------------------------------------------
PHASE 3 – CHAT ENDPOINT CREATION
-------------------------------------------------

Create:
POST /api/chat

Flow:

1. Validate Better Auth session
2. Extract user_id
3. Receive user message
4. Pass structured system + user prompt to Cohere
5. Allow tool execution via Agents SDK
6. Execute selected tool
7. Return final assistant response

Response format:

{
  success: boolean,
  message: string,
  data?: object
}

-------------------------------------------------
PHASE 4 – FRONTEND INTEGRATION
-------------------------------------------------

1. Create Chatbot UI Component:
   - Floating button bottom-right
   - Modal opens on click
   - Message list
   - Input field
   - Loading spinner

2. On send:
   - Call POST /api/chat
   - Pass message
   - Include authentication session

3. Display:
   - User message
   - Assistant response
   - Structured task confirmations

-------------------------------------------------
PHASE 5 – SECURITY HARDENING
-------------------------------------------------

- Ensure no frontend access to Cohere API
- Protect environment variables
- Validate user session before tool calls
- Prevent cross-user task access
- Sanitize all inputs

-------------------------------------------------
PHASE 6 – ERROR HANDLING
-------------------------------------------------

Handle:

- Invalid task ID
- Empty task list
- Unauthorized access
- Cohere API failure
- Tool execution failure
- Database timeout

Return structured error JSON.

-------------------------------------------------
PHASE 7 – TESTING & VALIDATION
-------------------------------------------------

Test cases:

- Add task via chatbot
- List tasks
- Complete task
- Delete task
- Update task
- Unauthorized user attempt
- Multiple user isolation

Ensure:
- No hallucinated responses
- Correct DB persistence
- Proper frontend updates

-------------------------------------------------
FINAL DELIVERABLE
-------------------------------------------------

A production-ready AI Todo Chatbot that:

- Uses Cohere via Agents SDK
- Integrates securely with backend
- Uses existing database
- Is fully authenticated
- Is accessible via chatbot UI icon
- Is modular and scalable
- Is hackathon-grade clean architecture
```

## Response snapshot
Created comprehensive implementation plan with Phase 0-1 design artifacts including research decisions, data model, API contracts, and quickstart guide. Plan defines 7-phase implementation approach for AI chatbot integration with Cohere API and OpenAI Agents SDK.

## Outcome

- ✅ Impact: Implementation plan ready with all Phase 0-1 artifacts
- 🧪 Tests: Constitution check passed (all 12 principles verified)
- 📁 Files: 6 created (plan.md, research.md, data-model.md, quickstart.md, chat-api.yaml, mcp-tools.yaml)
- 🔁 Next prompts: Run /sp.tasks to generate implementation task list
- 🧠 Reflection: Plan maintains Phase-II security while adding Phase-III AI capabilities

## Evaluation notes (flywheel)

- Failure modes observed: None - plan aligned with constitution from start
- Graders run and results (PASS/FAIL): PASS - Constitution check verified (12/12 principles)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.tasks for implementation breakdown

## Plan Summary

**Branch**: `003-ai-chatbot-cohere`
**Plan File**: `specs/003-ai-chatbot-cohere/plan.md`

### Phase 0: Research (Complete)
✅ Cohere API integration pattern decided
✅ Conversation history schema designed
✅ Intent detection approach selected
✅ Security best practices defined
✅ Error handling strategy documented
✅ Temperature settings specified
✅ MCP tool implementation pattern established

### Phase 1: Design (Complete)
✅ Data model created (Conversation, Message entities)
✅ API contracts generated (OpenAPI YAML)
✅ MCP tool definitions specified
✅ Quickstart guide written
✅ Database schema with indexes defined
✅ Migration strategy outlined

### Phase 2+: Implementation (Ready for /sp.tasks)

**7 Phases Planned**:
1. AI Infrastructure Setup (dependencies, env vars, folder structure)
2. Tool Implementation (5 MCP tools: add_task, list_tasks, complete_task, delete_task, update_task)
3. Chat Endpoint Creation (POST /api/chat with auth validation)
4. Frontend Integration (ChatbotIcon, ChatModal, MessageList, MessageInput)
5. Security Hardening (input sanitization, rate limiting, session validation)
6. Error Handling (structured JSON responses for all failure modes)
7. Testing & Validation (unit, integration, E2E tests)

### Constitution Compliance

✅ All 12 constitution principles verified:
- Sequential process adherence
- Process integrity
- No manual coding
- Spec-first changes
- Phase boundaries respected
- Authentication requirements
- Data persistence rules
- Spec documentation
- Agent constraints
- AI security rules
- MCP tool skills pattern
- AI response rules

**Plan Ready**: Yes  
**Next Command**: `/sp.tasks`
