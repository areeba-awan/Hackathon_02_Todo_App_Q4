# Tasks: Advanced Level Todo App

**Input**: Design documents from `/specs/003-advanced-todo/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create `specs/003-advanced-todo/quickstart.md` per implementation plan
- [ ] T002 [P] Install `python-dateutil` and `plyer` dependencies
- [ ] T003 [P] Verify development environment supports desktop notifications

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [ ] T004 Extended Task Entity: Update `src/models/task.py` with `due_datetime`, `recurrence`, `parent_id`, and `reminder_sent` fields.
- [ ] T005 [P] Notification Abstraction: Create `src/services/notification.py` with a consistent interface for `plyer` and terminal fallback.
- [ ] T006 [P] Recurrence Service: Implement `src/services/recurrence_service.py` using `dateutil.relativedelta` for Daily, Weekly, Monthly calculations.
- [ ] T007 Base Service Update: Update `src/services/todo_service.py` to handle new attributes during task creation and retrieval.

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Deadlines and Reminders (Priority: P1) 🎯 MVP

**Goal**: Enable setting deadlines and receiving notifications for tasks.

**Independent Test**: Use the CLI to create a task with a deadline 2 minutes from now. Verify it displays in the list and triggers a notification.

### Implementation for User Story 1

- [ ] T008 [P] [US1] CLI Input: Update `src/cli/handlers.py` to prompt for due date and time.
- [ ] T009 [US1] Reminder Logic: Implement a non-blocking check in `src/services/todo_service.py` that identifies tasks due within the notification window.
- [ ] T010 [US1] Notification Trigger: Integrate `src/services/notification.py` into the main application loop in `src/cli/main.py`.
- [ ] T011 [US1] Display Deadlines: Update task listing in `src/cli/menu.py` to show due dates and overdue status.

**Checkpoint**: User Story 1 functional - tasks can now have deadlines and trigger reminders.

---

## Phase 4: User Story 2 - Recurring Tasks (Priority: P2)

**Goal**: Automate routine task rescheduling.

**Independent Test**: Mark a "Daily" task as complete. Verify a new task is created for T+1 day and the current one is archived.

### Implementation for User Story 2

- [ ] T012 [P] [US2] CLI Input: Update `src/cli/handlers.py` to support selecting recurrence frequency (Daily, Weekly, Monthly).
- [ ] T013 [US2] Rescheduling Logic: Update `src/services/todo_service.py`'s completion handler to call the `recurrence_service` and spawn a new task instance.
- [ ] T014 [US2] Recurrence Marking: Update the task list display in `src/cli/menu.py` to include a `[R]` symbol for recurring tasks.

**Checkpoint**: User Story 2 functional - routine tasks now auto-reschedule.

---

## Phase 5: User Story 3 - Notification Fallback (Priority: P3)

**Goal**: Ensure reminders are seen even if system notifications fail.

**Independent Test**: Disable system notifications and verify that starting the app shows a banner for missed deadlines.

### Implementation for User Story 3

- [ ] T015 [US3] Missed Deadline Detection: Implement logic in `src/services/todo_service.py` to detect tasks whose deadline passed while the app was closed.
- [ ] T016 [US3] Terminal Banner: Create a "Reminders/Alerts" section at the top of the main menu in `src/cli/menu.py` to show missed notifications.

**Checkpoint**: All user stories functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T017 [P] Update `specs/003-advanced-todo/quickstart.md` with usage instructions.
- [ ] T018 Ensure backward compatibility: Check that loading a Phase I task list (no advanced fields) doesn't crash the app.
- [ ] T019 Final testing pass: verify multiple recurring tasks don't conflict.

---

## Dependencies & Execution Order

1. **Setup & Foundational (T001-T007)**: Must be completed first to provide the data structure and base services.
2. **User Story 1 (T008-T011)**: Crucial for the "Advanced" value proposition.
3. **User Story 2 (T012-T014)**: Builds on the date handling from US1.
4. **User Story 3 (T015-T016)**: Final reliability layer.
5. **Polish (T017-T019)**: Documentation and final cleanup.
