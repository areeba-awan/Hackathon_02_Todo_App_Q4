---
feature: "Backend API for Todo App"
branch: "002-backend-specs"
created: "2026-02-17"
status: "Draft"
input: "Backend implementation tasks for FastAPI todo app"
constitution_compliance: "All features must comply with project constitution v1.0.0"
---

# Implementation Tasks: Backend API for Todo App

**Feature Branch**: `002-backend-specs`
**Created**: 2026-02-17
**Status**: Draft
**Input**: Backend implementation tasks for FastAPI todo app
**Constitution Compliance**: All features must comply with project constitution v1.0.0

---

## Overview

This document breaks down the backend implementation plan into specific, actionable tasks organized by user story. Each task follows the checklist format and includes exact file paths.

**Total Tasks**: 47
**User Stories**: 3 (US1: Secure Data Access, US2: Task Management, US3: Error Feedback)
**Parallel Opportunities**: 8 tasks marked [P]

---

## Implementation Strategy

### MVP Scope (User Story 1 Only)
- Project setup and structure
- Database connection and Task model
- JWT authentication verification
- GET /api/tasks endpoint (list user's tasks)
- Basic error handling

### Incremental Delivery
1. **Phase 1-2**: Foundation (all stories depend on this)
2. **Phase 3 (US1)**: Secure data access - core authentication + list tasks
3. **Phase 4 (US2)**: Full CRUD operations for task management
4. **Phase 5 (US3)**: Enhanced error handling and validation
5. **Phase 6**: Polish and cross-cutting concerns

---

## Dependencies

```
Phase 1 (Setup) → Phase 2 (Foundation) → Phase 3 (US1) → Phase 4 (US2) → Phase 5 (US3) → Phase 6 (Polish)
```

**User Story Dependencies**:
- US1 (Secure Access): Depends on Phase 2 (auth + DB)
- US2 (Task Management): Depends on US1 completion
- US3 (Error Feedback): Integrated throughout, enhanced in Phase 5

**Parallel Execution Opportunities**:
- Within phases: Tasks marked [P] can run in parallel
- Across stories: US2 and US3 can start independently after US1 foundation

---

## Phase 1: Project Setup

**Purpose**: Initialize backend project structure and tooling

**Tasks**:

- [ ] T001 Create backend directory structure (backend/, backend/routes/)
- [ ] T002 Create requirements.txt with dependencies (fastapi, uvicorn, sqlmodel, psycopg2-binary, PyJWT, python-dotenv)
- [ ] T003 Create .gitignore for Python projects (venv, __pycache__, .env, etc.)
- [ ] T004 Create .env.example template (DATABASE_URL, BETTER_AUTH_SECRET, FRONTEND_URL)
- [ ] T005 [P] Create main.py with basic FastAPI app initialization
- [ ] T006 [P] Create db.py with database connection setup

**Expected Outcome**: Empty project structure ready for implementation

---

## Phase 2: Foundational Layer

**Purpose**: Build blocking prerequisites for all user stories

**Tasks**:

- [ ] T007 Implement database session dependency in db.py (get_session generator)
- [ ] T008 Create models.py with Task SQLModel entity (id, user_id, title, description, completed, created_at, updated_at)
- [ ] T009 Create schemas.py with Pydantic schemas (TaskCreate, TaskUpdate, TaskResponse, TaskListResponse, ErrorResponse)
- [ ] T010 Implement JWT verification dependency in auth.py (get_current_user function)
- [ ] T011 Add constant-time signature comparison using hmac.compare_digest
- [ ] T012 Add clock skew tolerance (60 seconds) to token expiration check
- [ ] T013 Configure CORS middleware in main.py (allow FRONTEND_URL, methods, headers)
- [ ] T014 Create database initialization script to create tasks table

**Expected Outcome**: Reusable dependencies (DB session, auth) and models ready for route implementation

---

## Phase 3: User Story 1 - Secure Task Data Access

**Priority**: P1

**Goal**: Implement authentication and task listing with user isolation

**Independent Test**: Can verify user isolation by attempting to access another user's tasks - must return 404

**Tasks**:

- [ ] T015 [P] [US1] Create routes/tasks.py with APIRouter setup
- [ ] T016 [P] [US1] Import dependencies in routes/tasks.py (get_session, get_current_user, Task, schemas)
- [ ] T017 [US1] Implement GET /api/tasks endpoint (list all tasks for authenticated user)
- [ ] T018 [US1] Add optional completed query parameter filter to GET /api/tasks
- [ ] T019 [US1] Ensure query filters by user_id from authenticated context
- [ ] T020 [US1] Return TaskListResponse with 200 status
- [ ] T021 [US1] Add 401 Unauthorized error response for invalid/missing token
- [ ] T022 [US1] Include routes/tasks.py in main.py app.include_router()

**Expected Outcome**: Users can list their own tasks only, with proper authentication

---

## Phase 4: User Story 2 - Create and Manage Tasks

**Priority**: P1

**Goal**: Implement full CRUD operations for task management

**Independent Test**: Can perform all CRUD operations (create, read, update, delete, toggle complete) and verify data persistence

**Tasks**:

- [ ] T023 [P] [US2] Implement POST /api/tasks endpoint (create new task)
- [ ] T024 [US2] Validate TaskCreate schema (title required, 1-200 chars)
- [ ] T025 [US2] Create task with user_id from auth context, completed=False, timestamps
- [ ] T026 [US2] Return TaskResponse with 201 status
- [ ] T027 [P] [US2] Implement GET /api/tasks/{id} endpoint (get single task)
- [ ] T028 [US2] Query task WHERE id AND user_id match
- [ ] T029 [US2] Return 404 if task not found or belongs to different user
- [ ] T030 [US2] Return TaskResponse with 200 status
- [ ] T031 [P] [US2] Implement PUT /api/tasks/{id} endpoint (full update)
- [ ] T032 [US2] Validate TaskUpdate schema (title, description, completed required)
- [ ] T033 [US2] Update task and updated_at timestamp
- [ ] T034 [US2] Return updated TaskResponse with 200 status
- [ ] T035 [P] [US2] Implement DELETE /api/tasks/{id} endpoint
- [ ] T036 [US2] Verify task ownership before deletion
- [ ] T037 [US2] Return 204 No Content on success
- [ ] T038 [P] [US2] Implement PATCH /api/tasks/{id}/complete endpoint (toggle completion)
- [ ] T039 [US2] Toggle completed boolean (NOT completed)
- [ ] T040 [US2] Update updated_at timestamp
- [ ] T041 [US2] Return updated TaskResponse with 200 status

**Expected Outcome**: Full CRUD operations for task management with user isolation

---

## Phase 5: User Story 3 - Receive Clear Error Feedback

**Priority**: P2

**Goal**: Implement consistent error handling across all endpoints

**Independent Test**: Can trigger various error conditions (invalid token, validation errors, not found) and verify clear error messages

**Tasks**:

- [ ] T042 [P] [US3] Create custom exception handler for HTTPException in main.py
- [ ] T043 [US3] Format errors as {"error": {"code": "...", "message": "...", "details": {...}}}
- [ ] T044 [US3] Map error codes: UNAUTHORIZED (401), NOT_FOUND (404), VALIDATION_ERROR (422)
- [ ] T045 [US3] Add field-specific validation error details for 422 responses
- [ ] T046 [US3] Implement global validation exception handler for Pydantic/SQLModel errors

**Expected Outcome**: Consistent, clear error responses across all endpoints

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final integration, validation, and production readiness

**Tasks**:

- [ ] T047 [P] Test full integration with frontend (CORS, JWT format, response structure)
- [ ] T048 Verify all endpoints require JWT authentication
- [ ] T049 Verify user isolation on all queries (inspect generated SQL)
- [ ] T050 Test concurrent multi-user scenarios (no data leakage)
- [ ] T051 Verify error responses match spec format
- [ ] T052 Create production deployment notes (gunicorn, env vars, HTTPS)
- [ ] T053 Verify constitution compliance (all 14 principles)
- [ ] T054 Update quickstart.md with working examples

**Expected Outcome**: Production-ready backend with all validation checks passed

---

## Task Summary

| Phase | Description | Task Count | Parallel Tasks |
|-------|-------------|------------|----------------|
| Phase 1 | Project Setup | 6 | 2 |
| Phase 2 | Foundational Layer | 8 | 0 |
| Phase 3 | US1: Secure Access | 8 | 2 |
| Phase 4 | US2: Task Management | 19 | 5 |
| Phase 5 | US3: Error Feedback | 5 | 1 |
| Phase 6 | Polish & Validation | 8 | 1 |
| **Total** | | **54** | **11** |

---

## MVP Definition

**Minimum Viable Product** (Phases 1-3 + minimal Phase 4):
- T001-T014: Setup and foundation
- T015-T022: US1 (list tasks with auth)
- T023-T026: US2 (create task only)

**MVP Testable Criteria**:
- User can authenticate via JWT
- User can list their own tasks only
- User can create new tasks
- Unauthorized access returns 401
- Cross-user access returns 404

---

## File Structure Reference

```
backend/
  main.py              # T005, T013, T022, T042
  db.py                # T006, T007
  models.py            # T008
  schemas.py           # T009
  auth.py              # T010, T011, T012
  routes/
    tasks.py           # T015, T016, T017-T021, T023-T041
  .env                 # T004
  .env.example         # T004
  .gitignore           # T003
  requirements.txt     # T002
```

---

## Next Steps

1. Review and approve tasks.md
2. Run `/sp.implement` to start implementation
3. Execute tasks in priority order (Phase 1 → Phase 6)
4. Validate each phase before proceeding to next
5. Create PHR for tasks generation

---

## References

- @specs/002-backend-specs/plan.md - Source implementation plan
- @specs/002-backend-specs/spec.md - User stories and requirements
- @specs/002-backend-specs/data-model.md - Task entity definition
- @specs/002-backend-specs/contracts/api-contracts.md - API endpoint specs
- @specs/002-backend-specs/research.md - Technical decisions
- @specs/002-backend-specs/quickstart.md - Setup guide
