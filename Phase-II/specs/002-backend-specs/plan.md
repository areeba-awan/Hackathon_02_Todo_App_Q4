---
feature: "Backend API Implementation Plan"
branch: "002-backend-specs"
created: "2026-02-17"
status: "Draft"
input: "Backend implementation plan for FastAPI todo app"
constitution_compliance: "All features must comply with project constitution v1.0.0"
---

# Implementation Plan: Backend API for Todo App

**Feature Branch**: `002-backend-specs`
**Created**: 2026-02-17
**Status**: Draft
**Input**: Backend implementation plan for FastAPI todo app
**Constitution Compliance**: All features must comply with project constitution v1.0.0

---

## Technical Context

### Technologies
- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLModel
- **Database**: Neon PostgreSQL (serverless)
- **Authentication**: JWT verification (Better Auth issued tokens)
- **Environment**: Python virtual environment

### Architecture Overview
```
Frontend (Next.js) → Backend (FastAPI) → Database (Neon PostgreSQL)
       ↓                    ↓
   Better Auth        JWT Verification
```

### Project Structure (Target)
```
backend/
  main.py              # FastAPI app entry point
  db.py                # Database connection and session
  models.py            # SQLModel entities
  schemas.py           # Pydantic request/response schemas
  auth.py              # JWT verification dependency
  routes/
    tasks.py           # Task CRUD endpoints
  .env                 # Environment variables (not committed)
  requirements.txt     # Python dependencies
```

### Known Constraints
- Backend runs independently from frontend
- JWT tokens issued by Better Auth (frontend service)
- BETTER_AUTH_SECRET must match frontend auth service
- DATABASE_URL provided by Neon PostgreSQL

---

## Constitution Check

### Principle 1: Sequential Process Adherence ✅
- Specs completed: spec.md, rest-endpoints.md, schema.md, backend-task-crud.md, backend-auth-verification.md
- Plan being created now
- Tasks will follow this plan
- Implementation will follow tasks

### Principle 2: Process Integrity ✅
- No steps skipped
- All implementation decisions traceable to specs

### Principle 3: No Manual Coding ✅
- All code will be generated via Claude Code
- This plan provides roadmap only, no implementation code

### Principle 4: Spec-First Changes ✅
- Any changes must update specs first
- Plan references spec files throughout

### Principle 5: Mandatory Authentication ✅
- All 6 endpoints require JWT authentication
- Auth dependency defined in auth.py

### Principle 6: JWT Implementation ✅
- JWT verification uses BETTER_AUTH_SECRET
- user_id extracted from token payload

### Principle 7: User Isolation ✅
- All queries filter by user_id
- Cross-user access returns 404

### Principle 8: Persistent Storage ✅
- Neon PostgreSQL specified
- SQLModel ORM for database operations

### Principle 9: API Compliance ✅
- REST endpoints follow spec exactly
- Task ownership enforced at query level

### Principle 10: Single Source of Truth ✅
- All features documented in specs/
- Plan references spec files

### Principle 11: Spec Referencing ✅
- Plan uses @specs paths throughout
- Implementation will reference specs

### Principle 12: Role Adherence ✅
- Plan stays within backend scope
- No frontend tasks included

### Principle 13: Constraint Enforcement ✅
- No feature invention
- Hackathon constraints respected

### Principle 14: Violation Response ✅
- All violations would stop execution
- Spec-level corrections required

---

## Gates Evaluation

### Gate 1: Spec Completeness
**Status**: PASS
- All required spec files exist
- User stories defined with acceptance criteria
- Requirements are testable
- Success criteria are measurable

### Gate 2: Constitution Compliance
**Status**: PASS
- All 14 principles verified
- No violations detected
- Backend scope strictly enforced

### Gate 3: Technical Readiness
**Status**: PASS
- Technology stack confirmed
- Database connection defined
- Authentication flow specified
- No blocking unknowns

---

## Phase 0: Research & Clarification

