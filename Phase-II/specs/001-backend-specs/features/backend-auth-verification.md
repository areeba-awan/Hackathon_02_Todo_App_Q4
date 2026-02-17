# Backend Authentication Verification Specification

**Feature**: JWT Token Verification
**Scope**: Verifying JWT tokens issued by Better Auth

## Overview

This specification defines how the backend verifies JWT tokens for authenticating API requests. The backend does NOT issue tokens - it only verifies tokens issued by the Better Auth service.

## Authentication Dependency

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Frontend  │ ──────▶ │   Backend   │ ──────▶ │ Better Auth │
│             │  JWT    │             │  Verify │   Service   │
│             │         │             │         │             │
└─────────────┘         └─────────────┘         └─────────────┘
```

**Key Points**:
- Frontend obtains JWT from Better Auth (separate service)
- Frontend sends JWT to backend in Authorization header
- Backend verifies JWT using shared secret
- Backend extracts `user_id` from token payload

---

## JWT Token Structure

### Header
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Payload (Claims)
```json
{
  "sub": "user_123",
  "user_id": "user_123",
  "iat": 1708164000,
  "exp": 1708250400
}
```

**Required Claims**:
- `user_id` (or `sub`): Unique identifier for the authenticated user
- `iat`: Issued at timestamp
- `exp`: Expiration timestamp

### Signature
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  BETTER_AUTH_SECRET
)
```

---

## Token Verification Process

### Step 1: Extract Authorization Header

**Request Header**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Extraction Logic**:
```
1. Read "Authorization" header
2. IF header is missing:
   RETURN 401 Unauthorized
3. IF header does not start with "Bearer ":
   RETURN 401 Unauthorized
4. Extract token: token = header.substring(7)
5. IF token is empty:
   RETURN 401 Unauthorized
```

### Step 2: Decode Token

**Decoding Logic**:
```
1. Split token by ".": parts = token.split(".")
2. IF parts.length != 3:
   RETURN 401 Unauthorized
3. Decode header from base64url
4. Decode payload from base64url
5. IF decoding fails:
   RETURN 401 Unauthorized
```

### Step 3: Verify Signature

**Verification Logic**:
```
1. Read BETTER_AUTH_SECRET from environment
2. IF BETTER_AUTH_SECRET is not set:
   LOG error "BETTER_AUTH_SECRET not configured"
   RETURN 500 Internal Server Error
3. Compute expected signature:
   expected = HMACSHA256(
     header_b64 + "." + payload_b64,
     BETTER_AUTH_SECRET
   )
4. Compare signatures (constant-time comparison):
   IF NOT constantTimeCompare(signature, expected):
     RETURN 401 Unauthorized
```

### Step 4: Validate Claims

**Validation Logic**:
```
1. Check expiration:
   current_time = unix_timestamp()
   IF payload.exp < current_time:
     RETURN 401 Unauthorized (token expired)

2. Check issued-at (optional, future protection):
   IF payload.iat > current_time + clock_skew:
     RETURN 401 Unauthorized (token from future)

3. Extract user_id:
   user_id = payload.user_id OR payload.sub
   IF user_id is missing or empty:
     RETURN 401 Unauthorized (invalid token structure)
```

### Step 5: Attach to Request Context

**Context Attachment**:
```
request.context.user_id = user_id
request.context.authenticated = true
proceed_to_handler()
```

---

## Error Responses

All authentication failures MUST return 401 Unauthorized with consistent format:

### Missing Authorization Header
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authorization header is required"
  }
}
```

### Invalid Token Format
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid token format"
  }
}
```

### Invalid Signature
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid token signature"
  }
}
```

### Expired Token
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Token has expired"
  }
}
```

### Missing user_id Claim
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid token: missing user_id"
  }
}
```

---

## Security Requirements

### Secret Key Management

**BETTER_AUTH_SECRET**:
- MUST be set via environment variable
- MUST match the secret used by Better Auth service
- MUST be at least 32 characters long
- MUST NOT be committed to version control
- MUST be rotated periodically (out of scope for Phase-II)

### Constant-Time Comparison

Signature comparison MUST use constant-time algorithm to prevent timing attacks:

```python
# Example in Python
import hmac

def verify_signature(provided: str, expected: str) -> bool:
    return hmac.compare_digest(provided, expected)
```

### Clock Skew Tolerance

Allow small clock skew (±60 seconds) for expiration checks:

```
clock_skew = 60  # seconds
IF payload.exp < current_time - clock_skew:
    RETURN 401 Unauthorized
```

---

## Reusable Authentication Component

Authentication MUST be implemented as reusable middleware/dependency:

### Pattern: Dependency Injection (FastAPI)

```python
async def get_current_user(authorization: str = Header(None)) -> str:
    """
    Extract and verify JWT token, return user_id
    Raises HTTPException with 401 on any failure
    """
    # Implementation per verification process above
    return user_id
```

### Usage in Routes

```python
@app.get("/api/tasks")
async def list_tasks(user_id: str = Depends(get_current_user)):
    # user_id is guaranteed to be authenticated
    tasks = query_tasks_for_user(user_id)
    return {"tasks": tasks}
```

**Benefits**:
- Single source of truth for authentication logic
- Consistent error handling across all endpoints
- Easy to test and maintain
- Prevents authentication bypass bugs

---

## Environment Variables

| Variable          | Required | Description                          | Example                          |
|-------------------|----------|--------------------------------------|----------------------------------|
| BETTER_AUTH_SECRET| Yes      | Shared secret for JWT verification   | "your-32-char-secret-key-here"   |

**Configuration Example**:
```bash
# .env file
BETTER_AUTH_SECRET=super-secret-key-at-least-32-characters-long
```

---

## Testing Scenarios

### Valid Token
```
GIVEN: Valid JWT with user_id="user_123"
WHEN: Request sent with Authorization: Bearer {token}
THEN: Request succeeds with user_id="user_123" in context
```

### Missing Token
```
GIVEN: No Authorization header
WHEN: Request sent to protected endpoint
THEN: 401 Unauthorized returned
```

### Expired Token
```
GIVEN: JWT with exp timestamp in the past
WHEN: Request sent with Authorization: Bearer {token}
THEN: 401 Unauthorized with "Token has expired"
```

### Invalid Signature
```
GIVEN: JWT signed with wrong secret
WHEN: Request sent with Authorization: Bearer {token}
THEN: 401 Unauthorized with "Invalid token signature"
```

### Malformed Token
```
GIVEN: String that is not valid JWT format
WHEN: Request sent with Authorization: Bearer {token}
THEN: 401 Unauthorized with "Invalid token format"
```
