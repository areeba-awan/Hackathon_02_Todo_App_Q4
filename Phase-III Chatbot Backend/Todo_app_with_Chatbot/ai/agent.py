"""AI agent for task management - Mock mode only."""
from typing import List, Dict, Any
import re


class CohereAgent:
    """AI agent for task management using mock responses."""

    def __init__(self):
        """Initialize agent in mock mode."""
        self.use_mock = True
        self.client = None
        self.model = "mock-only"
        self.temperature = 0.3

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get tool definitions for the agent."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_user_info",
                    "description": "Get current user information (email, name, etc.)",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task for the authenticated user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Task title (1-200 characters)"
                            },
                            "description": {
                                "type": "string",
                                "description": "Optional task description"
                            }
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List tasks for the authenticated user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filter": {
                                "type": "string",
                                "enum": ["all", "pending", "completed"],
                                "description": "Filter by completion status"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as complete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "ID of the task to complete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task permanently",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "ID of the task to delete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update a task's title or description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "ID of the task to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title (optional)"
                            },
                            "description": {
                                "type": "string",
                                "description": "New description (optional)"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]

    async def chat(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]] = None,
        temperature: float = None
    ) -> Any:
        """Generate mock response - no API calls."""
        return self._create_mock_response(messages, tools)

    def _create_mock_response(self, messages: List[Dict[str, str]], tools: List[Dict[str, Any]] = None) -> Any:
        """Create a mock response with proper intent detection."""
        user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break

        # Roman Urdu to English mapping
        roman_urdu_map = {
            'add': ['add', 'banao', 'likho', 'naya', 'create', 'yaad', 'rakhna', 'bana'],
            'list': ['list', 'dikhao', 'dekho', 'sab', 'show', 'view', 'dikha'],
            'complete': ['complete', 'done', 'khatam', 'finish', 'mark', 'check', 'pura', 'kro', 'kar'],
            'delete': ['delete', 'remove', 'hatao', 'cancel', 'mita', 'mitao'],
            'update': ['update', 'edit', 'change', 'badlo', 'modify', 'rename'],
            'user_info': ['profile', 'meri profile', 'mere profile', 'mera profile', 'my profile', 'my info', 'meri info', 'mere info', 'account', 'email', 'kaun hoon', 'kon hoon', 'who am i', 'about me']
        }

        # Roman Urdu words for language detection
        roman_urdu_words = ['banao', 'likho', 'dikhao', 'dekho', 'sab', 'mere', 'khatam', 'hatao', 'mita', 'badlo', 'kya', 'kaisa', 'kaise', 'theek', 'shukriya', 'dhanyavaad', 'shukria', 'madad', 'kar', 'sakte', 'ho', 'tak', 'salam', 'assalam', 'salaam', 'ek', 'to', 'ye', 'rha', 'ni', 'de', 'kr', 'ha', 'hain', 'kro', 'nahi', 'aur', 'database', 'table', 'ja', 'rhe']

        user_message_lower = user_message.lower()

        # Detect if user is using Roman Urdu
        is_roman_urdu = any(word in user_message_lower for word in roman_urdu_words)

        # Extract task ID - improved patterns for better matching
        task_id = None
        task_title = None
        patterns = [
            r'(?:task|tak|id)\s+#?(\d+)',    # "task 3", "tak 1", "id 5", "task #3"
            r'#(\d+)',                        # "#3"
            r'\b(\d+)\s+(?:task|tak)\b',    # "3 task" or "1 tak"
        ]

        for pattern in patterns:
            match = re.search(pattern, user_message_lower)
            if match:
                task_id = match.group(1)
                break

        # If no task ID found, try to extract task title
        if not task_id:
            words = user_message_lower.split()
            for i, word in enumerate(words):
                if word in ['task', 'tak', 'complete', 'delete', 'edit', 'update', 'mark', 'remove', 'hatao', 'mita', 'badlo', 'kro', 'kr']:
                    # Get everything after this word, excluding common stop words
                    remaining = words[i+1:]
                    if remaining and remaining[0] not in ['as', 'to', 'the', 'a', 'an', 'id']:
                        task_title = " ".join(remaining)
                        break

            # If still no task_title, default to "1" for task_id
            if not task_title:
                task_id = "1"

        # Detect intent and create tool call
        tool_name = None
        response_text = None

        # Task-related intents - ALWAYS create tool calls for these
        if any(word in user_message_lower for word in roman_urdu_map['user_info']):
            tool_name = "get_user_info"
            response_text = "Aapki information dekh rahe hain..." if is_roman_urdu else "Fetching your information..."
        elif any(word in user_message_lower for word in roman_urdu_map['add']):
            tool_name = "add_task"
            words = user_message_lower.split()
            # Find the add keyword and get everything after it
            title = ""
            for i, word in enumerate(words):
                if word in roman_urdu_map['add']:
                    title = " ".join(words[i+1:])
                    break
            if not title:
                title = "New task"
            response_text = f"Adding task: {title}" if not is_roman_urdu else f"Task add ho raha hai: {title}"
        elif any(word in user_message_lower for word in roman_urdu_map['list']):
            tool_name = "list_tasks"
            response_text = "Aapke tasks dekh rahe hain..." if is_roman_urdu else "Fetching your tasks..."
        elif any(word in user_message_lower for word in roman_urdu_map['complete']):
            tool_name = "complete_task"
            response_text = f"Task {task_id} complete ho gaya!" if is_roman_urdu else f"Marking task {task_id} as done..."
        elif any(word in user_message_lower for word in roman_urdu_map['delete']):
            tool_name = "delete_task"
            response_text = f"Task {task_id} delete ho gaya!" if is_roman_urdu else f"Deleting task {task_id}..."
        elif any(word in user_message_lower for word in roman_urdu_map['update']):
            tool_name = "update_task"
            words = user_message_lower.split()
            # Find where the new title starts (after "as", "to", etc.)
            title = ""
            for i, word in enumerate(words):
                if word in ['as', 'to', 'badlo', 'kr', 'kro']:
                    title = " ".join(words[i+1:])
                    break
            if not title:
                title = " ".join(words[2:]) if len(words) > 2 else "Updated task"
            task_title = title  # Set task_title for MockFunction
            response_text = f"Updating task {task_id} to: {title}" if not is_roman_urdu else f"Task {task_id} ko update ho raha hai: {title}"
        # Greeting intents - NO tool calls
        elif any(word in user_message_lower for word in ["hello", "hi", "hey", "greetings", "salam", "assalam", "salaam", "kya", "halo"]):
            if is_roman_urdu:
                response_text = "👋 Salam! Main aapka AI task assistant hoon. Main aapke tasks ko manage karne mein madad kar sakta hoon. Aap mujhe add, list, complete, delete, ya update tasks karne ke liye kah sakte hain."
            else:
                response_text = "👋 Hello! I'm your AI task assistant. I can help you manage your tasks. You can ask me to add, list, complete, delete, or update tasks."
        elif any(word in user_message_lower for word in ["how are you", "how are u", "how r u", "how's it going", "what's up", "kaisa", "kaise", "theek"]):
            if is_roman_urdu:
                response_text = "Main bilkul theek hoon, shukriya poochne ke liye! 😊 Main aapke tasks ko manage karne mein madad karne ke liye yahan hoon. Aap kya karna chahte hain?"
            else:
                response_text = "I'm doing great, thanks for asking! 😊 I'm here to help you manage your tasks. What would you like to do?"
        elif any(word in user_message_lower for word in ["thanks", "thank you", "appreciate", "thanks a lot", "shukriya", "dhanyavaad", "shukria"]):
            if is_roman_urdu:
                response_text = "Khush rahiye! Madad karne mein khushi hui. Kya aur kuch karna hai?"
            else:
                response_text = "You're welcome! Happy to help. Is there anything else you'd like me to do with your tasks?"
        elif any(word in user_message_lower for word in ["help", "what can you do", "capabilities", "what do you do", "madad", "kya kar sakte"]):
            if is_roman_urdu:
                response_text = "Main aapke liye ye kar sakta hoon:\n• Naye tasks add karna\n• Sab tasks dikhana\n• Tasks ko complete karna\n• Tasks ko delete karna\n• Task details ko update karna\n\nBas mujhe naturally poochiye!"
            else:
                response_text = "I can help you with:\n• Add new tasks\n• List all your tasks\n• Mark tasks as complete\n• Delete tasks\n• Update task details\n\nJust ask me naturally!"
        else:
            if is_roman_urdu:
                response_text = f"Main aapke tasks ko manage karne mein madad karne ke liye yahan hoon! Aap mujhe add, list, complete, delete, ya update tasks karne ke liye kah sakte hain. Kya karna hai?"
            else:
                response_text = f"I'm here to help with your tasks! You can ask me to add, list, complete, delete, or update tasks. What would you like to do?"

        # Create mock response object
        class MockChoice:
            def __init__(self, tool_name, response_text, task_id_val=None, task_title_val=None):
                self.message = MockMessage(tool_name, response_text, task_id_val, task_title_val)

        class MockMessage:
            def __init__(self, tool_name, response_text, task_id_val=None, task_title_val=None):
                self.content = response_text
                self.tool_calls = []
                if tool_name:
                    self.tool_calls = [MockToolCall(tool_name, user_message_lower, task_id_val, task_title_val)]

        class MockToolCall:
            def __init__(self, tool_name, user_msg, task_id_val, task_title_val=None):
                self.function = MockFunction(tool_name, user_msg, task_id_val, task_title_val)

        class MockFunction:
            def __init__(self, tool_name, user_msg, task_id_val, task_title_val=None):
                self.name = tool_name
                words = user_msg.split()

                # Escape quotes in strings for JSON
                def escape_json(s):
                    return s.replace('"', '\\"').replace('\n', '\\n')

                if tool_name == "add_task":
                    # For add, use task_title if available, otherwise extract from message
                    if task_title_val:
                        title = escape_json(task_title_val)
                    else:
                        title = escape_json(" ".join(words[1:]) if len(words) > 1 else "New task")
                    self.arguments = f'{{"title": "{title}", "description": ""}}'
                elif tool_name == "complete_task":
                    # Use task_id if available, otherwise default to 1
                    tid = task_id_val if task_id_val else "1"
                    self.arguments = f'{{"task_id": {tid}}}'
                elif tool_name == "delete_task":
                    # Use task_id if available, otherwise default to 1
                    tid = task_id_val if task_id_val else "1"
                    self.arguments = f'{{"task_id": {tid}}}'
                elif tool_name == "update_task":
                    # For update, use task_title if available
                    tid = task_id_val if task_id_val else "1"
                    if task_title_val:
                        update_title = escape_json(task_title_val)
                    else:
                        update_title = escape_json(" ".join(words[2:]) if len(words) > 2 else "Updated task")
                    self.arguments = f'{{"task_id": {tid}, "title": "{update_title}"}}'
                elif tool_name == "list_tasks":
                    self.arguments = '{"filter": "all"}'
                else:
                    self.arguments = '{}'

        class MockResponse:
            def __init__(self, tool_name, response_text, task_id_val=None, task_title_val=None):
                self.choices = [MockChoice(tool_name, response_text, task_id_val, task_title_val)]

        return MockResponse(tool_name, response_text, task_id, task_title)


# Global agent instance
agent = CohereAgent()
