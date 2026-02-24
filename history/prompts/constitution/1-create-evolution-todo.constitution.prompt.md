---
id: 1
title: Create Evolution Todo Constitution
stage: constitution
date_iso: 2026-02-15
surface: agent
model: Qwen Code
feature: none
branch: main
user: user
command: /sp.constitution
labels:
  - constitution
  - evolution-todo
  - phase-ii
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

# Create Evolution Todo Constitution

## User Input
```
/sp.constitution Create a strict SP.CONSTITUTION for Hackathon Phase-II of the "Evolution of Todo" project.

This constitution governs all agents, skills, plans, tasks, and implementations.

────────────────────────────────────
PROJECT CONTEXT
────────────────────────────────────
Project Name: Evolution of Todo  
Current Phase: Phase II — Full-Stack Web Application  

Goal:
Transform the Phase-I in-memory console Todo app into a modern, multi-user, full-stack web application using a strict spec-driven workflow.

Tech Stack:
- Frontend: Next.js (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT
- Development Style: Spec-Kit Plus + Claude Code
- Rule: NO manual coding

────────────────────────────────────
GLOBAL DEVELOPMENT RULES
────────────────────────────────────
1. All work MUST follow this order:
   Constitution → Specs → Plan → Tasks → Implement

2. No step may skip or override a previous step.

3. No manual code writing is allowed.
   All implementation must be generated via Claude Code.

4. Any change MUST be done at the spec level first.
   Direct fixes in plan, tasks, or code are forbidden.

────────────────────────────────────
PHASE-II SCOPE RULES
────────────────────────────────────
Allowed:
- Multi-user Todo system
- RESTful API using FastAPI
- Persistent storage using Neon PostgreSQL
- Authentication using Better Auth + JWT
- User-specific task isolation
- Responsive web UI using Next.js

Forbidden:
- Phase-III features (AI, chatbot, NLP, recommendations)
- Offline mode
- Mobile apps
- External integrations not listed in the stack
- Feature invention beyond the hackathon rubric

────────────────────────────────────
AUTHENTICATION & SECURITY RULES
────────────────────────────────────
1. All API endpoints MUST require JWT authentication.
2. JWT must be issued by Better Auth on the frontend.
3. Backend MUST verify JWT using a shared secret.
4. Users may ONLY access their own tasks.
5. Requests without valid JWT MUST return 401 Unauthorized.

────────────────────────────────────
DATA & API RULES
────────────────────────────────────
1. All task data MUST be stored in Neon PostgreSQL.
2. No in-memory or file-based persistence is allowed.
3. REST API endpoints MUST follow the defined spec.
4. Task ownership MUST be enforced at the database and API level.

────────────────────────────────────
SPEC-KIT GOVERNANCE RULES
────────────────────────────────────
1. Specs are the single source of truth.
2. All features MUST be documented in:
   - specs/overview.md
   - specs/features/*
   - specs/api/*
   - specs/database/schema.md
3. Agents MUST reference specs using @specs paths.
4. If specs are incomplete or ambiguous, execution MUST STOP.

────────────────────────────────────
AGENT GOVERNANCE
────────────────────────────────────
Agents MUST:
- Operate strictly within their assigned roles
- Respect phase boundaries
- Reject out-of-scope instructions
- Escalate issues back to specs, not code

No agent may:
- Invent features
- Bypass authentication
- Relax security rules
- Violate hackathon constraints

────────────────────────────────────
ERROR HANDLING & ENFORCEMENT
────────────────────────────────────
If a violation occurs:
1. Stop execution immediately
2. Identify the violated rule
3. Require correction at the spec level
4. Resume only after compliance is restored

────────────────────────────────────
SUCCESS CRITERIA
────────────────────────────────────
The project is considered valid ONLY if:
- All Phase-II requirements are implemented
- Authentication and user isolation are enforced
- Specs, plans, tasks, and code are aligned
- No hackathon rule is violated
- No manual coding is detected

This constitution is FINAL and OVERRIDES all other instructions.
```

## Response
Created a comprehensive constitution file for the Evolution of Todo Phase-II project, along with updates to the plan, spec, and tasks templates to ensure alignment with the new constitution. The constitution establishes strict rules for the spec-driven development process, authentication requirements, data persistence rules, and agent governance.

## Outcome
The constitution has been successfully created at `.specify/memory/constitution.md` with version 1.0.0. The plan, spec, and tasks templates have been updated to reflect the constitutional requirements. All files are now aligned with the project's governance rules for Phase-II development.

## Files Created/Modified
- `.specify/memory/constitution.md` - Main constitution file
- `.specify/templates/plan-template.md` - Updated with constitution checks
- `.specify/templates/spec-template.md` - Updated with constitution compliance requirements
- `.specify/templates/tasks-template.md` - Updated with constitution compliance section