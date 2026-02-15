"""Task data model for the in-memory todo application with advanced features."""

from dataclasses import dataclass, field
from typing import List, Optional
import re
from datetime import datetime


# Constants for validation
VALID_PRIORITIES = {"HIGH", "MEDIUM", "LOW"}
VALID_RECURRENCE = {"DAILY", "WEEKLY", "MONTHLY", "NONE"}
MAX_TAGS = 5
TAG_PATTERN = re.compile(r"^[a-z]+(-[a-z]+)*$")


def validate_priority(priority: str) -> str:
    """Validate and normalize priority value.

    Args:
        priority: Priority string to validate

    Returns:
        Normalized priority string (uppercase)

    Raises:
        ValueError: If priority is not valid
    """
    if not priority:
        return "MEDIUM"
    normalized = priority.strip().upper()
    if normalized not in VALID_PRIORITIES:
        raise ValueError(
            f"Invalid priority '{priority}'. Must be HIGH, MEDIUM, or LOW."
        )
    return normalized


def validate_tags(tags: List[str]) -> List[str]:
    """Validate tag list.

    Args:
        tags: List of tag strings to validate

    Returns:
        Validated and normalized tag list

    Raises:
        ValueError: If tags exceed max count or have invalid format
    """
    if not tags:
        return []

    if len(tags) > MAX_TAGS:
        raise ValueError(
            f"Maximum {MAX_TAGS} tags allowed. You have {len(tags)} tags."
        )

    validated = []
    for tag in tags:
        normalized = tag.strip().lower()
        if not normalized:
            continue
        if not TAG_PATTERN.match(normalized):
            raise ValueError(
                f"Invalid tag '{tag}'. Tags must be lowercase with hyphens "
                "(e.g., 'work-projects', 'home-errands')."
            )
        if normalized not in validated:
            validated.append(normalized)

    return validated


def validate_due_date(due_date: Optional[str]) -> Optional[str]:
    """Validate due date format.

    Args:
        due_date: Due date string in YYYY-MM-DD format

    Returns:
        Validated date string or None

    Note:
        Basic format check.
    """
    if not due_date:
        return None
    due_date = due_date.strip()
    if len(due_date) == 10 and due_date[4] == "-" and due_date[7] == "-":
        try:
            # More rigorous check for actual date validity
            datetime.strptime(due_date, "%Y-%m-%d")
            return due_date
        except ValueError:
            return None
    return None


def validate_due_datetime(due_datetime: Optional[str]) -> Optional[str]:
    """Validate due datetime format.

    Args:
        due_datetime: Due datetime string in YYYY-MM-DD HH:MM format

    Returns:
        Validated datetime string or None
    """
    if not due_datetime:
        return None
    due_datetime = due_datetime.strip()
    try:
        dt = datetime.strptime(due_datetime, "%Y-%m-%d %H:%M")
        return dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return None


def validate_recurrence(recurrence: Optional[str]) -> str:
    """Validate recurrence type.

    Args:
        recurrence: Recurrence type (DAILY, WEEKLY, MONTHLY, NONE)

    Returns:
        Normalized recurrence string
    """
    if not recurrence:
        return "NONE"
    normalized = recurrence.strip().upper()
    if normalized not in VALID_RECURRENCE:
        return "NONE"
    return normalized


