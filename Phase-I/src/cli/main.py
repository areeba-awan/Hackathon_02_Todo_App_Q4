"""Menu system and application entry point for the todo application with enhanced UX."""

import sys
import os
from src.services.todo_service import TodoService, PersistenceError
from src.services.notification import NotificationService
from src.cli.handlers import (
    handle_add_task,
    handle_view_tasks,
    handle_update_task,
    handle_delete_task,
    handle_mark_complete,
    handle_mark_incomplete,
    handle_search_tasks,
    handle_filter_tasks,
    handle_sort_tasks,
    handle_reorder_tasks,
    handle_clear_filters,
    handle_save_tasks,

    handle_help,
    Colors,
    print_header,
    print_error,
    print_info,
)


def clear_screen() -> None:
    """Clear the terminal screen for a fresh display."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_menu(service: TodoService) -> None:
    """Print the main menu options and notifications."""
    # Check for overdue tasks
    overdue = service.get_overdue_tasks()
    if overdue:
        print(f"\n{Colors.BRIGHT_RED}{'!' * 45}{Colors.RESET}")
        print(f"  {Colors.BOLD}{Colors.BRIGHT_RED}⚠️ OVERDUE TASKS FOUND ({len(overdue)}){Colors.RESET}")
        for task in overdue[:3]:
            print(f"  {Colors.RED}• {task.title} (due {task.due_datetime}){Colors.RESET}")
        if len(overdue) > 3:
            print(f"  {Colors.RED}• ... and {len(overdue)-3} more{Colors.RESET}")
        print(f"{Colors.BRIGHT_RED}{'!' * 45}{Colors.RESET}")

    print()
    print(f"{Colors.BRIGHT_YELLOW}{'=' * 45}{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.BRIGHT_GREEN}TODO LIST MANAGER{Colors.RESET}")
    print(f"{Colors.BRIGHT_YELLOW}{'=' * 45}{Colors.RESET}")
    print()
    print(f"{Colors.GREEN}[a] or 1{Colors.RESET}  Add a new task")
    print(f"{Colors.BLUE}[v] or 2{Colors.RESET}  View all tasks")
    print(f"{Colors.YELLOW}[u] or 3{Colors.RESET}  Update a task")
    print(f"{Colors.RED}[d] or 4{Colors.RESET}  Delete a task")
    print(f"{Colors.GREEN}[c] or 5{Colors.RESET}  Mark as complete")
    print(f"{Colors.CYAN}[i] or 6{Colors.RESET}  Mark as incomplete")
    print(f"{Colors.MAGENTA}[s] or 7{Colors.RESET}  Search tasks")
    print(f"{Colors.BRIGHT_CYAN}[f] or 8{Colors.RESET}  Filter tasks")
    print(f"{Colors.BRIGHT_BLUE}[o] or 9{Colors.RESET}  Sort tasks")
    print(f"{Colors.BRIGHT_YELLOW}[r] or 10{Colors.RESET}  Manual reorder")
    print(f"{Colors.BRIGHT_RED}[x] or 11{Colors.RESET}  Clear filters")
    print(f"{Colors.BRIGHT_GREEN}[w] or 12{Colors.RESET}  Save tasks")
    print(f"{Colors.BRIGHT_MAGENTA}[h] or 13{Colors.RESET}  Help")
    print(f"{Colors.BRIGHT_WHITE}[q] or 14{Colors.RESET}  Exit")
    print()
    print(f"{Colors.CYAN}Choose an option:{Colors.RESET}")


def get_user_choice() -> str:
    """Get user menu selection (single key or number)."""
    # Map numbers to letters
    number_map = {
        "1": "a", "2": "v", "3": "u", "4": "d", "5": "c", "6": "i",
        "7": "s", "8": "f", "9": "o", "10": "r", "11": "x",
        "12": "w", "13": "h", "14": "q"
    }

    while True:
        choice = input(f"{Colors.CYAN}> {Colors.RESET}").strip().lower()

        # Convert number to letter if needed
        if choice in number_map:
            choice = number_map[choice]

        valid_choices = {"a", "v", "u", "d", "c", "i", "s", "f", "o", "r", "x", "w", "h", "q"}
        if choice in valid_choices:
            return choice

        print_error("Invalid", "Press a key or number 1-14")


def handle_choice(service: TodoService, choice: str) -> bool:
    """Route user choice to appropriate handler."""
    handlers = {
        "a": handle_add_task,
        "v": handle_view_tasks,
        "u": handle_update_task,
        "d": handle_delete_task,
        "c": handle_mark_complete,
        "i": handle_mark_incomplete,
        "s": handle_search_tasks,
        "f": handle_filter_tasks,
        "o": handle_sort_tasks,
        "r": handle_reorder_tasks,
        "x": handle_clear_filters,
        "w": handle_save_tasks,
        "h": handle_help,
    }

    if choice == "q":
        return True

    handler = handlers.get(choice)
    if handler:
        try:
            handler(service)
            import time
            time.sleep(0.3)
        except KeyboardInterrupt:
            print()
            print_info("Press Enter to continue")
            try:
                input()
            except:
                pass
        except EOFError:
            print()
            print_info("Cancelled")
        except Exception as e:
            print_error(str(e))

    return False


def cleanup_storage() -> None:
    """Delete task.json file on exit for ephemeral behavior."""
    storage_file = "tasks.json"
    if os.path.exists(storage_file):
        try:
            os.remove(storage_file)
        except Exception:
            pass  # Silent fail on cleanup


def main_loop() -> None:
    """Run the main menu loop until user exits."""
    service = TodoService()
    notification_service = NotificationService()

    # Start with empty task list (no load for ephemeral behavior)
    print_info("Starting with empty task list")

    # Register auto-save callback
    def auto_save():
        try:
            service.save_tasks()
        except PersistenceError:
            pass  # Silent fail for auto-save

    service.add_change_callback(auto_save)

    # Welcome banner
    clear_screen()
    print()
    print(f"{Colors.BOLD}{Colors.BRIGHT_GREEN}Welcome to Todo List Manager!{Colors.RESET}")
    print(f"{Colors.DIM}Manage your tasks efficiently{Colors.RESET}")
    print()

    try:
        while True:
            try:
                # Poll for reminders every time the menu is displayed
                service.check_reminders(notification_service)

                display_menu(service)
                choice = get_user_choice()
                should_exit = handle_choice(service, choice)
                if should_exit:
                    # Cleanup storage on exit (ephemeral behavior)
                    cleanup_storage()

                    print()
                    print(f"{Colors.BOLD}{Colors.BRIGHT_GREEN}Thanks for using Todo List Manager!{Colors.RESET}")
                    print()
                    break
            except KeyboardInterrupt:
                print()
                print_info("Use 'q' or '14' to exit, or press Ctrl+C again to force quit.")
                continue
            except EOFError:
                # Cleanup storage on exit
                cleanup_storage()
                print()
                print(f"{Colors.BRIGHT_BLACK}Goodbye!{Colors.RESET}")
                print()
                break
    except KeyboardInterrupt:
        # Force quit on second Ctrl+C
        cleanup_storage()
        print()
        print(f"{Colors.BRIGHT_BLACK}Goodbye!{Colors.RESET}")
        print()


if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        cleanup_storage()
        print()
        print(f"{Colors.BRIGHT_BLACK}Goodbye!{Colors.RESET}")
        print()
        sys.exit(0)
