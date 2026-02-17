from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from backend.models.base import UUIDModel, TimestampMixin

if TYPE_CHECKING:
    from backend.models.todo import Todo


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)
    name: Optional[str] = Field(default=None, max_length=100)


class User(UserBase, UUIDModel, TimestampMixin, table=True):
    """User model for the application"""
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    password_hash: str = Field(nullable=False, max_length=255)
    todos: list["Todo"] = Relationship(back_populates="user")