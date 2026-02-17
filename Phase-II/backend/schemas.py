from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List

# =============================================================================
# Request Schemas
# =============================================================================

class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v or len(v) < 1 or len(v) > 200:
            raise ValueError('Title must be between 1 and 200 characters')
        return v.strip()


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(...)
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v or len(v) < 1 or len(v) > 200:
            raise ValueError('Title must be between 1 and 200 characters')
        return v.strip()


# =============================================================================
# Response Schemas
# =============================================================================

class TaskResponse(BaseModel):
    """Schema for task response."""
    
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class TaskListResponse(BaseModel):
    """Schema for list of tasks response."""
    
    tasks: List[TaskResponse]


# =============================================================================
# Error Schemas
# =============================================================================

class ErrorDetail(BaseModel):
    """Schema for error response."""
    
    code: str
    message: str
    details: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Schema for error response wrapper."""
    
    error: ErrorDetail
