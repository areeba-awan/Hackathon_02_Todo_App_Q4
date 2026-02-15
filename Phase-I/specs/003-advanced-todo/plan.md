# Implementation Plan: Advanced Todo App (Phase 1)

**Branch**: `003-advanced-todo` | **Date**: 2026-01-07 | **Spec**: [spec.md](./spec.md)

## Summary
Introduce time-based intelligence to the Todo App. This includes scheduling tasks with due dates/times and implementing a recurrence system (Daily, Weekly, Monthly) that automatically respawns tasks upon completion. Notifications will be handled via a cross-platform desktop library with a graceful console fallback.

## Technical Context

**Language/Version**: Python 3.13
**Primary Dependencies**: `python-dateutil` (for recurrence), `plyer` or `notifypy` (for notifications)
**Storage**: In-memory (existing) - data structures extended for new fields
**Testing**: `pytest` (unit and integration)
**Target Platform**: Cross-platform (WSL2/Linux focus)
**Project Type**: Single Console Application
**Performance Goals**: Reminders check in <100ms within the event loop
**Constraints**: Console-based, no persistent DB (runtime-only)
**Scale/Scope**: Advanced Level functionality (Phase 1)

## Constitution Check

| Gate | Status |
|------|--------|
| TDD Mandatory | PASS (Plan includes test-first steps) |
| CLI Interface | PASS (All new features mapped to console menu) |
| Simplicity | PASS (Polling in main loop vs complex background daemons) |

## Project Structure

### Documentation (this feature)

```text
specs/003-advanced-todo/
├── plan.md              # This file
├── research.md          # Technology decisions
├── data-model.md        # Extended Task model
├── quickstart.md        # How to run advanced features
├── contracts/           # Interaction definitions
└── tasks.md             # Implementation steps (to be generated)
```

### Source Code

```text
src/
├── models/
│   └── task.py          # Update with due_datetime, recurrence
├── services/
│   ├── todo_service.py  # Add recurrence logic, reminder polling
│   └── notification.py  # NEW: abstraction for system notifications
├── cli/
│   ├── handlers.py      # Update to handle date/time input
│   └── menu.py          # New menu options for Advanced features
```

## Step-by-Step Plan

### Phase 1: Core Time Logic
1.  **Date/Time Support**: Update the `Task` model and `TodoService` to accept and store `due_datetime`.
2.  **Recurrence Engine**: Implement `RecurrenceService` that calculates the next date based on the chosen frequency (Daily, Weekly, Monthly).
3.  **Rescheduling Logic**: Modify `TodoService.complete_task` to check for recurrence and trigger the creation of a new task instance if applicable.

### Phase 2: Reminders & Notifications
1.  **Notification Library**: Integrate `plyer` and create a `NotificationService` wrapper.
2.  **Polling Loop**: Implement a non-blocking check in the main CLI menu loop that scans for "soon-to-be-due" tasks.
3.  **Console Fallback**: Add logic to display a prominent "OVERDUE" warning in the task list if a notification was missed or is unavailable.

## Feature Dependency Order
1.  **Due Dates** (Foundation)
2.  **Recurrence** (Depends on Date logic)
3.  **Notifications** (Enhanced feature built on Dates)

## Validation & Completion Criteria
- [ ] Units tests for `relativedelta` recurrence calculations pass.
- [ ] Integration tests verify that completing a recurring task creates a new one for the next period.
- [ ] Manual test: Create a task due in 1 min, receive a desktop notification.
- [ ] Manual test: Open app with an overdue task, see the console warning.
- [ ] Backward compatibility: Existing Phase I/II tests must continue to pass.
