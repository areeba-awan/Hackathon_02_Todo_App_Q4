"""MCP tool implementations for AI chatbot task operations."""
from sqlmodel import Session, select
from typing import Optional, List, Dict, Any
from models import Task, User
from schemas import TaskCreate
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MCPTools:
    """MCP tool implementations for task operations.

    All tools enforce user isolation and authentication.
    """

    @staticmethod
    async def get_user_info(
        user_id: str,
        session: Session
    ) -> Dict[str, Any]:
        """Get user information by user_id."""
        try:
            # Try to convert user_id to int if it's numeric
            try:
                user_id_int = int(user_id)
                statement = select(User).where(User.id == user_id_int)
            except (ValueError, TypeError):
                # If not numeric, search by email or other field
                statement = select(User).where(User.email == user_id)

            user = session.exec(statement).first()

            if not user:
                return {
                    "success": False,
                    "message": "User not found",
                    "data": None
                }

            return {
                "success": True,
                "message": "User info retrieved",
                "data": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "created_at": user.created_at.isoformat()
                }
            }
        except Exception as e:
            logger.error(f"Failed to get user info: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": f"Failed to get user info: {str(e)}",
                "data": None
            }

    @staticmethod
    async def add_task(
        title: str,
        description: Optional[str],
        user_id: str,
        session: Session
    ) -> Dict[str, Any]:
        """Add a new task for the authenticated user."""
        try:
            logger.info(f"Adding task: title={title}, user_id={user_id}")
            task = Task(
                user_id=user_id,
                title=title,
                description=description,
                completed=False
            )
            session.add(task)
            session.commit()
            session.refresh(task)

            logger.info(f"Task added successfully: id={task.id}, user_id={task.user_id}")

            return {
                "success": True,
                "message": f"Task '{title}' added successfully",
                "data": {
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat()
                    }
                }
            }
        except Exception as e:
            logger.error(f"Failed to add task: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": f"Failed to add task: {str(e)}",
                "error": {
                    "code": "TASK_CREATION_ERROR",
                    "details": str(e)
                }
            }

    @staticmethod
    async def list_tasks(
        filter: str,
        user_id: str,
        session: Session
    ) -> Dict[str, Any]:
        """List tasks for the authenticated user."""
        try:
            logger.info(f"Listing tasks for user_id={user_id}, filter={filter}")
            statement = select(Task).where(Task.user_id == user_id)

            if filter == "pending":
                statement = statement.where(Task.completed == False)
            elif filter == "completed":
                statement = statement.where(Task.completed == True)

            statement = statement.order_by(Task.created_at.desc())
            results = session.exec(statement)
            tasks = results.all()

            logger.info(f"Found {len(tasks)} tasks")

            task_list = [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "completed": t.completed,
                    "created_at": t.created_at.isoformat()
                }
                for t in tasks
            ]

            return {
                "success": True,
                "message": f"Retrieved {len(task_list)} tasks",
                "data": task_list
            }
        except Exception as e:
            logger.error(f"Failed to list tasks: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": f"Failed to list tasks: {str(e)}",
                "error": {
                    "code": "TASK_LIST_ERROR",
                    "details": str(e)
                }
            }

    @staticmethod
    async def find_task_by_title(
        title: str,
        user_id: str,
        session: Session
    ) -> Optional[Task]:
        """Find a task by title for the user."""
        try:
            statement = select(Task).where(
                Task.user_id == user_id,
                Task.title.ilike(f"%{title}%")
            )
            task = session.exec(statement).first()
            return task
        except Exception as e:
            logger.error(f"Error finding task by title: {str(e)}")
            return None

    @staticmethod
    async def complete_task(
        task_id: Optional[int] = None,
        task_title: Optional[str] = None,
        user_id: str = None,
        session: Session = None
    ) -> Dict[str, Any]:
        """Mark a task as complete by ID or title."""
        try:
            task = None

            # Try to find by ID first
            if task_id:
                statement = select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
                task = session.exec(statement).first()

            # If not found by ID, try by title
            if not task and task_title:
                task = await MCPTools.find_task_by_title(task_title, user_id, session)

            if not task:
                return {
                    "success": False,
                    "message": f"Task not found",
                    "error": {
                        "code": "INVALID_TASK_ID",
                        "details": f"Task does not exist or you don't have permission"
                    }
                }

            task.completed = True
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)

            logger.info(f"Task completed: task_id={task.id}")

            return {
                "success": True,
                "message": f"Task '{task.title}' marked as complete",
                "data": {
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "completed": True,
                        "updated_at": task.updated_at.isoformat()
                    }
                }
            }
        except Exception as e:
            logger.error(f"Failed to complete task: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": f"Failed to complete task: {str(e)}",
                "error": {
                    "code": "TASK_COMPLETE_ERROR",
                    "details": str(e)
                }
            }

    @staticmethod
    async def delete_task(
        task_id: Optional[int] = None,
        task_title: Optional[str] = None,
        user_id: str = None,
        session: Session = None
    ) -> Dict[str, Any]:
        """Delete a task by ID or title."""
        try:
            task = None

            # Try to find by ID first
            if task_id:
                statement = select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
                task = session.exec(statement).first()

            # If not found by ID, try by title
            if not task and task_title:
                task = await MCPTools.find_task_by_title(task_title, user_id, session)

            if not task:
                return {
                    "success": False,
                    "message": f"Task not found",
                    "error": {
                        "code": "INVALID_TASK_ID",
                        "details": f"Task does not exist or you don't have permission"
                    }
                }

            session.delete(task)
            session.commit()

            logger.info(f"Task deleted: task_id={task.id}")

            return {
                "success": True,
                "message": f"Task deleted successfully",
                "data": {}
            }
        except Exception as e:
            logger.error(f"Failed to delete task: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": f"Failed to delete task: {str(e)}",
                "error": {
                    "code": "TASK_DELETE_ERROR",
                    "details": str(e)
                }
            }

    @staticmethod
    async def update_task(
        task_id: Optional[int] = None,
        task_title: Optional[str] = None,
        user_id: str = None,
        session: Session = None,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update a task by ID or title."""
        try:
            task = None

            # Try to find by ID first
            if task_id:
                statement = select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
                task = session.exec(statement).first()

            # If not found by ID, try by title
            if not task and task_title:
                task = await MCPTools.find_task_by_title(task_title, user_id, session)

            if not task:
                return {
                    "success": False,
                    "message": f"Task not found",
                    "error": {
                        "code": "INVALID_TASK_ID",
                        "details": f"Task does not exist or you don't have permission"
                    }
                }

            if title:
                task.title = title
            if description:
                task.description = description

            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)

            logger.info(f"Task updated: task_id={task.id}")

            return {
                "success": True,
                "message": f"Task updated successfully",
                "data": {
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "updated_at": task.updated_at.isoformat()
                    }
                }
            }
        except Exception as e:
            logger.error(f"Failed to update task: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": f"Failed to update task: {str(e)}",
                "error": {
                    "code": "TASK_UPDATE_ERROR",
                    "details": str(e)
                }
            }


# Export tool functions for direct use
add_task = MCPTools.add_task
list_tasks = MCPTools.list_tasks
complete_task = MCPTools.complete_task
delete_task = MCPTools.delete_task
update_task = MCPTools.update_task
