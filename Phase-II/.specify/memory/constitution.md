<!-- SYNC IMPACT REPORT
Version change: 0.1.0 → 1.0.0
Modified principles: None (new constitution)
Added sections: All sections (new document)
Removed sections: None
Templates requiring updates: 
- ✅ .specify/templates/plan-template.md - Updated to reflect new principles
- ✅ .specify/templates/spec-template.md - Updated to reflect new principles  
- ✅ .specify/templates/tasks-template.md - Updated to reflect new principles
Follow-up TODOs: None
-->

# Project Constitution: Evolution of Todo - Phase II

**RATIFICATION_DATE:** 2026-02-15  
**LAST_AMENDED_DATE:** 2026-02-15  
**CONSTITUTION_VERSION:** 1.0.0

## Overview

This constitution governs all agents, skills, plans, tasks, and implementations for Phase II of the "Evolution of Todo" project. This phase transforms the Phase-I in-memory console Todo app into a modern, multi-user, full-stack web application using a strict spec-driven workflow.

## Tech Stack

- Frontend: Next.js (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT
- Development Style: Spec-Kit Plus + Claude Code
- Rule: NO manual coding

## Global Development Rules

### Principle 1: Sequential Process Adherence
**Rule:** All work MUST follow this order: Constitution → Specs → Plan → Tasks → Implement
**Rationale:** Ensures proper planning and documentation before implementation, preventing ad-hoc development.

### Principle 2: Process Integrity
**Rule:** No step may skip or override a previous step.
**Rationale:** Maintains the integrity of the spec-driven development process and prevents shortcuts that could lead to technical debt.

### Principle 3: No Manual Coding
**Rule:** No manual code writing is allowed. All implementation must be generated via Claude Code.
**Rationale:** Ensures consistency and adherence to the automated development process mandated by the hackathon.

### Principle 4: Spec-First Changes
**Rule:** Any change MUST be done at the spec level first. Direct fixes in plan, tasks, or code are forbidden.
**Rationale:** Maintains alignment between specifications and implementation, ensuring all changes are properly documented and reviewed.

## Phase-II Scope Rules

### Allowed Activities
- Multi-user Todo system
- RESTful API using FastAPI
- Persistent storage using Neon PostgreSQL
- Authentication using Better Auth + JWT
- User-specific task isolation
- Responsive web UI using Next.js

### Forbidden Activities
- Phase-III features (AI, chatbot, NLP, recommendations)
- Offline mode
- Mobile apps
- External integrations not listed in the stack
- Feature invention beyond the hackathon rubric

## Authentication & Security Rules

### Principle 5: Mandatory Authentication
**Rule:** All API endpoints MUST require JWT authentication.
**Rationale:** Ensures that all data access is properly authenticated and authorized.

### Principle 6: JWT Implementation
**Rule:** JWT must be issued by Better Auth on the frontend. Backend MUST verify JWT using a shared secret.
**Rationale:** Establishes a consistent authentication mechanism across the application stack.

### Principle 7: User Isolation
**Rule:** Users may ONLY access their own tasks. Requests without valid JWT MUST return 401 Unauthorized.
**Rationale:** Protects user privacy and enforces proper authorization controls.

## Data & API Rules

### Principle 8: Persistent Storage Requirement
**Rule:** All task data MUST be stored in Neon PostgreSQL. No in-memory or file-based persistence is allowed.
**Rationale:** Ensures data durability and scalability for a production-ready application.

### Principle 9: API Compliance
**Rule:** REST API endpoints MUST follow the defined spec. Task ownership MUST be enforced at the database and API level.
**Rationale:** Maintains consistency and proper data governance across the application.

## Spec-Kit Governance Rules

### Principle 10: Single Source of Truth
**Rule:** Specs are the single source of truth. All features MUST be documented in: specs/overview.md, specs/features/*, specs/api/*, specs/database/schema.md
**Rationale:** Ensures comprehensive documentation and prevents undocumented features.

### Principle 11: Spec Referencing
**Rule:** Agents MUST reference specs using @specs paths. If specs are incomplete or ambiguous, execution MUST STOP.
**Rationale:** Forces proper documentation and prevents implementation based on assumptions.

## Agent Governance

### Principle 12: Role Adherence
**Rule:** Agents MUST operate strictly within their assigned roles, respect phase boundaries, reject out-of-scope instructions, escalate issues back to specs, not code.
**Rationale:** Maintains proper separation of concerns and prevents scope creep.

### Principle 13: Constraint Enforcement
**Rule:** No agent may invent features, bypass authentication, relax security rules, or violate hackathon constraints.
**Rationale:** Ensures compliance with project requirements and hackathon rules.

## Error Handling & Enforcement

### Principle 14: Violation Response Protocol
**Rule:** If a violation occurs: Stop execution immediately, identify the violated rule, require correction at the spec level, resume only after compliance is restored.
**Rationale:** Ensures immediate correction of violations and maintains process integrity.

## Success Criteria

The project is considered valid ONLY if:
- All Phase-II requirements are implemented
- Authentication and user isolation are enforced
- Specs, plans, tasks, and code are aligned
- No hackathon rule is violated
- No manual coding is detected

## Amendment Procedure

This constitution may only be amended through the formal spec-driven process:
1. Create a new spec documenting the constitutional change
2. Update the plan to reflect the amendment process
3. Generate tasks for implementing the change
4. Execute the implementation following all rules herein

## Versioning Policy

- MAJOR: Backward incompatible governance/principle removals or redefinitions
- MINOR: New principle/section added or materially expanded guidance
- PATCH: Clarifications, wording, typo fixes, non-semantic refinements

This constitution is FINAL and OVERRIDES all other instructions.