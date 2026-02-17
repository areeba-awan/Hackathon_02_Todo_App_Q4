# Data Model Specification

**Feature**: Backend API for Todo App
**Branch**: 002-backend-specs
**Created**: 2026-02-17
**Status**: Draft

---

## Overview

This document defines the SQLModel entity definitions for the backend database layer. All entities are derived from @specs/database/schema.md.

---

## Entity: Task

**Purpose**: Represents a user's todo item with full audit trail

**Table Name**: `tasks`

### Fields

| Field       | Type     | Required | Default     | Max Length | Index | Description                    |
|-------------|----------|----------|-------------|------------|-------|--------------------------------|
| id          | int      | Yes      | auto-increment | -      | PK    | Primary key                    |
| user_id     | str      | Yes      | -           | 255        | Yes   | Owner's user ID from JWT       |
| title       | str      | Yes      | -           | 200        | -     | Task title                     |
| description | str      | No       | NULL        | -          | -     | Optional task description      |
| completed   | bool     | Yes      | False       | -          | -     | Completion status              |
| created_at  | datetime | Yes      | utcnow()    | -          | -     | Record creation timestamp      |
| updated_at  | datetime | Yes      | utcnow()    | -          | -     | Last update timestamp          |

### SQLModel Definition

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """Task entity representing a user's todo item."""
    
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(..., max_length=255, index=True)
    title: str = Field(..., max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Database Indexes

```sql
-- Primary index for user-based filtering (required for all queries)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Composite index for user + completion filtering (optional optimization)
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

### Constraints

1. **Primary Key**: `id` uniquely identifies each task
2. **Not Null**: `user_id` and `title` are required fields
3. **Check Constraint**: `title` length must be between 1 and 200 characters
4. **User Isolation**: All queries MUST filter by `user_id`

### Validation Rules

```python
# Title validation
assert 1 <= len(title) <= 200

# User ID validation
assert len(user_id) > 0 and len(user_id) <= 255

# Completed is boolean
assert isinstance(completed, bool)
```

---

## Relationships

### User → Tasks

**Type**: One-to-Many (logical, no foreign key constraint)

**Description**: Each user can have multiple tasks. Tasks are isolated by user_id extracted from JWT token.

**Implementation Note**: No database-level foreign key since users are managed by Better Auth (separate service). User isolation enforced at application layer.

---

## Query Patterns

All queries MUST include `user_id` filter for data isolation.

### List All Tasks for User

```python
def list_tasks(session: Session, user_id: str, completed: Optional[bool] = None) -> list[Task]:
    statement = select(Task).where(Task.user_id == user_id)
    if completed is not None:
        statement = statement.where(Task.completed == completed)
    results = session.exec(statement)
    return results.all()
```

### Get Single Task

```python
def get_task(session: Session, task_id: int, user_id: str) -> Optional[Task]:
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = session.exec(statement)
    return result.first()
```

### Create Task

```python
def create_task(session: Session, user_id: str, title: str, description: Optional[str] = None) -> Task:
    task = Task(user_id=user_id, title=title, description=description)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### Update Task

```python
def update_task(session: Session, task_id: int, user_id: str, **update_data) -> Optional[Task]:
    task = get_task(session, task_id, user_id)
    if not task:
        return None
    for key, value in update_data.items():
        setattr(task, key, value)
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### Delete Task

```python
def delete_task(session: Session, task_id: int, user_id: str) -> bool:
    task = get_task(session, task_id, user_id)
    if not task:
        return False
    session.delete(task)
    session.commit()
    return True
```

### Toggle Completion

```python
def toggle_complete(session: Session, task_id: int, user_id: str) -> Optional[Task]:
    task = get_task(session, task_id, user_id)
    if not task:
        return None
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

---

## Timestamp Management

### created_at

- Set automatically on task creation
- Never modified after creation
- Uses UTC timezone

### updated_at

- Set automatically on task creation
- Updated on every task modification
- Uses UTC timezone
- Must be refreshed on PUT, PATCH operations

---

## Data Integrity Rules

1. **User Isolation**: Tasks without valid `user_id` cannot exist
2. **Title Validation**: Enforced at application and database level
3. **Timestamp Management**: `updated_at` refreshed on every update
4. **Cascade Behavior**: Tasks are independent; no cascade deletes required
5. **Soft Delete**: Not implemented; deletion is permanent

---

## Environment Variables

| Variable     | Required | Description                  | Example                                      |
|--------------|----------|------------------------------|----------------------------------------------|
| DATABASE_URL | Yes      | PostgreSQL connection string | postgresql://user:pass@host.neon.tech/db     |

---

## Migration Notes

**For Production Deployment**:

1. Create tasks table using SQLModel metadata:
   ```python
   SQLModel.metadata.create_all(engine)
   ```

2. Verify indexes are created:
   ```sql
   \di idx_tasks_user_id
   \di idx_tasks_user_completed
   ```

3. Test connection with simple query:
   ```python
   with Session(engine) as session:
       result = session.exec(select(Task).limit(1))
   ```

---

## References

- @specs/database/schema.md - Source specification
- @specs/features/backend-task-crud.md - CRUD operation requirements
- @specs/features/backend-auth-verification.md - user_id extraction
