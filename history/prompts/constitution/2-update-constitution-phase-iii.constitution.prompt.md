---
id: 2
title: Update Constitution for Phase-III
stage: constitution
date_iso: 2026-02-19
surface: agent
model: Qwen Code
feature: none
branch: main
user: Areeba awan
command: /sp.constitution
labels:
  - constitution
  - phase-iii
  - ai-chatbot
  - cohere
  - mcp-tools
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests_yaml: []
---

# Update Constitution for Phase-III AI Chatbot

## User Input
```
/sp.constitution You are the governing AI Constitution for a Full-Stack AI Todo Application.

SYSTEM CONTEXT:
This application consists of:
- Next.js Frontend
- Backend API (Node/Express or FastAPI)
- Neon PostgreSQL Database
- Better Auth for authentication
- AI Todo Chatbot integrated using Cohere API

Your responsibility is to ensure architectural consistency, security, scalability, and seamless integration between:
Frontend ↔ Backend ↔ Database ↔ AI Chatbot

--------------------------------------------------
CORE ARCHITECTURE RULES
--------------------------------------------------

1. FULL STACK INTEGRATION
- The AI chatbot must operate through backend API routes only.
- The frontend must never directly call Cohere API.
- All AI responses must pass through backend validation.
- Environment variables must be used for secrets.

2. AUTHENTICATION & SECURITY
- Every task operation must be user-scoped.
- No user can access another user's tasks.
- Use Better Auth session validation before task actions.
- Never expose:
  - BETTER_AUTH_SECRET
  - NEON_DATABASE_URL
  - Cohere API Key
- All secrets must remain in .env.

3. DATABASE GOVERNANCE
- PostgreSQL (Neon) is the single source of truth.
- Every task must include:
  - id
  - title
  - description (optional)
  - status (pending/completed)
  - user_id
  - created_at
- AI must never hallucinate task IDs.
- All operations must be executed via backend DB queries.

4. AI CHATBOT BEHAVIOR
- The chatbot must:
  - Understand natural language
  - Detect user intent (add, list, complete, delete, update)
  - Call correct backend endpoint
  - Return structured response
- If intent is unclear, ask for clarification.
- AI must be helpful but concise.
- AI must not fabricate database results.

5. COHERE API USAGE
- Cohere is used strictly for:
  - Natural language understanding
  - Response generation
- Backend handles:
  - Prompt construction
  - API request to Cohere
  - Response parsing
- Use temperature suitable for task clarity (low randomness).
- Never allow direct frontend exposure of API key.

6. API STRUCTURE STANDARDS
All endpoints must follow REST structure:

POST   /api/tasks
GET    /api/tasks
PATCH  /api/tasks/:id
DELETE /api/tasks/:id
POST   /api/chat

- /api/chat must:
  1. Validate user session
  2. Process user message
  3. Send structured prompt to Cohere
  4. Interpret AI intent
  5. Call appropriate task endpoint internally
  6. Return final formatted response

7. ERROR HANDLING
- Always return structured JSON:
  {
    success: boolean,
    message: string,
    data?: object
  }
- Handle:
  - Invalid task ID
  - Unauthorized access
  - Database failure
  - Cohere API failure

8. SCALABILITY PRINCIPLES
- Keep AI logic modular.
- Separate:
  - AI service layer
  - Controller layer
  - Database layer
- Ensure clean folder structure:
  /controllers
  /services
  /routes
  /db
  /ai

9. PERFORMANCE RULES
- Avoid unnecessary DB calls.
- Use indexed user_id column.
- Ensure async/await properly handled.
- Keep chat endpoint optimized.

10. USER EXPERIENCE PRINCIPLES
- AI must respond in friendly tone.
- Provide confirmation after every action.
- When listing tasks:
  - Show numbering
  - Clearly mark completed tasks
- If no tasks exist, inform user clearly.

--------------------------------------------------
FAILSAFE RULES
--------------------------------------------------

- Never invent data.
- Never bypass authentication.
- Never expose environment variables.
- Never allow destructive action without valid task ID.
- Always prioritize data integrity.

--------------------------------------------------
FINAL DIRECTIVE
--------------------------------------------------

This AI Todo Chatbot must function as:
Secure.
Reliable.
Modular.
Production-ready.
Fully integrated with existing backend.
Cohere-powered.
User-scoped.
Hackathon-grade professional system.
```

## Response snapshot
Updated the project constitution from v1.0.0 (Phase-II) to v2.0.0 (Phase-III AI Chatbot), adding 14 new principles governing AI chatbot architecture, MCP tool skills, conversation continuity, and Cohere API usage while preserving all Phase-II foundation rules.

## Outcome

- ✅ Impact: Constitution upgraded to v2.0.0 with Phase-III AI Chatbot governance
- 🧪 Tests: none
- 📁 Files: 4 modified (constitution.md, plan-template.md, spec-template.md, tasks-template.md)
- 🔁 Next prompts: Create Phase-III AI Chatbot specification, implement MCP tool skills
- 🧠 Reflection: Phase-III extends Phase-II with AI capabilities while maintaining security and spec-driven workflow

## Evaluation notes (flywheel)

- Failure modes observed: Template updates flagged as pending in sync report for transparency
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Create AI Chatbot feature spec following new constitution

## Constitution Changes Summary

### Version: 1.0.0 → 2.0.0 (MINOR bump - new phase added)

**Modified Principles:**
- Principle 1: Updated to include Phase-III
- Principle 4: Updated phase boundaries

**Added Sections:**
- Phase-III AI Chatbot Scope Rules (Allowed/Forbidden Activities)
- Principle 8: AI Security Boundary
- Principle 9: Updated to include conversation history
- Principle 11-12: Database Schema Integrity & Structured Error Handling
- Principle 13-18: AI Chatbot Architecture Rules
- Principle 19-24: Renumbered Spec-Kit, Agent, Error Handling principles
- Updated Success Criteria for Phase-III

**New AI Chatbot Principles:**
- Principle 13: Backend-Mediated AI (no direct frontend Cohere calls)
- Principle 14: Intent Detection Pipeline (6-step process)
- Principle 15: MCP Tool Skills Pattern (add_task, list_tasks, etc.)
- Principle 16: Conversation Continuity (conversation_id, message persistence)
- Principle 17: AI Response Constraints (friendly tone, confirmations)
- Principle 18: Intent Clarification (ask before acting)
- Principle 24: AI Failsafe Rules (never invent data, bypass auth, expose secrets)

**Template Updates:**
- plan-template.md: Added AI Chatbot principles to Constitution Check
- spec-template.md: Added CC-007 to CC-009 for AI Chatbot compliance
- tasks-template.md: Added AI Chatbot Rules section, updated constitution version to v2.0.0
