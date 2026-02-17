# Database Schema Specification

**Database**: Neon PostgreSQL
**ORM**: SQLModel

## Connection Configuration

Database connection string must be provided via environment variable:

```
DATABASE_URL=postgresql://user:password@host.neon.tech/database?sslmode=require
```

## Table: tasks

Stores todo items for authenticated users.

### Schema Definition

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT title_length_check CHECK (LENGTH(title) >= 1 AND LENGTH(title) <= 200)
);
```

### Column Specifications

| Column      | Type                        | Nullable | Default              | Description                          |
|-------------|-----------------------------|----------|----------------------|--------------------------------------|
| id          | SERIAL                      | No       | auto-increment       | Primary key                          |
| user_id     | VARCHAR(255)                | No       | -                    | Owner's user ID from JWT token       |
| title       | VARCHAR(200)                | No       | -                    | Task title (1-200 chars)             |
| description | TEXT                        | Yes      | NULL                 | Optional task description            |
| completed   | BOOLEAN                     | No       | FALSE                | Completion status                    |
| created_at  | TIMESTAMP WITH TIME ZONE    | No       | CURRENT_TIMESTAMP    | Record creation timestamp            |
| updated_at  | TIMESTAMP WITH TIME ZONE    | No       | CURRENT_TIMESTAMP    | Last update timestamp                |

### Indexes

```sql
-- Index for user-based filtering (required for all queries)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Composite index for user + completion filtering (optional optimization)
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

### Constraints

1. **Primary Key**: `id` uniquely identifies each task
2. **Not Null**: `user_id` and `title` are required fields
3. **Check Constraint**: `title` length must be between 1 and 200 characters
4. **User Isolation**: All queries MUST filter by `user_id` to ensure data isolation

## SQLModel Entity Definition

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(..., max_length=255, index=True)
    title: str = Field(..., max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Query Patterns

All database queries MUST include `user_id` filter:

### List Tasks for User
```sql
SELECT * FROM tasks WHERE user_id = :user_id;
```

### Filter by Completion Status
```sql
SELECT * FROM tasks 
WHERE user_id = :user_id 
  AND completed = :completed;
```

### Get Single Task
```sql
SELECT * FROM tasks 
WHERE user_id = :user_id 
  AND id = :task_id;
```

### Create Task
```sql
INSERT INTO tasks (user_id, title, description, completed)
VALUES (:user_id, :title, :description, FALSE)
RETURNING *;
```

### Update Task
```sql
UPDATE tasks 
SET title = :title, 
    description = :description, 
    completed = :completed,
    updated_at = CURRENT_TIMESTAMP
WHERE user_id = :user_id 
  AND id = :task_id
RETURNING *;
```

### Delete Task
```sql
DELETE FROM tasks 
WHERE user_id = :user_id 
  AND id = :task_id;
```

## Data Integrity Rules

1. **User Isolation**: Tasks without valid `user_id` cannot exist
2. **Title Validation**: Database enforces title length constraint
3. **Timestamp Management**: `updated_at` must be refreshed on every update
4. **Cascade Behavior**: Tasks are independent; no cascade deletes required

## Environment Variables

| Variable       | Required | Description                          |
|----------------|----------|--------------------------------------|
| DATABASE_URL   | Yes      | PostgreSQL connection string         |
