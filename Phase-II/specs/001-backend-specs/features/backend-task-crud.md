# Backend Task CRUD Operations Specification

**Feature**: Task Management API
**Scope**: Backend CRUD operations for tasks with user isolation

## Overview

This specification defines the backend behavior for task Create, Read, Update, and Delete (CRUD) operations. All operations require JWT authentication and enforce strict user isolation.

## Authentication Flow

Every request MUST follow this authentication sequence:

1. Extract `Authorization` header from request
2. Parse Bearer token: `Bearer {jwt_token}`
3. Verify JWT signature using `BETTER_AUTH_SECRET`
4. Extract `user_id` from token payload
5. Attach `user_id` to request context
6. Proceed with business logic

**Failure Points**:
- Missing Authorization header → 401 Unauthorized
- Invalid token format → 401 Unauthorized
- Expired token → 401 Unauthorized
- Invalid signature → 401 Unauthorized

---

## Create Task

**Endpoint**: `POST /api/tasks`

**Authentication**: Required

**Request Processing**:
1. Authenticate request and extract `user_id`
2. Validate request body:
   - `title`: Required, 1-200 characters
   - `description`: Optional
3. Create task record with:
   - `user_id`: From authenticated context
   - `title`: From request
   - `description`: From request (or NULL)
   - `completed`: FALSE (default)
   - `created_at`: Current timestamp
   - `updated_at`: Current timestamp
4. Return created task with 201 status

**Validation Rules**:
```
IF title is missing OR title.length < 1 OR title.length > 200:
    RETURN 422 Validation Error
```

**Success Response**: `201 Created`
```json
{
  "id": 1,
  "user_id": "user_123",
  "title": "My Task",
  "description": "Task description",
  "completed": false,
  "created_at": "2026-02-17T10:00:00Z",
  "updated_at": "2026-02-17T10:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing token
- `422 Validation Error`: Invalid request body

---

## Read Tasks (List)

**Endpoint**: `GET /api/tasks`

**Authentication**: Required

**Request Processing**:
1. Authenticate request and extract `user_id`
2. Query tasks filtered by `user_id`:
   ```sql
   SELECT * FROM tasks WHERE user_id = :user_id
   ```
3. Optional: Filter by `completed` query parameter
4. Return task list with 200 status

**Query Parameters**:
- `completed` (optional): Boolean filter for completion status

**Success Response**: `200 OK`
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "user_123",
      "title": "My Task",
      "description": "Task description",
      "completed": false,
      "created_at": "2026-02-17T10:00:00Z",
      "updated_at": "2026-02-17T10:00:00Z"
    }
  ]
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing token

---

## Read Task (Single)

**Endpoint**: `GET /api/tasks/{id}`

**Authentication**: Required

**Request Processing**:
1. Authenticate request and extract `user_id`
2. Query task by ID and `user_id`:
   ```sql
   SELECT * FROM tasks WHERE id = :id AND user_id = :user_id
   ```
3. If task not found → 404 Not Found
4. If task belongs to different user → 403 Forbidden (implicit via no results)
5. Return task with 200 status

**Path Parameters**:
- `id`: Task ID (integer)

**Success Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": "user_123",
  "title": "My Task",
  "description": "Task description",
  "completed": false,
  "created_at": "2026-02-17T10:00:00Z",
  "updated_at": "2026-02-17T10:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Task does not exist or belongs to different user

---

## Update Task

**Endpoint**: `PUT /api/tasks/{id}`

**Authentication**: Required

**Request Processing**:
1. Authenticate request and extract `user_id`
2. Verify task ownership:
   ```sql
   SELECT * FROM tasks WHERE id = :id AND user_id = :user_id
   ```
3. If task not found → 404 Not Found
4. Validate request body:
   - `title`: Required, 1-200 characters
   - `description`: Optional
   - `completed`: Required boolean
5. Update task:
   ```sql
   UPDATE tasks 
   SET title = :title, 
       description = :description, 
       completed = :completed,
       updated_at = CURRENT_TIMESTAMP
   WHERE id = :id AND user_id = :user_id
   RETURNING *
   ```
6. Return updated task with 200 status

**Validation Rules**:
```
IF title is missing OR title.length < 1 OR title.length > 200:
    RETURN 422 Validation Error
IF completed is missing OR not boolean:
    RETURN 422 Validation Error
```

**Success Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": "user_123",
  "title": "Updated Task",
  "description": "Updated description",
  "completed": true,
  "created_at": "2026-02-17T10:00:00Z",
  "updated_at": "2026-02-17T11:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Task does not exist or belongs to different user
- `422 Validation Error`: Invalid request body

---

## Delete Task

**Endpoint**: `DELETE /api/tasks/{id}`

**Authentication**: Required

**Request Processing**:
1. Authenticate request and extract `user_id`
2. Verify task ownership:
   ```sql
   SELECT * FROM tasks WHERE id = :id AND user_id = :user_id
   ```
3. If task not found → 404 Not Found
4. Delete task:
   ```sql
   DELETE FROM tasks WHERE id = :id AND user_id = :user_id
   ```
5. Return 204 No Content

**Success Response**: `204 No Content`

**Error Responses**:
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Task does not exist or belongs to different user

---

## Toggle Task Completion

**Endpoint**: `PATCH /api/tasks/{id}/complete`

**Authentication**: Required

**Request Processing**:
1. Authenticate request and extract `user_id`
2. Verify task ownership:
   ```sql
   SELECT * FROM tasks WHERE id = :id AND user_id = :user_id
   ```
3. If task not found → 404 Not Found
4. Toggle completion status:
   ```sql
   UPDATE tasks 
   SET completed = NOT completed,
       updated_at = CURRENT_TIMESTAMP
   WHERE id = :id AND user_id = :user_id
   RETURNING *
   ```
5. Return updated task with 200 status

**Success Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": "user_123",
  "title": "My Task",
  "description": "Task description",
  "completed": true,
  "created_at": "2026-02-17T10:00:00Z",
  "updated_at": "2026-02-17T11:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Task does not exist or belongs to different user

---

## Security Requirements

### User Isolation

**Rule**: Users can ONLY access their own tasks.

**Implementation**:
- Every query MUST include `WHERE user_id = :user_id`
- `user_id` MUST come from authenticated JWT context
- Never trust client-provided `user_id` values

### Authorization Checks

| Scenario                           | Expected Behavior              |
|------------------------------------|--------------------------------|
| Valid token, own task              | Allow access                   |
| Valid token, another user's task   | Return 404 (not 403)           |
| Invalid/missing token              | Return 401                     |
| Expired token                      | Return 401                     |

**Note**: Returning 404 for cross-user access attempts prevents information leakage about task existence.

---

## Error Handling

### Consistent Error Format

All errors MUST follow this structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}
  }
}
```

### Error Code Definitions

| Code             | HTTP Status | Description                          |
|------------------|-------------|--------------------------------------|
| UNAUTHORIZED     | 401         | Missing or invalid JWT token         |
| NOT_FOUND        | 404         | Resource does not exist              |
| VALIDATION_ERROR | 422         | Request validation failed            |

### Validation Error Details

For 422 responses, `details` object MUST include field-specific errors:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "title": "Title is required and must be between 1 and 200 characters"
    }
  }
}
```

---

## Environment Variables

| Variable          | Required | Description                          |
|-------------------|----------|--------------------------------------|
| BETTER_AUTH_SECRET| Yes      | Secret key for JWT verification      |
| DATABASE_URL      | Yes      | PostgreSQL connection string         |
