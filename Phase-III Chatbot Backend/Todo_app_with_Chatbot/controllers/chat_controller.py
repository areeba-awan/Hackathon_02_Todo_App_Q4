"""Chat controller for handling AI chatbot requests."""
from fastapi import HTTPException
from sqlmodel import Session
from typing import Dict, Any, Optional, List
from ai.agent import agent
from ai.config import AIConfig
from services.conversation_service import ConversationService
from ai.tools import MCPTools
import json


class ChatController:
    """Controller for processing chat messages and managing conversations."""
    
    @staticmethod
    async def process_message(
        message: str,
        user_id: str,
        session: Session,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process a chat message and return AI response.

        Args:
            message: User's natural language message
            user_id: Authenticated user ID
            session: Database session
            conversation_id: Optional existing conversation ID

        Returns:
            Structured response with AI reply and optional task action
        """
        try:
            # Detect language
            roman_urdu_words = ['banao', 'likho', 'dikhao', 'dekho', 'sab', 'mere', 'khatam', 'hatao', 'mita', 'badlo', 'kya', 'kaisa', 'kaise', 'theek', 'shukriya', 'dhanyavaad', 'shukria', 'madad', 'kar', 'sakte', 'ho', 'tak', 'salam', 'assalam', 'salaam', 'ek', 'to', 'ye', 'rha', 'ni', 'de', 'kr', 'ha', 'hain', 'kro', 'nahi', 'aur', 'database', 'table', 'ja', 'rhe']
            is_roman_urdu = any(word in message.lower() for word in roman_urdu_words)

            # Get or create conversation
            if conversation_id:
                conversation = ConversationService.get_conversation(
                    session, conversation_id, user_id
                )
                if not conversation:
                    # Create new conversation if not found
                    conversation = ConversationService.create_conversation(
                        session, user_id
                    )
                    conversation_id = conversation.conversation_id
            else:
                conversation = ConversationService.create_conversation(
                    session, user_id
                )
                conversation_id = conversation.conversation_id

            # Save user message
            ConversationService.save_message(
                session, conversation_id, "user", message
            )

            # Load conversation history for context
            history = ConversationService.load_history(
                session, conversation_id, user_id, limit=10
            )

            # Build messages for AI
            messages = [
                {"role": msg.role, "content": msg.content}
                for msg in history
            ]

            # Get AI response with tools
            tools = agent.get_tools()
            response = await agent.chat(messages, tools)

            # Check if AI wants to call a tool
            if response.choices and response.choices[0].message.tool_calls:
                tool_call = response.choices[0].message.tool_calls[0]
                tool_result = await ChatController._execute_tool(
                    tool_call, user_id, session
                )

                # Format response based on success and language
                if tool_result.get("success"):
                    ai_response = ChatController._format_tool_response(tool_result, is_roman_urdu)
                else:
                    ai_response = tool_result.get("message", "Failed to complete action")

                # Save AI response
                ConversationService.save_message(
                    session, conversation_id, "assistant", ai_response
                )

                # Determine if response is a list (from list_tasks) or single task
                tool_data = tool_result.get("data") if tool_result.get("success") else None
                is_list = isinstance(tool_data, list)

                # For delete operations, tool_data is empty dict, so set to None
                if isinstance(tool_data, dict) and not tool_data:
                    tool_data = None

                return {
                    "success": True,
                    "message": tool_result.get("message", "Done"),
                    "data": {
                        "response": ai_response,
                        "conversation_id": conversation_id,
                        "task_action": ChatController._get_action_type(tool_call.function.name),
                        "task": tool_data if not is_list else None,
                        "tasks": tool_data if is_list else None
                    }
                }
            else:
                # Regular chat response
                ai_response = response.choices[0].message.content
                ConversationService.save_message(
                    session, conversation_id, "assistant", ai_response
                )

                return {
                    "success": True,
                    "message": "Chat response",
                    "data": {
                        "response": ai_response,
                        "conversation_id": conversation_id,
                        "task_action": "none"
                    }
                }

        except Exception as e:
            import logging
            logging.error(f"Chat error: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": f"Failed to process message: {str(e)}",
                "error": {
                    "code": "CHAT_ERROR",
                    "details": str(e)
                }
            }
    
    @staticmethod
    async def _execute_tool(
        tool_call,
        user_id: str,
        session: Session
    ) -> Dict[str, Any]:
        """Execute a tool call from AI.

        Args:
            tool_call: Tool call object from AI response
            user_id: Authenticated user ID
            session: Database session

        Returns:
            Tool execution result
        """
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)

        if tool_name == "get_user_info":
            return await MCPTools.get_user_info(
                user_id=user_id,
                session=session
            )
        elif tool_name == "add_task":
            return await MCPTools.add_task(
                title=tool_args.get("title"),
                description=tool_args.get("description"),
                user_id=user_id,
                session=session
            )
        elif tool_name == "list_tasks":
            return await MCPTools.list_tasks(
                filter=tool_args.get("filter", "all"),
                user_id=user_id,
                session=session
            )
        elif tool_name == "complete_task":
            task_id = tool_args.get("task_id")
            try:
                task_id = int(task_id) if task_id else None
            except (ValueError, TypeError):
                task_id = None

            return await MCPTools.complete_task(
                task_id=task_id,
                user_id=user_id,
                session=session
            )
        elif tool_name == "delete_task":
            task_id = tool_args.get("task_id")
            try:
                task_id = int(task_id) if task_id else None
            except (ValueError, TypeError):
                task_id = None

            return await MCPTools.delete_task(
                task_id=task_id,
                user_id=user_id,
                session=session
            )
        elif tool_name == "update_task":
            task_id = tool_args.get("task_id")
            try:
                task_id = int(task_id) if task_id else None
            except (ValueError, TypeError):
                task_id = None

            return await MCPTools.update_task(
                task_id=task_id,
                title=tool_args.get("title"),
                description=tool_args.get("description"),
                user_id=user_id,
                session=session
            )
        else:
            return {
                "success": False,
                "message": f"Unknown tool: {tool_name}",
                "error": {
                    "code": "UNKNOWN_TOOL",
                    "details": f"Tool {tool_name} is not available"
                }
            }
    
    @staticmethod
    def _format_tool_response(tool_result: Dict[str, Any], is_roman_urdu: bool = False) -> str:
        """Format tool result as natural language response."""
        if not tool_result.get("success"):
            message = tool_result.get("message", "Failed to complete action")
            if "not found" in message.lower():
                if is_roman_urdu:
                    return "❌ Task nahi mila. Task number check karke dobara try kariye."
                else:
                    return "❌ Task not found. Please check the task number and try again."
            return f"❌ {message}"

        data = tool_result.get("data", {})

        # Handle user info - check for email field
        if isinstance(data, dict) and data and "email" in data:
            user = data
            email = user.get('email', 'N/A')
            name = user.get('name', 'N/A')
            created = user.get('created_at', 'N/A')
            if is_roman_urdu:
                return f"👤 **Aapka Profile**\n\n📧 Email: {email}\n👤 Naam: {name}\n📅 Member since: {created}"
            else:
                return f"👤 **Your Profile**\n\n📧 Email: {email}\n👤 Name: {name}\n📅 Member since: {created}"

        # Handle delete (returns empty data)
        message = tool_result.get("message", "")
        if "deleted" in message.lower():
            if is_roman_urdu:
                return "Ho gaya! Task delete ho gaya."
            else:
                return "Done! Task has been deleted."

        # Handle single task (add, complete, delete, update)
        if isinstance(data, dict) and "task" in data:
            task = data["task"]
            title = task.get('title', 'Task')
            completed = task.get('completed', False)
            action = tool_result.get("message", "")

            if completed:
                if is_roman_urdu:
                    return f"Ho gaya! Task '{title}' complete mark ho gaya."
                else:
                    return f"Done! Task '{title}' marked as complete."
            else:
                # Check if it's an add or update based on the message
                if "added" in action.lower():
                    if is_roman_urdu:
                        return f"Ho gaya! Task '{title}' add ho gaya."
                    else:
                        return f"Done! Task '{title}' has been added."
                else:
                    if is_roman_urdu:
                        return f"Ho gaya! Task '{title}' update ho gaya."
                    else:
                        return f"Done! Task '{title}' has been updated."

        # Handle list of tasks
        if isinstance(data, list):
            tasks = data
            if not tasks:
                if is_roman_urdu:
                    return "📋 Aapke paas koi task nahi hai. Ek naya task add kariye!"
                else:
                    return "📋 You don't have any tasks yet. Add one to get started!"

            if is_roman_urdu:
                response = f"📋 Aapke paas {len(tasks)} task{'s' if len(tasks) != 1 else ''} hain:\n\n"
            else:
                response = f"📋 You have {len(tasks)} task{'s' if len(tasks) != 1 else ''}:\n\n"

            for i, task in enumerate(tasks, 1):
                status = "✅" if task.get("completed") else "⭕"
                title = task.get('title', 'Untitled')
                task_id = task.get('id', i)
                response += f"{i}. [{status}] {title} (ID: {task_id})\n"
            return response

        return tool_result.get("message", "✅ Done!")
    
    @staticmethod
    def _get_action_type(tool_name: str) -> str:
        """Get action type from tool name.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Action type string
        """
        action_map = {
            "add_task": "created",
            "list_tasks": "listed",
            "complete_task": "completed",
            "delete_task": "deleted",
            "update_task": "updated"
        }
        return action_map.get(tool_name, "none")