**Status**: COMPLETE

All technical decisions resolved during specification phase:

### Decision: JWT Library
- **Chosen**: PyJWT or equivalent Python JWT library
- **Rationale**: Standard JWT verification for Python
- **Spec Reference**: @specs/features/backend-auth-verification.md

### Decision: Database Connection
- **Chosen**: SQLModel with Neon PostgreSQL connection string
- **Rationale**: SQLModel provides SQLAlchemy + Pydantic integration
- **Spec Reference**: @specs/database/schema.md

### Decision: CORS Configuration
- **Chosen**: FastAPI CORS middleware with FRONTEND_URL env var
- **Rationale**: Allows frontend origin while maintaining security
- **Spec Reference**: @specs/api/rest-endpoints.md

### Decision: Error Handling
- **Chosen**: Consistent JSON error format with error codes
- **Rationale**: Frontend needs predictable error responses
- **Spec Reference**: @specs/api/rest-endpoints.md

**Output**: `research.md` - All clarifications resolved

---

## Phase 1: Design & Contracts

### 1.1 Data Model Design

**Source**: @specs/database/schema.md

**Entity: Task**
```
Fields:
- id: int (primary key, auto-increment)
- user_id: str (max 255, indexed, not null)
- title: str (max 200, not null)
- description: str (optional, text)
- completed: bool (default false)
- created_at: datetime (default now)
- updated_at: datetime (default now)

Indexes:
- idx_tasks_user_id (user_id)
- idx_tasks_user_completed (user_id, completed)

Constraints:
- title length: 1-200 characters
- user_id required (no orphan tasks)
```

**Output**: `data-model.md` - SQLModel entity definitions

---

### 1.2 API Contracts

**Source**: @specs/api/rest-endpoints.md

**Base Path**: `/api/tasks`

**Endpoints**:
1. `GET /api/tasks` - List user's tasks
2. `POST /api/tasks` - Create task
3. `GET /api/tasks/{id}` - Get single task
4. `PUT /api/tasks/{id}` - Update task
5. `DELETE /api/tasks/{id}` - Delete task
6. `PATCH /api/tasks/{id}/complete` - Toggle completion

**Request Schemas**:
```
TaskCreate:
- title: str (required, 1-200 chars)
- description: str (optional)

TaskUpdate:
- title: str (required, 1-200 chars)
- description: str (optional)
- completed: bool (required)
```

**Response Schema**:
```
TaskResponse:
- id: int
- user_id: str
- title: str
- description: str | null
- completed: bool
- created_at: datetime
- updated_at: datetime

TaskListResponse:
- tasks: list[TaskResponse]
```

**Error Schema**:
```
ErrorResponse:
- error:
  - code: str
  - message: str
  - details: dict (optional)
```

**Output**: `contracts/api-contracts.md` - OpenAPI-style contract definitions

---

### 1.3 Quickstart Guide

**Purpose**: Developer setup instructions

**Steps**:
1. Create Python virtual environment
2. Install dependencies from requirements.txt
3. Create .env file with DATABASE_URL and BETTER_AUTH_SECRET
4. Run database migrations (create tasks table)
5. Start FastAPI server with uvicorn

**Output**: `quickstart.md` - Development setup guide

---

### 1.4 Agent Context Update

**Purpose**: Update Qwen agent context with backend technologies

**Technologies to Add**:
- FastAPI framework
- SQLModel ORM
- PyJWT library
- Neon PostgreSQL
- Uvicorn ASGI server

**Output**: Agent-specific context file updated

---

## Phase 2: Implementation Breakdown

### Phase 2.1: Project Setup

**Purpose**: Initialize backend project structure

**Steps**:
1. Create backend/ directory structure
2. Create requirements.txt with dependencies:
   - fastapi
   - uvicorn
   - sqlmodel
   - psycopg2-binary (or asyncpg)
   - python-jose or PyJWT
   - python-dotenv
   - fastapi.middleware.cors
