"""Conversation and Message models for chat history."""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class Conversation(SQLModel, table=True):
    """Conversation session for chat history.
    
    Stored in 'conversations' table with user isolation via user_id field.
    All queries MUST filter by user_id to ensure data privacy.
    """
    
    __tablename__ = "conversations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        unique=True,
        index=True,
        max_length=255
    )
    user_id: str = Field(..., max_length=255, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    """Individual chat message.
    
    Stored in 'messages' table, linked to conversations via conversation_id.
    Messages inherit user isolation from their parent conversation.
    """
    
    __tablename__ = "messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: str = Field(..., max_length=255, index=True)
    role: str = Field(..., max_length=50)  # 'user' or 'assistant'
    content: str = Field(..., max_length=10000)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
