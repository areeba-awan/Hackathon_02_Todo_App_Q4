---
id: 001
title: AI Chatbot Cohere Integration Spec
stage: spec
date_iso: 2026-02-19
surface: agent
model: Qwen Code
feature: 003-ai-chatbot-cohere
branch: 003-ai-chatbot-cohere
user: Areeba awan
command: /sp.specify
labels:
  - ai-chatbot
  - cohere
  - spec
  - phase-iii
  - nlp
links:
  spec: specs/003-ai-chatbot-cohere/spec.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/003-ai-chatbot-cohere/spec.md
  - specs/003-ai-chatbot-cohere/checklists/requirements.md
tests_yaml: []
---

# AI Chatbot Cohere Integration Specification

## User Input
```
/sp.specify You are defining the technical specification for integrating an AI Todo Chatbot into an existing full-stack Todo application. PROJECT CONTEXT --------------- The application stack includes: Frontend: - Next.js (App Router) - Tailwind CSS - Authenticated UI - Floating Chatbot Icon in bottom-right corner Backend: - Node.js / Express or FastAPI - Neon PostgreSQL database - Better Auth authentication - REST API structure - .env for secrets AI Layer: - OpenAI Agents SDK - Currently Gemini example code - Must migrate to Cohere API - AI used for natural language task management ----------------------------------------- OBJECTIVE ----------------------------------------- Replace Gemini provider with Cohere in OpenAI Agents SDK and fully integrate AI chatbot with backend + frontend. ----------------------------------------- AI ARCHITECTURE REQUIREMENTS ----------------------------------------- 1. MODEL PROVIDER CHANGE - Remove Gemini base_url. - Replace AsyncOpenAI provider with Cohere-compatible OpenAI endpoint. - Use Cohere API key from .env: COHERE_API_KEY=your_key_here - Ensure backend securely loads: os.getenv("COHERE_API_KEY") - No API key exposure in frontend. 2. AGENT DESIGN Create a single primary agent: Agent Name: todo-chatbot-agent Responsibilities: - Understand natural language - Detect intent: add_task list_tasks complete_task delete_task update_task - Call backend APIs internally - Return structured JSON responses Agent must: - Never hallucinate task IDs - Never fabricate DB data - Always rely on backend responses 3. FUNCTION TOOLS Define structured tools: add_task(title: str, description: str | None) list_tasks(filter: str) complete_task(task_id: int) delete_task(task_id: int) update_task(task_id: int, title?: str, description?: str) Each tool: - Calls backend REST endpoint - Returns real DB response 4. BACKEND CHAT ENDPOINT Create: POST /api/chat Flow: 1. Validate Better Auth session 2. Extract user_id 3. Send structured system prompt + user message to Cohere 4. Allow tool calling via Agents SDK 5. Execute selected function_tool 6. Return formatted assistant response Response format: { success: true, message: "Task added successfully.", data: {...} } 5. FRONTEND INTEGRATION UI Requirements: - Floating chatbot icon bottom-right - Click → Opens chat modal - Message history displayed - Input box at bottom - Loading state indicator - Calls POST /api/chat Frontend must: - Never call Cohere directly - Always call backend - Send credentials (auth session) 6. DATABASE INTEGRATION All tasks must contain: - id - title - description - status - user_id - created_at AI must operate only within user scope. 7. ERROR HANDLING Handle: - Invalid task ID - Unauthorized access - Empty task list - Cohere API failure - Tool execution errors Return structured error JSON. 8. CLEAN ARCHITECTURE Backend structure: /routes /controllers /services /ai /tools /db Separate: - AI logic - DB logic - Route handling 9. PERFORMANCE RULES - Async execution required - Avoid duplicate DB queries - Keep Cohere temperature low (0.3–0.5) - Ensure fast response time 10. SECURITY RULES - Never expose: COHERE_API_KEY BETTER_AUTH_SECRET NEON_DATABASE_URL - Always validate session before tool execution - Prevent cross-user data access ----------------------------------------- EXPECTED OUTCOME ----------------------------------------- A fully working AI Todo Chatbot that: - Uses Cohere instead of Gemini - Is integrated with OpenAI Agents SDK - Can call backend tools - Is authenticated - Is database-connected - Is accessible via frontend chatbot icon - Is production-ready - Is hackathon-grade clean architecture
```

## Response snapshot
Created comprehensive feature specification for AI Chatbot integration with Cohere, including 6 user stories (natural language task operations + chat interface), 25 functional requirements, 9 constitution compliance requirements, and 7 measurable success criteria. Specification passed all quality validation checks with zero NEEDS CLARIFICATION markers.

## Outcome

- ✅ Impact: Feature specification ready for technical planning phase
- 🧪 Tests: Specification quality checklist created and passed
- 📁 Files: 2 created (spec.md, checklists/requirements.md)
- 🔁 Next prompts: Run /sp.plan to create technical implementation plan
- 🧠 Reflection: Specification focused on user value and business needs, avoided implementation details

## Evaluation notes (flywheel)

- Failure modes observed: None - specification was clear and complete
- Graders run and results (PASS/FAIL): PASS - all 16 checklist items passed
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.plan for technical architecture

## Specification Summary

**Branch**: `001-ai-chatbot-cohere`
**Spec File**: `specs/001-ai-chatbot-cohere/spec.md`

**User Stories (6 total):**
1. Natural Language Task Creation (P1) - Core value proposition
2. Natural Language Task Listing (P1) - Task retrieval
3. Natural Language Task Completion (P2) - Hands-free completion
4. Natural Language Task Deletion (P2) - Conversational cleanup
5. Natural Language Task Update (P3) - Flexible modifications
6. Conversational Chat Interface (P1) - Primary UI

**Key Requirements:**
- 25 Functional Requirements (FR-001 to FR-025)
- 9 Constitution Compliance Requirements (CC-001 to CC-009)
- 4 Key Entities: User, Task, Conversation, Message
- 7 Measurable Success Criteria (SC-001 to SC-007)

**Security Rules:**
- Frontend NEVER calls Cohere directly
- API keys NEVER exposed
- AI NEVER hallucinates task data
- All operations user-scoped with JWT authentication