3. Create .env template file
4. Create .gitignore for Python projects
5. Set up Python virtual environment

**Dependencies**: None
**Expected Outcome**: Empty project structure ready for implementation

---

### Phase 2.2: Database Layer

**Purpose**: Set up database connection and models

**Steps**:
1. Create db.py:
   - Define create_db_session() dependency
   - Set up engine with DATABASE_URL
   - Create session-local storage
   - Define get_db() dependency for routes
2. Create models.py:
   - Define Task SQLModel class
   - Include all fields from spec
   - Add table_name = "tasks"
   - Define indexes via Field parameters
3. Create database initialization script:
   - Create tables using SQLModel metadata
   - Verify connection to Neon PostgreSQL

**Dependencies**: Phase 2.1 complete
**Expected Outcome**: Working database connection and Task model

---

### Phase 2.3: Authentication Layer

**Purpose**: Implement JWT verification dependency

**Steps**:
1. Create auth.py:
   - Define get_current_user() dependency
   - Extract Authorization header
   - Parse Bearer token
   - Verify JWT signature using BETTER_AUTH_SECRET
   - Validate token expiration
   - Extract user_id from payload
   - Raise HTTPException(401) on any failure
2. Implement constant-time signature comparison
3. Add clock skew tolerance (60 seconds)
4. Create error response helpers for auth failures

**Dependencies**: Phase 2.1 complete
**Expected Outcome**: Reusable auth dependency for route protection

---

### Phase 2.4: Schema Definitions

**Purpose**: Define Pydantic schemas for requests/responses

**Steps**:
1. Create schemas.py:
   - Define TaskCreate schema (title required, description optional)
   - Define TaskUpdate schema (all fields with validation)
   - Define TaskResponse schema (all Task fields)
   - Define TaskListResponse schema
   - Define ErrorResponse schema
   - Add validation rules (title 1-200 chars)
2. Add response models to FastAPI routes

**Dependencies**: Phase 2.1 complete
**Expected Outcome**: Type-safe request/response handling

---

### Phase 2.5: Task CRUD Routes

**Purpose**: Implement all 6 task endpoints

**Steps**:
1. Create routes/tasks.py:
   - Import FastAPI APIRouter
   - Import db session dependency
   - Import auth dependency
   - Import schemas
   - Import Task model
2. Implement GET /api/tasks:
   - Depend on get_db() and get_current_user()
   - Query tasks WHERE user_id = current_user
   - Optional: filter by completed query param
   - Return TaskListResponse
3. Implement POST /api/tasks:
   - Validate TaskCreate schema
   - Create Task with user_id from auth context
   - Return TaskResponse with 201 status
4. Implement GET /api/tasks/{id}:
   - Query task WHERE id AND user_id match
   - Return 404 if not found
   - Return TaskResponse
5. Implement PUT /api/tasks/{id}:
   - Verify ownership
   - Validate TaskUpdate schema
   - Update task and updated_at timestamp
   - Return TaskResponse
6. Implement DELETE /api/tasks/{id}:
   - Verify ownership
   - Delete task
   - Return 204 No Content
7. Implement PATCH /api/tasks/{id}/complete:
   - Verify ownership
   - Toggle completed boolean
   - Update updated_at timestamp
   - Return TaskResponse

**Dependencies**: Phase 2.2, 2.3, 2.4 complete
**Expected Outcome**: All 6 CRUD endpoints functional

---

### Phase 2.6: Main Application Assembly

**Purpose**: Wire all components together

**Steps**:
1. Create main.py:
   - Initialize FastAPI app
   - Configure CORS middleware:
     - Allow origins from FRONTEND_URL env var
     - Allow methods: GET, POST, PUT, DELETE, PATCH, OPTIONS
     - Allow headers: Content-Type, Authorization
   - Include routes from routes/tasks.py
   - Add health check endpoint (optional)
   - Define lifespan context manager for DB cleanup
2. Add exception handlers:
   - Handle 404 globally
   - Handle validation errors (422)
   - Format errors per spec
