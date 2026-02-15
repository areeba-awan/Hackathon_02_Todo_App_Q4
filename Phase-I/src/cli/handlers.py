"""CLI handlers for todo application operations with enhanced UX and intermediate features."""

from typing import Optional
from src.services.todo_service import (
    TodoService,
    TaskNotFoundError,
    ValidationError,
    PersistenceError,
)
from src.models.task import VALID_PRIORITIES, MAX_TAGS


# ANSI color codes
class Colors:
    """Terminal color codes for enhanced output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright foreground colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


def print_success(message: str) -> None:
    """Print a success message in green."""
    print(f"\n{Colors.GREEN}[OK] {message}{Colors.RESET}")


def print_error(message: str, hint: str = "") -> None:
    """Print an error message in red with optional hint."""
    print(f"\n{Colors.RED}✗ {message}{Colors.RESET}")
    if hint:
        print(f"\n{Colors.DIM}  → {hint}{Colors.RESET}")


def print_info(message: str) -> None:
    """Print an info message in cyan."""
    print(f"\n{Colors.CYAN}→ {message}{Colors.RESET}")


def print_header(message: str) -> None:
    """Print a header message."""
    print()
    print(f"{Colors.BRIGHT_YELLOW}{'=' * 45}{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.BRIGHT_CYAN}{message}{Colors.RESET}")
    print(f"{Colors.BRIGHT_YELLOW}{'=' * 45}{Colors.RESET}")
    print()


def get_valid_description(prompt: str = "Description: ") -> str:
    """Get a non-empty description from user input with enhanced prompts."""
    while True:
        desc = input(f"\n{Colors.CYAN}{prompt}{Colors.RESET}").strip()
        if not desc:
            print_error("\nTask description cannot be empty", "Type something and press Enter")
        else:
            return desc


def get_valid_task_id(prompt: str = "Task ID: ") -> int:
    """Get a valid task ID from user input with enhanced prompts."""
    while True:
        try:
            task_id = int(input(f"{Colors.CYAN}{prompt}{Colors.RESET}"))
            if task_id <= 0:
                print_error("\nTask ID must be a positive number", "Enter a number like 1, 2, 3...")
                continue
            return task_id
        except ValueError:
            print_error("\nPlease enter a valid number", "Numbers only, like 1 or 2")


def get_valid_priority() -> str:
    """Get a valid priority from user input."""
    print_info(f"\nPriority options: {', '.join(sorted(VALID_PRIORITIES))}")
    while True:
        priority = input(f"\n{Colors.CYAN}Priority [{Colors.BRIGHT_GREEN}MEDIUM{Colors.CYAN}]: {Colors.RESET}").strip().upper()
        if not priority:
            return "MEDIUM"
        if priority in VALID_PRIORITIES:
            return priority
        print_error(f"\nInvalid priority '{priority}'", f"Must be: {', '.join(sorted(VALID_PRIORITIES))}")


def get_valid_tags() -> list:
    """Get valid tags from user input."""
    print_info(f"\nTags (max {MAX_TAGS}, lowercase with hyphens, e.g., 'work-projects')")
    print_info("\nEnter tags one at a time, or press Enter twice to finish")
    tags = []
    while len(tags) < MAX_TAGS:
        tag = input(f"{Colors.CYAN}Tag [{len(tags) + 1}]: {Colors.RESET}").strip().lower()
        if not tag:
            if not tags:
                # Ask if they want to add tags
                confirm = input(f"{Colors.CYAN}Add no tags? [Y/n]: {Colors.RESET}").strip().lower()
                if confirm and confirm != 'y':
                    continue
            break
        # Validate tag format
        if not tag.replace("-", "").isalpha() or "  " in tag:
            print_error("\nInvalid tag format", "Use lowercase letters with hyphens, no spaces")
            continue
        if tag in tags:
            print_info(f"\nTag '{tag}' already added")
            continue
        tags.append(tag)
        print_success(f"\nAdded tag: {tag}")
    return tags


def get_valid_datetime(prompt: str = "\n Due Date & Time (YYYY-MM-DD HH:MM) or Enter for none: ") -> Optional[str]:
    """Get a valid datetime from user input."""
    while True:
        dt_str = input(f"{Colors.CYAN}{prompt}{Colors.RESET}").strip()
        if not dt_str:
            return None
        try:
            from datetime import datetime
            datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            return dt_str
        except ValueError:
            print_error("\nInvalid format", "Use YYYY-MM-DD HH:MM (e.g., 2026-01-07 14:00)")


def get_valid_recurrence() -> str:
    """Get a valid recurrence type from user input."""
    options = ["NONE", "DAILY", "WEEKLY", "MONTHLY"]
    print_info(f"\nRecurrence options: {', '.join(options)}")
    while True:
        recur = input(f"\n{Colors.CYAN}Recurrence [{Colors.BRIGHT_GREEN}NONE{Colors.CYAN}]: {Colors.RESET}").strip().upper()
        if not recur:
            return "NONE"
        if recur in options:
            return recur
        print_error(f"Invalid recurrence '{recur}'", f"Must be: {', '.join(options)}")


def handle_add_task(service: TodoService) -> None:
    """Handle the Add Task menu option with advanced features."""
    print_header("Add New Task")
    try:
        title = get_valid_description("What needs to be done?")
        description = input(f"\n{Colors.CYAN}Description (optional): {Colors.RESET}").strip()

        priority = get_valid_priority()
        tags = get_valid_tags()

        # Advanced features
        due_datetime = get_valid_datetime()
        recurrence = "NONE"
        if due_datetime:
            recurrence = get_valid_recurrence()

        task = service.add_task(
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_datetime=due_datetime,
            recurrence=recurrence,
        )
        print_success(f"Task added: \"{task.title}\"")
        print_info(f"Task #{task.id} created")
        if task.due_datetime:
            print_info(f"Due: {task.due_datetime}")
        if task.recurrence != "NONE":
            print_info(f"Recurrence: {task.recurrence}")
    except ValidationError as e:
        print_error(str(e))
    except (EOFError, KeyboardInterrupt):
        print_info("Operation cancelled")



def handle_view_tasks(service: TodoService) -> None:
    """Handle the View Tasks menu option with clean colorful formatting."""
    tasks = service.get_tasks()
    view_state = service.get_view_state()

    # Clean header
    print()
    print(f"{Colors.BRIGHT_YELLOW}{'=' * 45}{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.BRIGHT_GREEN}YOUR TASKS{Colors.RESET}")
    print(f"{Colors.BRIGHT_YELLOW}{'=' * 45}{Colors.RESET}")

    # Active filters
    filters = []
    if view_state["search_term"]:
        filters.append(f'🔍 "{view_state["search_term"]}"')
    if view_state["filter"]["status"] != "all":
        filters.append(f'📋 {view_state["filter"]["status"]}')
    if view_state["filter"]["priority"] != "all":
        filters.append(f'⚡ {view_state["filter"]["priority"]}')
    if view_state["filter"]["tag"]:
        filters.append(f'🏷️ {view_state["filter"]["tag"]}')
    if view_state["sort_mode"] != "date_added":
        sort_icons = {"priority": "📊", "alpha": "🔤", "manual": "✏️"}
        filters.append(f'{sort_icons.get(view_state["sort_mode"], "🔄")} {view_state["sort_mode"]}')

    if filters:
        print(f"{Colors.DIM}Filters: {', '.join(filters)}{Colors.RESET}")
        print()

    all_tasks = service.get_all_tasks()
    if not all_tasks:
        print()
        print(f"\n{Colors.DIM}No tasks yet! Add a task to get started.{Colors.RESET}")
        return

    if not tasks:
        print()
        print(f"{Colors.BRIGHT_RED}No tasks match your filters{Colors.RESET}")
        print(f"{Colors.DIM}Total: {view_state['total_count']} tasks{Colors.RESET}")
        return

    # Progress bar
    completed = sum(1 for t in all_tasks if t.is_complete)
    total = len(all_tasks)
    percent = int(completed / total * 10) if total > 0 else 0
    prog_bar = f"[{Colors.GREEN}{'█' * percent}{Colors.DIM}{'░' * (10 - percent)}{Colors.RESET}]"
    print(f"{prog_bar} {Colors.BOLD}{completed}/{total}{Colors.RESET} done")
    print()

        # Task list
    for task in tasks:
        # Status with enhanced styling
        if task.is_complete:
            status = f"{Colors.BRIGHT_GREEN}{Colors.BOLD}[✔]{Colors.RESET}"
        else:
            status = f"{Colors.BRIGHT_RED}{Colors.BOLD}[✘]{Colors.RESET}"

        # Recurrence symbol
        recur_sym = f" {Colors.MAGENTA}🔄{Colors.RESET}" if task.recurrence != "NONE" else ""

        # Priority
        if task.priority == "HIGH":
            p_badge = f"{Colors.BRIGHT_RED}[HIGH]{Colors.RESET}"
        elif task.priority == "LOW":
            p_badge = f"{Colors.GREEN}[LOW]{Colors.RESET}"
        else:
            p_badge = f"{Colors.BRIGHT_YELLOW}[MED]{Colors.RESET}"

        # Main title line with ID, status, priority, and title
        print(f"{status}{recur_sym} {Colors.BOLD}#{task.id}{Colors.RESET} {p_badge} {task.title}")

        # Description
        if task.description:
            print(f"   {Colors.DIM}{Colors.CYAN}📝 {task.description}{Colors.RESET}")

        # Tags
        if task.tags:
            tags_list = ", ".join(task.tags[:3])
            if len(task.tags) > 3:
                tags_list += f"+{len(task.tags)-3}"
            print(f"   {Colors.BRIGHT_CYAN}🏷️ {tags_list}{Colors.RESET}")

        # Due date/time
        if task.due_datetime:
            from datetime import datetime
            try:
                due_dt = datetime.strptime(task.due_datetime, "%Y-%m-%d %H:%M")
                if due_dt < datetime.now() and not task.is_complete:
                    print(f"   {Colors.BRIGHT_RED}⏰ OVERDUE: {task.due_datetime}{Colors.RESET}")
                else:
                    print(f"   {Colors.BRIGHT_YELLOW}📅 {task.due_datetime}{Colors.RESET}")
            except ValueError:
                print(f"   {Colors.BRIGHT_YELLOW}📅 {task.due_datetime}{Colors.RESET}")
        elif task.due_date:
            print(f"   {Colors.BRIGHT_YELLOW}📅 {task.due_date}{Colors.RESET}")

        # Add gap between tasks
        print()


    pending = total - completed
    print()
    print(f"{Colors.GREEN}{completed}{Colors.RESET} done  ·  {Colors.YELLOW}{pending}{Colors.RESET} pending")


def handle_update_task(service: TodoService) -> None:
    """Handle the Update Task menu option with enhanced UX."""
    print_header("Update Task")
    try:
        task_id = get_valid_task_id("Which task to update? (ID)")

        task = service.get_task(task_id)
        if task is None:
            print_error(f"Task #{task_id} not found", "Use View Tasks to see all tasks")
            return

        # Show current values
        print(f"\nCurrent: \"{task.title}\"")
        print(f"  Description: {task.description or '(none)'}")
        print(f"  Priority: {task.priority}")
        print(f"  Tags: {', '.join(task.tags) if task.tags else '(none)'}")
        print()

        # Update options
        print("Leave a field blank to keep current value")
        print()

        # Title
        title = get_valid_description(f"New title [{task.title}]: ")
        if title.strip() == "":
            title = None

        # Description
        description = input(f"{Colors.CYAN}New description (or press Enter to keep current): {Colors.RESET}").strip()
        if description == "":
            description = None

        # Priority
        new_priority = get_valid_priority()
        if new_priority == task.priority:
            new_priority = None

        # Tags
        print_info("Current tags: " + (", ".join(task.tags) if task.tags else "(none)"))
        new_tags_input = input(f"{Colors.CYAN}New tags (comma-separated) or Enter to keep: {Colors.RESET}").strip()
        if new_tags_input:
            new_tags = [t.strip().lower() for t in new_tags_input.split(",") if t.strip()]
        else:
            new_tags = None

        # Advanced Features
        print(f"\nCurrent Due: {task.due_datetime or '(none)'}")
        due_datetime = get_valid_datetime("New Due Date & Time (YYYY-MM-DD HH:MM) or Enter to keep: ")

        print(f"Current Recurrence: {task.recurrence}")
        recurrence = get_valid_recurrence()
        if recurrence == task.recurrence:
            recurrence = None

        # Update
        updated = service.update_task(
            task_id=task_id,
            title=title,
            description=description,
            priority=new_priority,
            tags=new_tags,
            due_datetime=due_datetime,
            recurrence=recurrence,
        )

        print_success("Task updated successfully!")
        print(f"  \"{updated.title}\"")

    except (ValueError, TaskNotFoundError, ValidationError) as e:
        print_error(str(e))
    except (EOFError, KeyboardInterrupt):
        print_info("Operation cancelled")


def handle_delete_task(service: TodoService) -> None:
    """Handle the Delete Task menu option with confirmation."""
    print_header("Delete Task")
    try:
        task_id = get_valid_task_id("Which task to delete? (ID)")

        task = service.get_task(task_id)
        if task is None:
            print_error(f"Task #{task_id} not found", "Use View Tasks to see all tasks")
            return

        # Show task and confirm
        print()
        print(f"  Task: \"{task.title}\"")
        status = "Done" if task.is_complete else "Todo"
        print(f"  Status: {status}")
        print()

        confirm = input(f"{Colors.YELLOW}Delete this task? [y/N]: {Colors.RESET}").strip().lower()

        if confirm != 'y':
            print_info("Cancelled - task not deleted")
            return

        success = service.delete_task(task_id)
        if success:
            print_success("Task deleted")
        else:
            print_error("Failed to delete task")

    except (EOFError, KeyboardInterrupt):
        print_info("Operation cancelled")


def handle_mark_complete(service: TodoService) -> None:
    """Handle the Mark Complete menu option."""
    print_header("Mark Complete")
    try:
        task_id = get_valid_task_id("Which task is done? (ID)")

        task = service.get_task(task_id)
        if task is None:
            print_error(f"Task #{task_id} not found", "Use View Tasks to see all tasks")
            return

        if task.is_complete:
            print_info(f"Task #{task_id} is already marked as complete")
            return

        success = service.mark_complete(task_id)
        if success:
            print_success(f"Marked \"{task.title}\" as complete!")
        else:
            print_error("Failed to update task")

    except (EOFError, KeyboardInterrupt):
        print_info("Operation cancelled")


def handle_mark_incomplete(service: TodoService) -> None:
    """Handle the Mark Incomplete menu option."""
    print_header("Mark Incomplete")
    try:
        task_id = get_valid_task_id("Which task is not done? (ID)")

        task = service.get_task(task_id)
        if task is None:
            print_error(f"Task #{task_id} not found", "Use View Tasks to see all tasks")
            return

        if not task.is_complete:
            print_info(f"Task #{task_id} is already marked as incomplete")
            return

        success = service.mark_incomplete(task_id)
        if success:
            print_success(f"Marked \"{task.title}\" as todo again")
        else:
            print_error("Failed to update task")

    except (EOFError, KeyboardInterrupt):
        print_info("Operation cancelled")


def handle_search_tasks(service: TodoService) -> None:
    """Handle the Search Tasks menu option."""
    print_header("Search Tasks")
    try:
        keyword = input(f"{Colors.CYAN}Search keyword: {Colors.RESET}").strip()

        if not keyword:
            print_error("Please enter a search keyword")
            return

        tasks = service.search_tasks(keyword)
        print_info(f"Found {len(tasks)} tasks matching \"{keyword}\"")

        if tasks:
            for task in tasks:
                status = "[X]" if task.is_complete else "[ ]"
                print(f"  {Colors.BOLD}#{task.id}{Colors.RESET} {status} {task.title}")
        else:
            print_info("No tasks match your search")

    except ValidationError as e:
        print_error(str(e))
    except (EOFError, KeyboardInterrupt):
        print_info("Operation cancelled")


def handle_filter_tasks(service: TodoService) -> None:
    """Handle the Filter Tasks submenu."""
    while True:
        print_header("Filter Tasks")
        print("1. Filter by Status (all/pending/complete)")
        print("2. Filter by Priority (all/HIGH/MEDIUM/LOW)")
        print("3. Filter by Tag")
        print("4. View filtered tasks")
        print("5. Back to main menu")

        choice = input(f"\n{Colors.CYAN}Choose [1-5]: {Colors.RESET}").strip()

        if choice == "5":
            break
        elif choice == "1":
            status = input(f"{Colors.CYAN}Status [all/pending/complete]: {Colors.RESET}").strip().lower()
            if not status:
                status = "all"
            try:
                tasks = service.filter_tasks("status", status)
                print_success(f"Status filter set to '{status}'. {len(tasks)} tasks match.")
            except ValidationError as e:
                print_error(str(e))
        elif choice == "2":
            priority = input(f"{Colors.CYAN}Priority [all/HIGH/MEDIUM/LOW]: {Colors.RESET}").strip().upper()
            if not priority:
                priority = "ALL"
            try:
                tasks = service.filter_tasks("priority", priority)
                print_success(f"Priority filter set to '{priority}'. {len(tasks)} tasks match.")
            except ValidationError as e:
                print_error(str(e))
        elif choice == "3":
            tag = input(f"{Colors.CYAN}Tag name: {Colors.RESET}").strip().lower()
            if tag:
                try:
                    tasks = service.filter_tasks("tag", tag)
                    print_success(f"Tag filter set to '{tag}'. {len(tasks)} tasks match.")
                except ValidationError as e:
                    print_error(str(e))
            else:
                print_error("Please enter a tag name")
        elif choice == "4":
            handle_view_tasks(service)
        else:
            print_error("Invalid choice")


def handle_sort_tasks(service: TodoService) -> None:
    """Handle the Sort Tasks menu option."""
    print_header("Sort Tasks")
    print("Sort modes:")
    print("1. priority  - Sort by priority (HIGH → MEDIUM → LOW)")
    print("2. alpha     - Sort alphabetically (A → Z)")
    print("3. date_added - Sort by date added (newest first)")
    print("4. manual    - Sort manually (use up/down commands)")

    mode = input(f"\n{Colors.CYAN}Sort mode [1-4 or name]: {Colors.RESET}").strip().lower()

    mode_map = {
        "1": "priority", "priority": "priority",
        "2": "alpha", "alpha": "alpha",
        "3": "date_added", "date_added": "date_added",
        "4": "manual", "manual": "manual",
    }

    if mode in mode_map:
        mode = mode_map[mode]
        try:
            tasks = service.sort_tasks(mode)
            print_success(f"Sorted by '{mode}'. {len(tasks)} tasks shown.")
        except ValidationError as e:
            print_error(str(e))
    else:
        print_error("Invalid sort mode")


def handle_reorder_tasks(service: TodoService) -> None:
    """Handle the Manual Reorder menu option."""
    print_header("Manual Reorder")
    try:
        task_id = get_valid_task_id("Which task to move? (ID)")

        task = service.get_task(task_id)
        if task is None:
            print_error(f"Task #{task_id} not found", "Use View Tasks to see all tasks")
            return

        print(f"Task: \"{task.title}\"")
        print("1. Move up (appear earlier)")
        print("2. Move down (appear later)")

        direction = input(f"\n{Colors.CYAN}Direction [1-2]: {Colors.RESET}").strip()
        direction_map = {"1": "up", "2": "down"}

        if direction in direction_map:
            try:
                moved_task = service.move_task(task_id, direction_map[direction])
                print_success(f"Moved \"{moved_task.title}\" {direction_map[direction]}")
            except (ValidationError, TaskNotFoundError) as e:
                print_error(str(e))
        else:
            print_error("Invalid direction")

    except (EOFError, KeyboardInterrupt):
        print_info("Operation cancelled")


def handle_clear_filters(service: TodoService) -> None:
    """Handle the Clear Filters menu option."""
    print_header("Clear Filters")
    tasks = service.clear_filters()
    print_success("All filters and search cleared")
    print(f"Showing all {len(tasks)} tasks")


def handle_save_tasks(service: TodoService) -> None:
    """Handle the Save Tasks menu option."""
    print_header("Save Tasks")
    try:
        success = service.save_tasks()
        if success:
            print_success("Tasks saved to file")
        else:
            print_error("Failed to save tasks")
    except PersistenceError as e:
        print_error(str(e))


def handle_help(service: TodoService) -> None:
    """Print help message."""
    print_header("Help")
    print("Commands:")
    print("1. Add Task        - Create a new task")
    print("2. View Tasks      - Show all tasks")
    print("3. Update Task     - Edit a task")
    print("4. Delete Task     - Remove a task")
    print("5. Mark Complete   - Mark task as done")
    print("6. Mark Incomplete - Mark task as todo")
    print("7. Search Tasks    - Search by keyword")
    print("8. Filter Tasks    - Filter by status/priority/tag")
    print("9. Sort Tasks      - Change sort order")
    print("10. Manual Reorder - Move tasks up/down")
    print("11. Clear Filters  - Reset all filters")
    print("12. Save Tasks     - Save to file")
    print("13. Help           - Show this help")
    print("14. Exit           - Exit the application")
