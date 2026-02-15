---
id: "002"
title: "Create Intermediate Constitution Supplement"
stage: "constitution"
date: "2026-01-06"
surface: "agent"
model: "sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "Human"
command: "/sp.constitution"
labels: ["constitution","phase-governance","phase-II"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - ".specify/memory/constitution-intermediate.md"
  - ".specify/memory/constitution.md"
tests: []
---

## Prompt

Create a dedicated constitution supplement for the Intermediate Level of the "Evolution of Todo" project, building directly upon the existing global constitution (dated 2026-01-02) and focusing exclusively on integrating and governing the intermediate features: Priorities & Tags/Categories, Search & Filter, and Sort Tasks. This must align with Phase II (Full-Stack Web Application) transition from Phase I's in-memory Python console app.

This intermediate constitution supplement must strictly enforce and extend the global principles:

**Spec-Driven Development (mandatory extension)**
No code changes or additions without updated specs approved via /sp.specify, following: Global Constitution → Intermediate Specs Update → Plan Revision → Tasks → Implement
All intermediate work must reference and extend the basic task model (add fields like priority enum: high/medium/low, tags: list of strings, without breaking existing CRUD operations)

**Agent Behavior Rules (reinforced)**
Humans/agents cannot manually code or invent beyond specified intermediate features
Refinements (e.g., filter logic) must happen at spec level; no code-level hacks
Ensure no leakage of advanced features (e.g., no recurring tasks or reminders here)

**Phase Governance for Intermediate (Phase II scoped)**
Scope limited to:
- Priorities: Assign high/medium/low to tasks
- Tags/Categories: User-assignable labels (e.g., work/home/personal)
- Search: Keyword-based on title/description
- Filter: By status (complete/incomplete), priority, tag, date range
- Sort: By due date, priority level, alphabetical title

Integrate with basic features (add/update/view/delete/mark complete) in web UI
Architecture evolution: Shift from in-memory to persistent DB (SQLModel/Neon), backend FastAPI APIs, frontend Next.js for interactive list/search UI
No future-phase tech (e.g., no Kafka or Kubernetes yet)

**Technology Constraints (Phase II specific)**
Backend: Python/FastAPI/SQLModel for APIs (endpoints for filter/sort/search)
Frontend: Next.js for dynamic UI (task list with filters, sortable table)
DB: Extend schema for priority (enum/string), tags (JSON/array field)
Agents: Use OpenAI Agents SDK/MCP for any spec generation, but no AI in runtime app yet (save for Phase III)

**Quality Principles (applied to intermediate)**
Maintain clean architecture: Separate concerns (API routes, DB models, frontend components)
Stateless APIs where possible; use Neon DB for persistence
Ensure responsive web UI, basic validation (e.g., valid priority values)
Observability: Add logging for search/filter operations

This supplement must remain compatible with the global constitution as the supreme document, act as an addendum for Phase II governance, and be stored/updated in .specify/memory/constitution-intermediate.md or similar. Include amendment process tied to global rules.
Enforce phase transition: Intermediate features must be fully spec'd, tested in web context, before advancing to AI chatbot in Phase III.

## Response snapshot

Created `.specify/memory/constitution-intermediate.md` as a Phase II governance supplement. This document:
- Extends Spec-Driven Development workflow for intermediate features
- Reinforces agent behavior rules (no feature invention beyond scope)
- Defines Phase II feature scope (priorities, tags, search, filter, sort)
- Specifies technology constraints (FastAPI, SQLModel, Neon DB, Next.js)
- Prohibits future-phase tech (Kafka, Kubernetes, AI runtime)
- Adds observability requirements for search/filter/sort operations
- Includes phase transition requirements (I→II and II→III)
- Updated global constitution to v1.1.0 with supplement reference

## Outcome

- ✅ Impact: Created Phase II constitution supplement governing intermediate features; updated global constitution version and amendment process
- 📁 Files: 2 files modified/created (.specify/memory/constitution.md, .specify/memory/constitution-intermediate.md)
- 🔁 Next prompts: Create intermediate feature specifications via /sp.specify
- 🧠 Reflection: Constitution supplement approach keeps global document clean while providing phase-specific governance. Templates verified compatible with new rules.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Consider creating phase-specific checklist template aligned with intermediate constitution rules
