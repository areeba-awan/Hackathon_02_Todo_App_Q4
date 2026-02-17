# API Contracts Specification

**Feature**: Backend API for Todo App
**Branch**: 002-backend-specs
**Created**: 2026-02-17
**Status**: Draft

---

## Overview

This document defines the API contracts for the backend REST endpoints. All contracts are derived from @specs/api/rest-endpoints.md and @specs/features/backend-task-crud.md.

---

## Base Configuration

**Base Path**: `/api/tasks`

**Authentication**: JWT Bearer token required for all endpoints

**Content Type**: `application/json`

---

## Authentication

### Authorization Header

All requests must include:

```
Authorization: Bearer {jwt_token}
```

### Token Requirements

- Token must be valid and not expired
- Token must be signed with BETTER_AUTH_SECRET
- Token must contain `user_id` or `sub` claim
- Token extracted from Authorization header

### Authentication Failure Response

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired token"
  }
}
```

**Status Code**: `401 Unauthorized`

---

## Request Schemas

### TaskCreate

**Used By**: `POST /api/tasks`

```json
{
  "title": "string (required, 1-200 characters)",
  "description": "string (optional, max unlimited)"
}
```

**Validation Rules**:
- `title`: Required, minimum 1 character, maximum 200 characters
- `description`: Optional, defaults to null if not provided

**Example**:
```json
{
  "title": "Complete backend API",
  "description": "Implement all CRUD endpoints"
}
```

---

### TaskUpdate

**Used By**: `PUT /api/tasks/{id}`

```json
{
  "title": "string (required, 1-200 characters)",
  "description": "string (optional)",
  "completed": "boolean (required)"
}
```

**Validation Rules**:
- `title`: Required, minimum 1 character, maximum 200 characters
- `description`: Optional
- `completed`: Required boolean

**Example**:
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true
}
```

---

## Response Schemas

### TaskResponse

**Used By**: All successful task operations

```json
{
  "id": "integer",
  "user_id": "string",
  "title": "string",
  "description": "string or null",
  "completed": "boolean",
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime"
}
```

**Example**:
```json
{
  "id": 1,
  "user_id": "user_123",
  "title": "Complete backend API",
  "description": "Implement all CRUD endpoints",
  "completed": false,
  "created_at": "2026-02-17T10:00:00Z",
  "updated_at": "2026-02-17T10:00:00Z"
}
```

---

### TaskListResponse

**Used By**: `GET /api/tasks`

```json
{
  "tasks": ["array of TaskResponse objects"]
}
```

**Example**:
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "user_123",
      "title": "Task 1",
      "description": null,
      "completed": false,
      "created_at": "2026-02-17T10:00:00Z",
      "updated_at": "2026-02-17T10:00:00Z"
    },
    {
      "id": 2,
      "user_id": "user_123",
      "title": "Task 2",
      "description": "Description here",
      "completed": true,
      "created_at": "2026-02-17T11:00:00Z",
      "updated_at": "2026-02-17T12:00:00Z"
    }
  ]
}
```

---

### ErrorResponse

**Used By**: All error responses

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "object (optional)"
  }
}
```

---

## Endpoint Contracts

### GET /api/tasks

**Purpose**: Retrieve all tasks for the authenticated user

**Request**:
```
GET /api/tasks
Authorization: Bearer {jwt_token}
```

**Query Parameters**:
| Parameter | Type    | Required | Description                 |
|-----------|---------|----------|-----------------------------|
| completed | boolean | No       | Filter by completion status |

**Success Response**: `200 OK`
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "user_123",
      "title": "Task 1",
      "description": null,
      "completed": false,
      "created_at": "2026-02-17T10:00:00Z",
      "updated_at": "2026-02-17T10:00:00Z"
    }
  ]
}
```

**Error Responses**:
- `401 Unauthorized` - Missing or invalid token

---

### POST /api/tasks

**Purpose**: Create a new task

**Request**:
```
POST /api/tasks
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "title": "string",
  "description": "string (optional)"
}
```

**Success Response**: `201 Created`
```json
{
  "id": 1,
  "user_id": "user_123",
  "title": "New Task",
  "description": "Task description",
  "completed": false,
  "created_at": "2026-02-17T10:00:00Z",
  "updated_at": "2026-02-17T10:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized` - Missing or invalid token
- `422 Validation Error` - Invalid request body

**422 Example**:
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

### GET /api/tasks/{id}

**Purpose**: Retrieve a single task by ID

**Request**:
```
GET /api/tasks/{id}
Authorization: Bearer {jwt_token}
```

**Path Parameters**:
| Parameter | Type    | Required | Description |
|-----------|---------|----------|-------------|
| id        | integer | Yes      | Task ID     |

**Success Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": "user_123",
  "title": "Task 1",
  "description": null,
  "completed": false,
  "created_at": "2026-02-17T10:00:00Z",
  "updated_at": "2026-02-17T10:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Task does not exist or belongs to different user

**404 Example**:
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Task not found"
  }
}
```

---

### PUT /api/tasks/{id}

**Purpose**: Update an existing task (full update)

**Request**:
```
PUT /api/tasks/{id}
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "title": "string",
  "description": "string (optional)",
  "completed": "boolean"
}
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
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Task does not exist or belongs to different user
- `422 Validation Error` - Invalid request body

---

### DELETE /api/tasks/{id}

**Purpose**: Delete a task permanently

**Request**:
```
DELETE /api/tasks/{id}
Authorization: Bearer {jwt_token}
```

**Success Response**: `204 No Content`

**Error Responses**:
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Task does not exist or belongs to different user

---

### PATCH /api/tasks/{id}/complete

**Purpose**: Toggle task completion status

**Request**:
```
PATCH /api/tasks/{id}/complete
Authorization: Bearer {jwt_token}
```

**Success Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": "user_123",
  "title": "Task 1",
  "description": null,
  "completed": true,
  "created_at": "2026-02-17T10:00:00Z",
  "updated_at": "2026-02-17T11:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Task does not exist or belongs to different user

---

## Error Code Reference

| Status Code | Error Code       | Description                          |
|-------------|------------------|--------------------------------------|
| 401         | UNAUTHORIZED     | Missing or invalid JWT token         |
| 403         | FORBIDDEN        | Access denied to this resource       |
| 404         | NOT_FOUND        | Resource does not exist              |
| 422         | VALIDATION_ERROR | Request body validation failed       |

---

## CORS Configuration

**Allowed Origins**: Configured via `FRONTEND_URL` environment variable

**Allowed Methods**: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `OPTIONS`

**Allowed Headers**: `Content-Type`, `Authorization`

**Allow Credentials**: `false`

**Max Age**: `600` seconds

---

## Content Negotiation

**Request Format**: `application/json`

**Response Format**: `application/json`

**Character Encoding**: `UTF-8`

---

## Rate Limiting

**Status**: Not implemented in Phase-II

**Future Consideration**: Add rate limiting headers if needed in Phase-III

---

## References

- @specs/api/rest-endpoints.md - Source specification
- @specs/features/backend-task-crud.md - CRUD operation details
- @specs/features/backend-auth-verification.md - Authentication requirements
