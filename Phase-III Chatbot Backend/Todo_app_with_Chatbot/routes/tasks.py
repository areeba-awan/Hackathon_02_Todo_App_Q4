from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional

from db import get_session
from auth import get_current_user
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse

# Create router with /api/tasks prefix
router = APIRouter(prefix="/api/tasks", tags=["tasks"])


# =============================================================================
# GET /api/tasks - List all tasks for authenticated user
# =============================================================================

@router.get("", response_model=TaskListResponse)
async def list_tasks(
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session),
    completed: Optional[bool] = Query(None, description="Filter by completion status")
) -> TaskListResponse:
    """
    Retrieve all tasks for the authenticated user.
    
    Optionally filter by completion status using the 'completed' query parameter.
    Only returns tasks owned by the authenticated user (user isolation).
    """
    # Build query with mandatory user_id filter
    statement = select(Task).where(Task.user_id == user_id)
    
    # Apply optional completion filter
    if completed is not None:
        statement = statement.where(Task.completed == completed)
    
    # Order by created_at descending (newest first)
    statement = statement.order_by(Task.created_at.desc())
    
    # Execute query
    results = session.exec(statement)
    tasks = results.all()
    
    return TaskListResponse(tasks=tasks)


# =============================================================================
# POST /api/tasks - Create a new task
# =============================================================================

@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Create a new task for the authenticated user.
    
    The task is automatically associated with the authenticated user
    and marked as incomplete by default.
    """
    # Create task with user_id from authenticated context
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=False
    )
    
    # Add to database
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task


# =============================================================================
# GET /api/tasks/{id} - Get a single task by ID
# =============================================================================

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Retrieve a single task by ID.
    
    Only returns the task if it belongs to the authenticated user.
    Returns 404 if task not found or belongs to different user.
    """
    # Query with user_id filter for security
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    result = session.exec(statement)
    task = result.first()
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "message": "Task not found"
            }
        )
    
    return task


# =============================================================================
# PUT /api/tasks/{id} - Update an existing task (full update)
# =============================================================================

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Update an existing task (full update).
    
    All fields (title, description, completed) must be provided.
    Only updates if task belongs to authenticated user.
    """
    # Find task with ownership check
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    result = session.exec(statement)
    task = result.first()
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "message": "Task not found"
            }
        )
    
    # Update fields
    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed
    
    # Save changes
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task


# =============================================================================
# DELETE /api/tasks/{id} - Delete a task permanently
# =============================================================================

@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task permanently.
    
    Only deletes if task belongs to authenticated user.
    Returns 204 No Content on success.
    """
    # Find task with ownership check
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    result = session.exec(statement)
    task = result.first()
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "message": "Task not found"
            }
        )
    
    # Delete task
    session.delete(task)
    session.commit()
    
    return None


# =============================================================================
# PATCH /api/tasks/{id}/complete - Toggle task completion status
# =============================================================================

@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_complete(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Toggle task completion status (completed ↔ incomplete).
    
    Only toggles if task belongs to authenticated user.
    Updates the updated_at timestamp.
    """
    from datetime import datetime
    
    # Find task with ownership check
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    result = session.exec(statement)
    task = result.first()
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "message": "Task not found"
            }
        )
    
    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    
    # Save changes
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task
