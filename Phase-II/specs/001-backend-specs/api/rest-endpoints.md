# REST API Endpoints Specification

**Base Path**: `/api/tasks`
**Authentication**: Required for all endpoints (JWT Bearer token)

## Authentication

All endpoints require JWT authentication via the Authorization header:

```
Authorization: Bearer {jwt_token}
```

Token verification:
- Token must be valid and not expired
- Token must be signed with BETTER_AUTH_SECRET
- user_id extracted from token payload identifies the request context

## Endpoints

### GET /api/tasks

**Purpose**: Retrieve all tasks for the authenticated user

**Request Headers**:
```
Authorization: Bearer {jwt_token}
```

**Query Parameters**:
| Parameter | Type   | Required | Description                    |
|-----------|--------|----------|--------------------------------|
| completed | boolean| No       | Filter by completion status    |

**Response**: `200 OK`
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "user_123",
      "title": "Complete project",
      "description": "Finish the backend API",
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

**Request Headers**:
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "string (required, 1-200 chars)",
  "description": "string (optional)"
}
```

**Validation Rules**:
- `title`: Required, minimum 1 character, maximum 200 characters
- `description`: Optional, no length limit

**Response**: `201 Created`
```json
{
  "id": 1,
  "user_id": "user_123",
  "title": "Complete project",
  "description": "Finish the backend API",
  "completed": false,
  "created_at": "2026-02-17T10:00:00Z",
  "updated_at": "2026-02-17T10:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized` - Missing or invalid token
- `422 Validation Error` - Invalid request body

---

### GET /api/tasks/{id}

**Purpose**: Retrieve a single task by ID

**Path Parameters**:
| Parameter | Type    | Required | Description     |
|-----------|---------|----------|-----------------|
| id        | integer | Yes      | Task ID         |

**Request Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": "user_123",
  "title": "Complete project",
  "description": "Finish the backend API",
  "completed": false,
  "created_at": "2026-02-17T10:00:00Z",
  "updated_at": "2026-02-17T10:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Task belongs to another user
- `404 Not Found` - Task with ID does not exist

---

### PUT /api/tasks/{id}

**Purpose**: Update an existing task (full update)

**Path Parameters**:
| Parameter | Type    | Required | Description     |
|-----------|---------|----------|-----------------|
| id        | integer | Yes      | Task ID         |

**Request Headers**:
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "string (required, 1-200 chars)",
  "description": "string (optional)",
  "completed": "boolean (required)"
}
```

**Validation Rules**:
- `title`: Required, minimum 1 character, maximum 200 characters
- `description`: Optional
- `completed`: Required boolean

**Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": "user_123",
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "created_at": "2026-02-17T10:00:00Z",
  "updated_at": "2026-02-17T11:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Task belongs to another user
- `404 Not Found` - Task with ID does not exist
- `422 Validation Error` - Invalid request body

---

### DELETE /api/tasks/{id}

**Purpose**: Delete a task permanently

**Path Parameters**:
| Parameter | Type    | Required | Description     |
|-----------|---------|----------|-----------------|
| id        | integer | Yes      | Task ID         |

**Request Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response**: `204 No Content`

**Error Responses**:
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Task belongs to another user
- `404 Not Found` - Task with ID does not exist

---

### PATCH /api/tasks/{id}/complete

**Purpose**: Toggle task completion status

**Path Parameters**:
| Parameter | Type    | Required | Description     |
|-----------|---------|----------|-----------------|
| id        | integer | Yes      | Task ID         |

**Request Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": "user_123",
  "title": "Complete project",
  "description": "Finish the backend API",
  "completed": true,
  "created_at": "2026-02-17T10:00:00Z",
  "updated_at": "2026-02-17T11:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Task belongs to another user
- `404 Not Found` - Task with ID does not exist

---

## Error Response Format

All errors return consistent JSON format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {} 
  }
}
```

### Standard Error Codes

| Status Code | Error Code      | Description                          |
|-------------|-----------------|--------------------------------------|
| 401         | UNAUTHORIZED    | Missing or invalid JWT token         |
| 403         | FORBIDDEN       | Access denied to this resource       |
| 404         | NOT_FOUND       | Resource does not exist              |
| 422         | VALIDATION_ERROR| Request body validation failed       |

### Example Error Responses

**401 Unauthorized**:
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired token"
  }
}
```

**403 Forbidden**:
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Access denied to this resource"
  }
}
```

**404 Not Found**:
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Task not found"
  }
}
```

**422 Validation Error**:
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

## CORS Configuration

Backend must support Cross-Origin Resource Sharing (CORS) for frontend integration.

**Configuration**:
- Allowed origins: Configured via `FRONTEND_URL` environment variable
- Allowed methods: GET, POST, PUT, DELETE, PATCH, OPTIONS
- Allowed headers: Content-Type, Authorization
- Expose headers: (none required)
- Max age: 600 seconds
- Allow credentials: false

**Example CORS Headers**:
```
Access-Control-Allow-Origin: {FRONTEND_URL}
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```