3. Configure OpenAPI docs at /docs

**Dependencies**: All Phase 2.x complete
**Expected Outcome**: Complete, runnable FastAPI application

---

### Phase 2.7: Environment & Configuration

**Purpose**: Set up environment variables and configuration

**Steps**:
1. Create .env.example template:
   ```
   DATABASE_URL=postgresql://...
   BETTER_AUTH_SECRET=your-secret-key-min-32-chars
   FRONTEND_URL=http://localhost:3000
   ```
2. Document environment variable requirements
3. Add configuration loading in main.py or config.py
4. Ensure .env is in .gitignore

**Dependencies**: Phase 2.6 complete
**Expected Outcome**: Configuration management ready for deployment

---

## Phase 3: Integration & Validation

### Phase 3.1: Frontend Compatibility

**Purpose**: Ensure backend works with existing frontend

**Validation Steps**:
1. Verify CORS allows frontend origin
2. Test JWT header format matches frontend output
3. Confirm JSON response structure matches frontend expectations
4. Verify error codes match frontend error handling
5. Test with frontend running against backend

**Dependencies**: All phases complete
**Expected Outcome**: Backend ready for frontend integration

---

### Phase 3.2: Constitution Compliance Check

**Purpose**: Final verification against constitution

**Checklist**:
- [ ] All endpoints require JWT authentication
- [ ] User isolation enforced on all queries
- [ ] No manual coding detected
- [ ] All code generated via Claude Code
- [ ] Specs updated if any changes made
- [ ] Error responses follow consistent format
- [ ] Database uses Neon PostgreSQL
- [ ] BETTER_AUTH_SECRET used for verification

**Dependencies**: All phases complete
**Expected Outcome**: Constitution compliance verified

---

## Success Criteria Validation

After implementation, verify:

| Criterion | Validation Method |
|-----------|-------------------|
| SC-001: API < 500ms | Load testing with multiple concurrent requests |
| SC-002: 100% auth rejection | Test all endpoints without valid token |
| SC-003: 100% cross-user rejection | Test accessing another user's tasks |
| SC-004: Correct status codes | Test all error scenarios |
| SC-005: Idempotent operations | Repeat operations, verify consistency |
| SC-006: user_id filtering | Inspect all generated queries |
| SC-007: Clear error messages | Review all error response formats |
| SC-008: No data leakage | Test concurrent multi-user scenarios |

---

## Risk Mitigation

### Risk 1: JWT Verification Fails
**Mitigation**: Ensure BETTER_AUTH_SECRET matches frontend exactly
**Fallback**: Test with known-good token during development

### Risk 2: Database Connection Issues
**Mitigation**: Verify DATABASE_URL format, check Neon SSL requirements
**Fallback**: Use connection pooling, add retry logic

### Risk 3: CORS Blocks Frontend
**Mitigation**: Add frontend URL to allowed origins
**Fallback**: Test with wildcard (*) during development only

---

## Definition of Done

Implementation is complete when:

- [ ] All 6 endpoints implemented and tested
- [ ] JWT authentication working on all routes
- [ ] User isolation enforced at database level
- [ ] Error responses match spec format
- [ ] CORS configured for frontend
- [ ] Database schema matches spec
- [ ] Environment variables documented
- [ ] Code generated via Claude Code (no manual coding)
- [ ] All constitution principles verified
- [ ] Frontend can successfully call all endpoints

---

## Next Steps

After plan completion:
1. Run `/sp.tasks` to break this plan into actionable tasks
2. Execute tasks via `/sp.implement`
3. Validate implementation against success criteria
4. Create PHR for planning phase

---

## Artifacts Generated

- `plan.md` - This implementation plan
- `research.md` - Research findings (all resolved)
- `data-model.md` - Entity definitions
- `contracts/api-contracts.md` - API contract specifications
- `quickstart.md` - Development setup guide
- Agent context file updated with backend technologies
