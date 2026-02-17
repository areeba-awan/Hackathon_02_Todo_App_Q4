from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    """
    User entity for authentication.
    """
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(..., unique=True, index=True, max_length=255)
    name: str = Field(..., max_length=255)
    hashed_password: str = Field(..., max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Task(SQLModel, table=True):
    """
    Task entity representing a user's todo item.

    Stored in 'tasks' table with user isolation via user_id field.
    All queries MUST filter by user_id to ensure data privacy.
    """

    __tablename__ = "tasks"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Owner's user ID from JWT token (indexed for efficient filtering)
    user_id: str = Field(..., max_length=255, index=True)

    # Task title (required, 1-200 characters)
    title: str = Field(..., max_length=200)

    # Optional task description
    description: Optional[str] = Field(default=None)

    # Completion status (default: not completed)
    completed: bool = Field(default=False)

    # Timestamps (UTC)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
