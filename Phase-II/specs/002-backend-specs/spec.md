---
feature: "Backend API Specification"
branch: "001-backend-specs"
created: "2026-02-17"
status: "Draft"
input: "Backend specification for FastAPI todo app with JWT authentication verification"
constitution_compliance: "All features must comply with project constitution v1.0.0"
---

# Feature Specification: Backend API for Todo App

**Feature Branch**: `001-backend-specs`
**Created**: 2026-02-17
**Status**: Draft
**Input**: Backend specification for FastAPI todo app with JWT authentication verification
**Constitution Compliance**: All features must comply with project constitution v1.0.0

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure Task Data Access (Priority: P1)

As an authenticated user, I want my task data to be securely accessed only by me so that my personal information remains private.

**Why this priority**: Security and data isolation are foundational requirements for any multi-user application. Users must trust that their data cannot be accessed by others.

**Independent Test**: Can be fully tested by attempting to access another user's tasks with a valid token - all such attempts must fail.

**Acceptance Scenarios**:

1. **Given** user has a valid JWT token, **When** user requests their tasks, **Then** user receives only their own tasks
2. **Given** user has a valid JWT token, **When** user attempts to access another user's task by ID, **Then** request is rejected with 403 Forbidden
3. **Given** user has an invalid/expired JWT token, **When** user requests any protected endpoint, **Then** request is rejected with 401 Unauthorized

---

### User Story 2 - Create and Manage Tasks (Priority: P1)

As an authenticated user, I want to create, read, update, and delete my tasks so that I can effectively manage my todo list.

**Why this priority**: CRUD operations are the core functionality of a todo application. Without these, the application provides no value.

**Independent Test**: Can be fully tested by performing all CRUD operations and verifying data persistence and isolation.

**Acceptance Scenarios**:

1. **Given** user is authenticated, **When** user creates a task with valid data, **Then** task is created and returned with assigned ID
2. **Given** user has existing tasks, **When** user requests task list, **Then** user receives all their tasks in a structured format
3. **Given** user has an existing task, **When** user updates the task with valid data, **Then** task is updated and changes are reflected
4. **Given** user has an existing task, **When** user marks task as complete, **Then** task completion status is updated
5. **Given** user has an existing task, **When** user deletes the task, **Then** task is permanently removed

---

### User Story 3 - Receive Clear Error Feedback (Priority: P2)

As a user, I want to receive clear, actionable error messages when operations fail so that I understand what went wrong and how to fix it.

**Why this priority**: Clear error messages improve user experience and reduce frustration when things don't work as expected.

**Independent Test**: Can be fully tested by triggering various error conditions and verifying error response format and clarity.

**Acceptance Scenarios**:

1. **Given** user sends invalid request data, **When** API validates the request, **Then** user receives 422 with specific field errors
2. **Given** user sends request without authentication, **When** API checks authentication, **Then** user receives 401 with clear message
3. **Given** user requests non-existent task, **When** API looks up the task, **Then** user receives 404 with clear message

---

### Edge Cases

- What happens when a user tries to create a task with a title exceeding 200 characters?
- How does the system handle concurrent updates to the same task?
- What occurs when the database connection is temporarily unavailable?
- How does the API behave when JWT token is malformed or tampered with?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide REST API endpoints under `/api/tasks` prefix
- **FR-002**: System MUST require JWT authentication for all task-related endpoints via Authorization header
- **FR-003**: System MUST verify JWT tokens using BETTER_AUTH_SECRET environment variable
- **FR-004**: System MUST extract user_id from JWT token payload for request context
- **FR-005**: System MUST reject requests with invalid/missing tokens with 401 Unauthorized
- **FR-006**: System MUST reject cross-user resource access attempts with 403 Forbidden
- **FR-007**: System MUST provide GET endpoint to list all tasks for authenticated user
- **FR-008**: System MUST provide POST endpoint to create new tasks
- **FR-009**: System MUST provide GET endpoint to retrieve single task by ID
- **FR-010**: System MUST provide PUT endpoint to update existing task
- **FR-011**: System MUST provide DELETE endpoint to remove task
- **FR-012**: System MUST provide PATCH endpoint to toggle task completion status
- **FR-013**: System MUST validate task title is required and between 1-200 characters
- **FR-014**: System MUST allow optional task description field
- **FR-015**: System MUST track created_at and updated_at timestamps for all tasks
- **FR-016**: System MUST return consistent JSON error responses with status codes
- **FR-017**: System MUST support CORS for frontend origin configured via environment variable
- **FR-018**: System MUST use DATABASE_URL environment variable for database connection
- **FR-019**: System MUST index tasks by user_id for efficient querying
- **FR-020**: System MUST enforce foreign key constraint linking tasks to user_id

### Constitution Compliance Requirements

- **CC-001**: All implementation MUST follow the spec-driven workflow: Constitution → Specs → Plan → Tasks → Implement
- **CC-002**: No manual coding is allowed; all code MUST be generated via Claude Code
- **CC-003**: All API endpoints MUST require JWT authentication via Better Auth
- **CC-004**: All task data MUST be filtered by authenticated user's user_id
- **CC-005**: Users MAY ONLY access their own tasks; unauthorized access MUST return 401/403
- **CC-006**: All features MUST be documented in specs/api/*, specs/database/*, specs/features/*

### Key Entities

- **User**: Represents an authenticated individual identified by user_id extracted from JWT token
- **Task**: Represents a user's todo item with id, user_id, title, description, completed status, created_at, updated_at
- **JWT Token**: Authentication credential issued by Better Auth containing user_id in payload

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All authenticated API requests complete within 500ms under normal load
- **SC-002**: System correctly rejects 100% of unauthorized access attempts
- **SC-003**: System correctly rejects 100% of cross-user data access attempts
- **SC-004**: API returns appropriate HTTP status codes (200, 201, 400, 401, 403, 404, 422) for all scenarios
- **SC-005**: All task CRUD operations are idempotent and produce consistent results
- **SC-006**: Database queries filter by user_id on all task operations
- **SC-007**: Error responses include clear, actionable messages without exposing internal details
- **SC-008**: API supports concurrent requests from multiple users without data leakage

## Assumptions

- **A-001**: JWT tokens are issued by a separate Better Auth service (not this backend)
- **A-002**: BETTER_AUTH_SECRET environment variable is available and matches the auth service
- **A-003**: Neon PostgreSQL database is provisioned and accessible via DATABASE_URL
- **A-004**: Frontend is configured to send JWT in Authorization header as "Bearer {token}"
- **A-005**: Task deletion is permanent (no soft delete or trash functionality)
