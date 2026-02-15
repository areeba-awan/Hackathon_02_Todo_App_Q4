"""Todo service for managing tasks with intermediate features."""

import json
import os
from typing import List, Optional
from src.models.task import (
    Task,
    TaskList,
    TaskFilter,
    SortMode,
    validate_priority,
    validate_tags,
    validate_due_date,
)


class TodoServiceError(Exception):
    """Base exception for todo service errors."""

    pass


class TaskNotFoundError(TodoServiceError):
    """Raised when a task is not found."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task #{task_id} not found")


class ValidationError(TodoServiceError):
    """Raised when validation fails."""

    pass


class PersistenceError(TodoServiceError):
    """Raised when save/load operations fail."""

    pass


# Default storage file location
DEFAULT_STORAGE_FILE = "tasks.json"


class TodoService:
    """Handles all operations on tasks including CRUD, search, filter, sort, and persistence.

    The service layer contains all business logic and validation.
    Data models (Task, TaskList) are simple containers with no behavior.
    """

    def __init__(self, storage_file: str = DEFAULT_STORAGE_FILE) -> None:
        """Initialize the todo service.

        Args:
            storage_file: Path to the JSON file for persistence
        """
        self._task_list = TaskList()
        self._storage_file = storage_file
        self._search_term: Optional[str] = None
        self._current_filter = TaskFilter()
        self._current_sort = SortMode()
        self._on_change_callbacks: List[callable] = []

    def add_change_callback(self, callback: callable) -> None:
        """Register a callback to be called on any task change.

        Args:
            callback: Function to call after changes
        """
        self._on_change_callbacks.append(callback)

    def _notify_change(self) -> None:
        """Notify all registered callbacks of a change."""
        for callback in self._on_change_callbacks:
            try:
                callback()
            except Exception:
                pass  # Don't let callback errors affect main operation

    def _trigger_save(self) -> None:
        """Trigger save and notify callbacks."""
        self._notify_change()

    # =========================================================================
    # CRUD Operations
    # =========================================================================

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "MEDIUM",
        tags: List[str] = None,
        due_date: str = None,
        due_datetime: str = None,
        recurrence: str = "NONE",
    ) -> Task:
        """Add a new task.

        Args:
            title: Non-empty string (whitespace preserved)
            description: Optional task description
            priority: Task priority (HIGH, MEDIUM, LOW)
            tags: Optional list of tags
            due_date: Optional due date in YYYY-MM-DD format (legacy)
            due_datetime: Optional due datetime in YYYY-MM-DD HH:MM format
            recurrence: Recurrence rule (DAILY, WEEKLY, MONTHLY, NONE)

        Returns:
            The created Task with assigned ID

        Raises:
            ValidationError: If title is empty or validation fails
        """
        if not title or title.strip() == "":
            raise ValidationError("Title cannot be empty.")

        # Validate inputs
        try:
            from src.models.task import (
                validate_priority,
                validate_tags,
                validate_due_date,
                validate_due_datetime,
                validate_recurrence,
            )

            priority = validate_priority(priority)
            tags = validate_tags(tags or [])
            due_date = validate_due_date(due_date)
            due_datetime = validate_due_datetime(due_datetime)
            recurrence = validate_recurrence(recurrence)
        except ValueError as e:
            raise ValidationError(str(e))

        task = Task(
            id=self._task_list._next_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date,
            due_datetime=due_datetime,
            recurrence=recurrence,
        )
        self._task_list.tasks.append(task)
        self._task_list._next_id += 1

        self._trigger_save()
        return task


    def get_all_tasks(self) -> List[Task]:
        """Return all tasks in insertion order.

        Returns:
            Copy of all tasks (empty list if none exist)
        """
        return self._task_list.get_all()

    def get_task(self, task_id: int) -> Task | None:
        """Get a single task by ID.

        Args:
            task_id: The unique task identifier

        Returns:
            The Task if found, None otherwise
        """
        return self._task_list.get_by_id(task_id)

    def update_task(
        self,
        task_id: int,
        title: str = None,
        description: str = None,
        priority: str = None,
        tags: List[str] = None,
        due_date: str = None,
        due_datetime: str = None,
        recurrence: str = "NONE",
    ) -> Task:
        """Update a task's fields.

        Args:
            task_id: The unique task identifier
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)
            tags: New tags list (optional)
            due_date: New due date (optional)
            due_datetime: New due datetime (optional)
            recurrence: New recurrence rule (optional)

        Returns:
            The updated Task

        Raises:
            TaskNotFoundError: If task is not found
            ValidationError: If validation fails
        """
        task = self._task_list.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        # Validate inputs if provided
        if title is not None and title.strip() == "":
            raise ValidationError("Title cannot be empty.")

        try:
            from src.models.task import (
                validate_priority,
                validate_tags,
                validate_due_date,
                validate_due_datetime,
                validate_recurrence,
            )

            if priority is not None:
                priority = validate_priority(priority)
            if tags is not None:
                tags = validate_tags(tags)
            if due_date is not None:
                due_date = validate_due_date(due_date)
            if due_datetime is not None:
                due_datetime = validate_due_datetime(due_datetime)
                # Reset reminder flag if due time changes
                if due_datetime != task.due_datetime:
                    task.reminder_sent = False
            if recurrence is not None:
                recurrence = validate_recurrence(recurrence)
        except ValueError as e:
            raise ValidationError(str(e))

        success = self._task_list.update(
            task_id=task_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date,
        )

        if not success:
            raise TaskNotFoundError(task_id)

        # Update advanced fields directly on the task object
        if due_datetime is not None:
            task.due_datetime = due_datetime
        if recurrence is not None:
            task.recurrence = recurrence

        self._trigger_save()
        return self._task_list.get_by_id(task_id)


    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The unique task identifier

        Returns:
            True if task was deleted, False if not found
        """
        result = self._task_list.delete(task_id)
        if result:
            self._trigger_save()
        return result

    def mark_complete(self, task_id: int) -> bool:
        """Mark a task as complete and handle recurrence.

        Args:
            task_id: The unique task identifier

        Returns:
            True if task was marked, False if not found
        """
        task = self._task_list.get_by_id(task_id)
        if task is None:
            return False

        if not task.is_complete:
            task.is_complete = True

            # Handle recurrence
            if task.recurrence != "NONE" and task.due_datetime:
                from src.services.recurrence_service import RecurrenceService

                next_due = RecurrenceService.get_next_date(
                    task.due_datetime, task.recurrence
                )
                if next_due:
                    self.add_task(
                        title=task.title,
                        description=task.description,
                        priority=task.priority,
                        tags=task.tags,
                        due_datetime=next_due,
                        recurrence=task.recurrence,
                    )
                    # Link instances
                    new_task = self._task_list.tasks[-1]
                    new_task.parent_id = task.id

            self._trigger_save()
            return True
        return True


    def mark_incomplete(self, task_id: int) -> bool:
        """Mark a task as incomplete.

        Args:
            task_id: The unique task identifier

        Returns:
            True if task was marked, False if not found
        """
        result = self._task_list.mark_incomplete(task_id)
        if result:
            self._trigger_save()
        return result

    # =========================================================================
    # Search Operations
    # =========================================================================

    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks by keyword (case-insensitive, title OR description).

        Args:
            keyword: The search term

        Returns:
            List of matching tasks (filtered view)

        Raises:
            ValidationError: If keyword is empty
        """
        if not keyword or keyword.strip() == "":
            raise ValidationError("Please provide a search keyword.")

        self._search_term = keyword.strip().lower()
        return self.get_tasks()

    def clear_search(self) -> None:
        """Clear the current search term."""
        self._search_term = None

    def get_search_term(self) -> Optional[str]:
        """Get the current search term.

        Returns:
            The search term or None if no search is active
        """
        return self._search_term

    # =========================================================================
    # Filter Operations
    # =========================================================================

    def filter_tasks(
        self,
        filter_type: str,
        value: str,
    ) -> List[Task]:
        """Apply or update a filter.

        Args:
            filter_type: Type of filter ('status', 'priority', 'tag')
            value: Filter value

        Returns:
            List of filtered tasks

        Raises:
            ValidationError: If filter type or value is invalid
        """
        if filter_type not in ("status", "priority", "tag"):
            raise ValidationError(
                f"Invalid filter type '{filter_type}'. "
                "Must be: status, priority, or tag."
            )

        value = value.strip().lower() if value else ""

        if filter_type == "status":
            if value not in ("all", "pending", "complete"):
                raise ValidationError(
                    "Invalid status filter. Must be: all, pending, or complete."
                )
            self._current_filter.status = value

        elif filter_type == "priority":
            if value not in ("all", "high", "medium", "low"):
                raise ValidationError(
                    "Invalid priority filter. Must be: all, HIGH, MEDIUM, or LOW."
                )
            self._current_filter.priority = value.upper()

        elif filter_type == "tag":
            if not value:
                raise ValidationError("Please provide a tag name.")
            self._current_filter.tag = value

        return self.get_tasks()

    def clear_filters(self) -> List[Task]:
        """Clear all filters and search.

        Returns:
            List of all tasks
        """
        self._search_term = None
        self._current_filter.reset()
        return self.get_tasks()

    def get_current_filter(self) -> TaskFilter:
        """Get the current filter state.

        Returns:
            Current TaskFilter instance
        """
        return self._current_filter

    # =========================================================================
    # Sort Operations
    # =========================================================================

    def sort_tasks(self, mode: str) -> List[Task]:
        """Change the sort mode.

        Args:
            mode: Sort mode ('priority', 'alpha', 'date_added', 'manual')

        Returns:
            Sorted list of tasks

        Raises:
            ValidationError: If mode is invalid
        """
        try:
            self._current_sort = SortMode(mode)
        except ValueError as e:
            raise ValidationError(str(e))

        return self.get_tasks()

    def get_current_sort(self) -> SortMode:
        """Get the current sort mode.

        Returns:
            Current SortMode instance
        """
        return self._current_sort

    # =========================================================================
    # Manual Reorder Operations
    # =========================================================================

    def move_task(self, task_id: int, direction: str) -> Task:
        """Move a task up or down in manual sort order.

        Args:
            task_id: The task identifier
            direction: 'up' to move earlier, 'down' to move later

        Returns:
            The moved Task

        Raises:
            TaskNotFoundError: If task is not found
            ValidationError: If direction is invalid
        """
        if direction not in ("up", "down"):
            raise ValidationError("Direction must be 'up' or 'down'.")

        task = self._task_list.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        result = self._task_list.move_task(task_id, direction)
        if not result:
            raise ValidationError(f"Cannot move task #{task_id} {direction}.")

        self._trigger_save()
        return self._task_list.get_by_id(task_id)

    # =========================================================================
    # Get Tasks (Applies Search, Filter, Sort)
    # =========================================================================

    def get_tasks(self) -> List[Task]:
        """Get tasks with active search, filter, and sort settings applied.

        Returns:
            List of tasks matching all criteria, sorted appropriately
        """
        # Start with all tasks
        tasks = self._task_list.get_all()

        # Apply search
        if self._search_term:
            keyword = self._search_term.lower()
            tasks = [
                t
                for t in tasks
                if keyword in t.title.lower() or keyword in t.description.lower()
            ]

        # Apply filters
        tasks = [t for t in tasks if self._current_filter.matches(t)]

        # Apply sort
        tasks.sort(key=self._current_sort.get_sort_key)

        return tasks

    # =========================================================================
    # View State
    # =========================================================================

    def get_view_state(self) -> dict:
        """Get the current view state including filters, sort, and search.

        Returns:
            Dictionary with search_term, filter, sort_mode, and total_count
        """
        return {
            "search_term": self._search_term,
            "filter": {
                "status": self._current_filter.status,
                "priority": self._current_filter.priority,
                "tag": self._current_filter.tag,
            },
            "sort_mode": self._current_sort.mode,
            "total_count": len(self._task_list.get_all()),
        }

    def check_reminders(self, notification_service) -> None:
        """Scan tasks for upcoming deadlines and trigger notifications."""
        from datetime import datetime, timedelta

        now = datetime.now()
        threshold = now + timedelta(minutes=15)

        for task in self._task_list.tasks:
            if not task.is_complete and task.due_datetime and not task.reminder_sent:
                try:
                    due_dt = datetime.strptime(task.due_datetime, "%Y-%m-%d %H:%M")
                    if now <= due_dt <= threshold:
                        success = notification_service.notify(
                            title="Task Due Soon",
                            message=f"'{task.title}' is due at {task.due_datetime.split(' ')[1]}"
                        )
                        task.reminder_sent = True
                        self._trigger_save()
                except ValueError:
                    continue

    def get_overdue_tasks(self) -> List[Task]:
        """Identify tasks whose deadline has passed."""
        from datetime import datetime
        now = datetime.now()
        overdue = []

        for task in self._task_list.tasks:
            if not task.is_complete and task.due_datetime:
                try:
                    due_dt = datetime.strptime(task.due_datetime, "%Y-%m-%d %H:%M")
                    if due_dt < now:
                        overdue.append(task)
                except ValueError:
                    continue
        return overdue

    # =========================================================================
    # Persistence Operations
    # =========================================================================

    def save_tasks(self) -> bool:
        """Save all tasks to JSON file.

        Returns:
            True if save was successful

        Raises:
            PersistenceError: If save fails
        """
        all_tasks = self._task_list.get_all()

        data = {
            "version": "2.0",
            "next_id": self._task_list._next_id,
            "tasks": [task.to_dict() for task in all_tasks],
            "filter_state": {
                "status": self._current_filter.status,
                "priority": self._current_filter.priority,
                "tag": self._current_filter.tag,
            },
            "sort_mode": self._current_sort.mode,
        }

        try:
            with open(self._storage_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except (IOError, OSError) as e:
            raise PersistenceError(f"Failed to save tasks: {e}")

    def load_tasks(self) -> List[Task]:
        """Load tasks from JSON file.

        Returns:
            List of loaded tasks (also populates internal state)

        Note:
            If file doesn't exist (first run), returns empty list.
            If file is corrupted, logs error and returns empty list.
        """
        if not os.path.exists(self._storage_file):
            return []

        try:
            with open(self._storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError, OSError) as e:
            # Log but don't fail - start with empty list
            print(f"Warning: Could not load tasks from {self._storage_file}: {e}")
            return []

        # Validate version
        version = data.get("version", "1.0")
        if not version.startswith("2."):
            # Migration needed or old format
            print(f"Warning: Unknown tasks file version '{version}'")

        # Load tasks
        tasks_data = data.get("tasks", [])
        for task_data in tasks_data:
            self._task_list.add_from_dict(task_data)

        # Load filter state if present
        filter_state = data.get("filter_state", {})
        if filter_state:
            self._current_filter.status = filter_state.get("status", "all")
            self._current_filter.priority = filter_state.get("priority", "all")
            self._current_filter.tag = filter_state.get("tag")

        # Load sort mode if present
        sort_mode = data.get("sort_mode")
        if sort_mode:
            try:
                self._current_sort = SortMode(sort_mode)
            except ValueError:
                pass  # Use default

        return self._task_list.get_all()
