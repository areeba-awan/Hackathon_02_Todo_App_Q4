"""Chat router for AI chatbot endpoint."""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Optional
from pydantic import BaseModel, Field
from controllers.chat_controller import ChatController
from db import get_session
from auth import get_current_user

# Create router with /api/chat prefix
router = APIRouter(prefix="/api/chat", tags=["chat"])


# =============================================================================
# Request/Response Schemas
# =============================================================================

class ChatRequest(BaseModel):
    """Schema for chat request."""
    
    message: str = Field(..., min_length=1, max_length=1000)
    conversation_id: Optional[str] = Field(
        default=None,
        description="Optional conversation ID to continue existing conversation"
    )


class ChatResponseData(BaseModel):
    """Schema for chat response data."""
    
    response: str
    conversation_id: str
    task_action: str
    task: Optional[dict] = None
    tasks: Optional[list] = None


class ChatResponse(BaseModel):
    """Schema for chat response."""
    
    success: bool
    message: str
    data: ChatResponseData


class ErrorResponse(BaseModel):
    """Schema for error response."""
    
    error: dict


# =============================================================================
# POST /api/chat - Send message to AI chatbot
# =============================================================================

@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> ChatResponse:
    """
    Send a natural language message to the AI chatbot.

    The chatbot will:
    1. Understand the user's intent (add_task, list_tasks, complete_task, delete_task, update_task)
    2. Execute the appropriate action via MCP tools
    3. Return a structured response with the result

    All task operations are automatically scoped to the authenticated user.
    """
    # Validate message
    if not request.message or len(request.message.strip()) == 0:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "VALIDATION_ERROR",
                "message": "Message is required"
            }
        )

    # Process message
    result = await ChatController.process_message(
        message=request.message,
        user_id=user_id,
        session=session,
        conversation_id=request.conversation_id
    )

    # Always return success with the result data
    return ChatResponse(
        success=result.get("success", True),
        message=result.get("message", "Done"),
        data=ChatResponseData(
            response=result["data"]["response"],
            conversation_id=result["data"]["conversation_id"],
            task_action=result["data"].get("task_action", "none"),
            task=result["data"].get("task"),
            tasks=result["data"].get("tasks")
        )
    )