@dataclass
class Task:
    """Represents a single todo task with advanced features.

    Attributes:
        id: Unique identifier (1-based, sequential, auto-assigned)
        title: The task title (non-empty string)
        description: Additional details about the task
        is_complete: Whether the task is completed
        priority: Task priority level (HIGH, MEDIUM, LOW)
        tags: List of category labels (max 5, lowercase hyphenated)
        due_date: Optional due date in YYYY-MM-DD format (legacy)
        due_datetime: Optional due datetime in YYYY-MM-DD HH:MM format
        recurrence: Recurrence rule (DAILY, WEEKLY, MONTHLY, NONE)
        parent_id: ID of the task this instance was generated from
        reminder_sent: Whether the notification has been triggered
        order: Numeric value for manual sorting
    """
    id: int
    title: str
    description: str = ""
    is_complete: bool = False
    priority: str = "MEDIUM"
    tags: List[str] = field(default_factory=list)
    due_date: Optional[str] = None
    due_datetime: Optional[str] = None
    recurrence: str = "NONE"
    parent_id: Optional[int] = None
    reminder_sent: bool = False
    order: int = 0

    def __post_init__(self) -> None:
        """Validate and normalize fields after initialization."""
        self.description = self.description.strip()
        self.priority = validate_priority(self.priority)
        self.tags = validate_tags(self.tags)
        self.due_date = validate_due_date(self.due_date)
        self.due_datetime = validate_due_datetime(self.due_datetime)
        self.recurrence = validate_recurrence(self.recurrence)


    def to_dict(self) -> dict:
        """Convert task to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the task
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.is_complete,
            "priority": self.priority,
            "tags": self.tags,
            "due_date": self.due_date,
            "due_datetime": self.due_datetime,
            "recurrence": self.recurrence,
            "parent_id": self.parent_id,
            "reminder_sent": self.reminder_sent,
            "order": self.order,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create Task from dictionary (JSON deserialization).

        Args:
            data: Dictionary with task data

        Returns:
            New Task instance
        """
        return cls(
            id=data.get("id", 0),
            title=data.get("title", ""),
            description=data.get("description", ""),
            is_complete=data.get("completed", False),
            priority=data.get("priority", "MEDIUM"),
            tags=data.get("tags", []),
            due_date=data.get("due_date"),
            due_datetime=data.get("due_datetime"),
            recurrence=data.get("recurrence", "NONE"),
            parent_id=data.get("parent_id"),
            reminder_sent=data.get("reminder_sent", False),
            order=data.get("order", 0),
        )


    def get_priority_indicator(self) -> str:
        """Get single-character priority indicator for display.

        Returns:
            'H' for HIGH, 'M' for MEDIUM, 'L' for LOW
        """
        return self.priority[0]

    def get_tags_display(self, max_length: int = 15) -> str:
        """Get comma-separated tags for display.

        Args:
            max_length: Maximum display length before truncation

        Returns:
            Comma-separated tag string, truncated if needed
        """
        if not self.tags:
            return ""
        tags_str = ", ".join(self.tags)
        if len(tags_str) > max_length:
            return tags_str[: max_length - 3] + "..."
        return tags_str


class TaskFilter:
    """Encapsulates the current filter state for viewing tasks."""

    def __init__(
        self,
        status: str = "all",
        priority: str = "all",
        tag: Optional[str] = None,
    ) -> None:
        """Initialize task filter.

        Args:
            status: Filter by completion status (all, pending, complete)
            priority: Filter by priority level
            tag: Filter by exact tag match
        """
        self.status = status if status in ("all", "pending", "complete") else "all"
        self.priority = (
            priority.upper()
            if priority in ("HIGH", "MEDIUM", "LOW")
            else "all"
        )
        self.tag = tag.strip().lower() if tag else None

    def matches(self, task: Task) -> bool:
        """Check if task matches all filter criteria.

        Args:
            task: Task to check

        Returns:
            True if task matches all active filter criteria
        """
        # Status filter
        if self.status != "all":
            if self.status == "pending" and task.is_complete:
                return False
            if self.status == "complete" and not task.is_complete:
                return False

        # Priority filter
        if self.priority != "all" and task.priority != self.priority:
            return False

        # Tag filter
        if self.tag and self.tag not in task.tags:
            return False

        return True

    def is_active(self) -> bool:
        """Check if any filter is active.

        Returns:
            True if any filter criteria are set
        """
        return (
            self.status != "all"
            or self.priority != "all"
            or self.tag is not None
        )

    def reset(self) -> None:
        """Reset all filters to default values."""
        self.status = "all"
        self.priority = "all"
        self.tag = None


