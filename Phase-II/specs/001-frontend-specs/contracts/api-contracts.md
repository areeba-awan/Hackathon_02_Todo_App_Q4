# API Contracts: Frontend Specifications for Next.js Todo App

## Authentication Endpoints

### POST /api/auth/login
Login user and return JWT

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK)**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user_12345",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Invalid credentials"
}
```

### POST /api/auth/register
Register new user

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Response (201 Created)**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user_12345",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Response (400 Bad Request)**:
```json
{
  "error": "Email already exists"
}
```

### POST /api/auth/logout
Logout user and invalidate session

**Request Headers**:
```
Authorization: Bearer {token}
```

**Response (200 OK)**:
```json
{
  "message": "Successfully logged out"
}
```

### GET /api/auth/me
Get current user info

**Request Headers**:
```
Authorization: Bearer {token}
```

**Response (200 OK)**:
```json
{
  "user": {
    "id": "user_12345",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Unauthorized"
}
```

## Task Management Endpoints

### GET /api/tasks
Get user's tasks

**Request Headers**:
```
Authorization: Bearer {token}
```

**Response (200 OK)**:
```json
{
  "tasks": [
    {
      "id": "task_12345",
      "title": "Complete project proposal",
      "description": "Finish the project proposal document and submit to manager",
      "completed": false,
      "dueDate": "2026-02-20T10:00:00Z",
      "createdAt": "2026-02-15T14:30:00Z",
      "updatedAt": "2026-02-15T14:30:00Z",
      "userId": "user_12345"
    },
    {
      "id": "task_12346",
      "title": "Schedule team meeting",
      "description": "Arrange a team sync for next week",
      "completed": true,
      "dueDate": "2026-02-18T09:00:00Z",
      "createdAt": "2026-02-14T11:15:00Z",
      "updatedAt": "2026-02-14T16:45:00Z",
      "userId": "user_12345"
    }
  ]
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Unauthorized"
}
```

### POST /api/tasks
Create new task

**Request Headers**:
```
Authorization: Bearer {token}
```

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, fruits",
  "dueDate": "2026-02-16T18:00:00Z"
}
```

**Response (201 Created)**:
```json
{
  "task": {
    "id": "task_12347",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread, fruits",
    "completed": false,
    "dueDate": "2026-02-16T18:00:00Z",
    "createdAt": "2026-02-15T15:20:00Z",
    "updatedAt": "2026-02-15T15:20:00Z",
    "userId": "user_12345"
  }
}
```

**Response (400 Bad Request)**:
```json
{
  "error": "Title is required"
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Unauthorized"
}
```

### PUT /api/tasks/{id}
Update task

**Request Headers**:
```
Authorization: Bearer {token}
```

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true,
  "dueDate": "2026-02-20T10:00:00Z"
}
```

**Response (200 OK)**:
```json
{
  "task": {
    "id": "task_12345",
    "title": "Updated task title",
    "description": "Updated description",
    "completed": true,
    "dueDate": "2026-02-20T10:00:00Z",
    "createdAt": "2026-02-15T14:30:00Z",
    "updatedAt": "2026-02-15T16:30:00Z",
    "userId": "user_12345"
  }
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Unauthorized"
}
```

**Response (404 Not Found)**:
```json
{
  "error": "Task not found"
}
```

### DELETE /api/tasks/{id}
Delete task

**Request Headers**:
```
Authorization: Bearer {token}
```

**Response (200 OK)**:
```json
{
  "message": "Task deleted successfully"
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Unauthorized"
}
```

**Response (404 Not Found)**:
```json
{
  "error": "Task not found"
}
```