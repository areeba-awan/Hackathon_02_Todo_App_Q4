# Research Findings: Backend Implementation

**Feature**: Backend API for Todo App
**Branch**: 002-backend-specs
**Created**: 2026-02-17
**Status**: Complete

---

## Overview

This document consolidates all research findings and technical decisions for the FastAPI backend implementation. All NEEDS CLARIFICATION items from the specification phase have been resolved.

---

## Technical Decisions

### Decision 1: JWT Verification Library

**Context**: Need to verify JWT tokens issued by Better Auth

**Decision**: Use `PyJWT` library for JWT verification

**Rationale**:
- Industry standard for Python JWT handling
- Supports HS256 algorithm (used by Better Auth)
- Well-maintained and widely adopted
- Simple API for decode and verify operations
- Built-in expiration validation

**Alternatives Considered**:
- `python-jose`: More features but larger footprint
- `authlib`: Overkill for simple verification

**Implementation**:
```python
import jwt

payload = jwt.decode(
    token,
    BETTER_AUTH_SECRET,
    algorithms=["HS256"],
    options={"verify_exp": True}
)
```

**Spec Reference**: @specs/features/backend-auth-verification.md

---

### Decision 2: Database Driver

**Context**: Need PostgreSQL driver for SQLModel

**Decision**: Use `psycopg2-binary` for development, `psycopg2` for production

**Rationale**:
- SQLModel/SQLAlchemy default PostgreSQL driver
- Binary version simplifies development setup
- Production can use standard psycopg2
- Well-documented and stable

**Alternatives Considered**:
- `asyncpg`: Async support but requires different setup
- `psycopg`: Newer version but less battle-tested

**Implementation**:
```python
# requirements.txt
psycopg2-binary==2.9.9  # Development
```

**Spec Reference**: @specs/database/schema.md

---

### Decision 3: CORS Configuration

**Context**: Backend must allow frontend requests

**Decision**: Use FastAPI CORSMiddleware with FRONTEND_URL env var

**Rationale**:
- Built-in FastAPI middleware
- Simple configuration via environment variable
- Secure by default (explicit origins)
- Supports all required HTTP methods

**Implementation**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)
```

**Spec Reference**: @specs/api/rest-endpoints.md

---

### Decision 4: Error Handling Pattern

**Context**: Consistent error responses across all endpoints

**Decision**: Use FastAPI HTTPException with custom error handler

**Rationale**:
- Integrates with FastAPI exception handling
- Allows custom error format
- Automatic status code mapping
- Clean separation of concerns

**Implementation**:
```python
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed",
                "details": exc.errors()
            }
        }
    )
```

**Spec Reference**: @specs/api/rest-endpoints.md

---

### Decision 5: Database Session Management

**Context**: Need reusable database session dependency

**Decision**: Use FastAPI dependency injection with yield

**Rationale**:
- Automatic session cleanup
- Integrates with FastAPI lifecycle
- Clean, testable pattern
- Recommended by FastAPI docs

**Implementation**:
```python
from sqlmodel import Session, create_engine, SQLModel

engine = create_engine(DATABASE_URL)

def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
```

**Spec Reference**: @specs/database/schema.md

---

### Decision 6: Environment Variable Loading

**Context**: Need to load .env file for development

**Decision**: Use `python-dotenv` for environment variable loading

**Rationale**:
- Standard practice for Python projects
- Loads .env automatically on import
- No code changes needed for production
- Widely adopted and maintained

**Implementation**:
```python
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
```

**Spec Reference**: @specs/database/schema.md, @specs/features/backend-auth-verification.md

---

### Decision 7: ASGI Server

**Context**: Need server to run FastAPI application

**Decision**: Use Uvicorn as ASGI server

**Rationale**:
- Official FastAPI recommendation
- High performance (ASGI native)
- Auto-reload for development
- Simple CLI interface

**Implementation**:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Spec Reference**: Project structure

---

### Decision 8: Pydantic Version

**Context**: Need schema validation library

**Decision**: Use Pydantic v2 (via SQLModel)

**Rationale**:
- SQLModel includes Pydantic v2
- Better performance than v1
- Improved error messages
- Latest features and bug fixes

**Implementation**:
```python
from sqlmodel import SQLModel, Field
# SQLModel uses Pydantic v2 internally
```

**Spec Reference**: @specs/api/rest-endpoints.md

---

## Dependency Resolution

### Core Dependencies
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlmodel>=0.0.14
psycopg2-binary>=2.9.9
PyJWT>=2.8.0
python-dotenv>=1.0.0
```

### Development Dependencies (Optional)
```
pytest>=7.4.0
httpx>=0.25.0  # For async testing
```

---

## Integration Patterns

### Pattern 1: Auth Dependency Injection
```python
async def get_current_user(authorization: str = Header(None)) -> str:
    # Verify JWT and return user_id
    return user_id

@app.get("/api/tasks")
async def list_tasks(user_id: str = Depends(get_current_user)):
    # user_id guaranteed authenticated
```

### Pattern 2: Database Session + Auth
```python
@app.post("/api/tasks")
async def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    # Both DB and auth available
```

### Pattern 3: Error Handling
```python
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.detail, "message": str(exc.detail)}}
    )
```

---

## Best Practices Applied

### Security
- Constant-time signature comparison (hmac.compare_digest)
- Clock skew tolerance (60 seconds)
- Environment variables for secrets
- No hardcoded credentials

### Performance
- Database indexing on user_id
- Connection pooling via SQLModel
- Async-ready architecture

### Maintainability
- Dependency injection pattern
- Clear separation of concerns
- Type hints throughout
- Consistent error format

---

## Clarifications Resolved

All NEEDS CLARIFICATION items from specification phase:

| Item | Resolution |
|------|------------|
| JWT library choice | PyJWT |
| Database driver | psycopg2-binary |
| CORS setup | FastAPI CORSMiddleware |
| Error format | Custom JSONResponse handler |
| Session management | FastAPI yield dependency |
| Environment loading | python-dotenv |
| ASGI server | Uvicorn |
| Pydantic version | v2 (via SQLModel) |

---

## References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLModel Documentation: https://sqlmodel.tiangolo.com/
- PyJWT Documentation: https://pyjwt.readthedocs.io/
- Neon PostgreSQL: https://neon.tech/docs

---

## Next Steps

All research complete. Proceed to Phase 1 design:
1. Create data-model.md with entity definitions
2. Create contracts/api-contracts.md with API specs
3. Create quickstart.md with setup guide
4. Update agent context with backend technologies