class SortMode:
    """Enumeration of available sorting behaviors."""

    PRIORITY = "priority"
    ALPHA = "alpha"
    DATE_ADDED = "date_added"
    MANUAL = "manual"

    _VALID_MODES = {PRIORITY, ALPHA, DATE_ADDED, MANUAL}

    def __init__(self, mode: str = DATE_ADDED) -> None:
        """Initialize sort mode.

        Args:
            mode: Sort mode string

        Raises:
            ValueError: If mode is not valid
        """
        normalized = mode.lower()
        if normalized not in self._VALID_MODES:
            raise ValueError(
                f"Invalid sort mode '{mode}'. "
                f"Must be: {', '.join(sorted(self._VALID_MODES))}"
            )
        self.mode = normalized

    @classmethod
    def valid_modes(cls) -> List[str]:
        """Get list of valid sort mode values.

        Returns:
            List of valid mode strings
        """
        return sorted(cls._VALID_MODES)

    def get_sort_key(self, task: Task):
        """Get sort key function for this sort mode.

        Args:
            task: Task to get key for

        Returns:
            Tuple suitable for sorting
        """
        if self.mode == self.PRIORITY:
            # HIGH (3) > MEDIUM (2) > LOW (1), so invert for ascending sort
            priority_map = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
            return (priority_map.get(task.priority, 0), task.order, task.id)
        elif self.mode == self.ALPHA:
            return (task.title.lower(), task.order, task.id)
        elif self.mode == self.DATE_ADDED:
            # Newest first (higher ID first)
            return (-task.id,)
        else:  # MANUAL
            return (task.order, task.id)


class TaskList:
    """In-memory collection of tasks with new Task model.

    Maintains tasks in insertion order and generates unique sequential IDs.
    """

    def __init__(self) -> None:
        self.tasks: List[Task] = []
        self._next_id: int = 1

    def add(
        self,
        title: str,
        description: str = "",
        priority: str = "MEDIUM",
        tags: List[str] = None,
        due_date: str = None,
    ) -> Task:
        """Add a new task with auto-assigned ID.

        Args:
            title: The task title (non-empty, validated by caller)
            description: Optional task description
            priority: Task priority (HIGH, MEDIUM, LOW)
            tags: Optional list of tags
            due_date: Optional due date in YYYY-MM-DD format

        Returns:
            The newly created Task
        """
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags or [],
            due_date=due_date,
        )
        self.tasks.append(task)
        self._next_id += 1
        return task

    def add_from_dict(self, data: dict) -> Task:
        """Add a task from dictionary (for loading from JSON).

        Args:
            data: Dictionary with task data

        Returns:
            The newly created Task
        """
        task = Task.from_dict(data)
        if task.id >= self._next_id:
            self._next_id = task.id + 1
        self.tasks.append(task)
        return task

    def get_by_id(self, task_id: int) -> Task | None:
        """Find task by ID.

        Args:
            task_id: The task identifier to search for

        Returns:
            The Task if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_all(self) -> List[Task]:
        """Return all tasks in insertion order.

        Returns:
            Copy of the tasks list to prevent external modification
        """
        return self.tasks.copy()

    def update(
        self,
        task_id: int,
        title: str = None,
        description: str = None,
        priority: str = None,
        tags: List[str] = None,
        due_date: str = None,
    ) -> bool:
        """Update task fields by ID.

        Args:
            task_id: The task identifier
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)
            tags: New tags list (optional)
            due_date: New due date (optional)

        Returns:
            True if task was updated, False if not found
        """
        task = self.get_by_id(task_id)
        if task is not None:
            if title is not None:
                task.title = title.strip()
            if description is not None:
                task.description = description.strip()
            if priority is not None:
                task.priority = validate_priority(priority)
            if tags is not None:
                task.tags = validate_tags(tags)
            if due_date is not None:
                task.due_date = validate_due_date(due_date)
            return True
        return False

    def delete(self, task_id: int) -> bool:
        """Delete task by ID.

        Args:
            task_id: The task identifier

        Returns:
            True if task was deleted, False if not found
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False

    def mark_complete(self, task_id: int) -> bool:
        """Mark task as complete.

        Args:
            task_id: The task identifier

        Returns:
            True if task was marked, False if not found
        """
        task = self.get_by_id(task_id)
        if task is not None:
            task.is_complete = True
            return True
        return False

    def mark_incomplete(self, task_id: int) -> bool:
        """Mark task as incomplete.

        Args:
            task_id: The task identifier

        Returns:
            True if task was marked, False if not found
        """
        task = self.get_by_id(task_id)
        if task is not None:
            task.is_complete = False
            return True
        return False

    def move_task(self, task_id: int, direction: str) -> bool:
        """Move task up or down in manual sort order.

        Args:
            task_id: The task identifier
            direction: 'up' to decrease order, 'down' to increase order

        Returns:
            True if task was moved, False if not found or at boundary
        """
        task = self.get_by_id(task_id)
        if task is None:
            return False

        if direction == "up":
            task.order -= 1
        elif direction == "down":
            task.order += 1
        else:
            return False

        return True
