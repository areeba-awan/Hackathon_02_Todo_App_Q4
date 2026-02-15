# Feature Specification: Advanced Level Todo App

**Feature Branch**: `003-advanced-todo`
**Created**: 2026-01-07
**Status**: Draft
**Input**: User description: "Advanced features including Recurring Tasks (daily/weekly/monthly) and Due Dates with Time Reminders."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Deadlines and Reminders (Priority: P1)

As a busy professional, I want to set specific due dates and times for my tasks and receive notifications, so that I never miss a deadline.

**Why this priority**: Deadlines are the core of advanced task management. Without time-based tracking, productivity is limited to simple lists.

**Independent Test**: Can be tested by creating a task with a due date 1 minute in the future and verifying the console/system alert triggers.

**Acceptance Scenarios**:

1. **Given** a new or existing task, **When** I assign a due date (e.g., 2026-01-07) and time (e.g., 14:00), **Then** the task should display its deadline in the terminal list.
2. **Given** a task with a deadline reaching its threshold, **When** the system time matches the deadline, **Then** a system notification (or terminal alert if system notifications are unavailable) must be triggered.

---

### User Story 2 - Recurring Tasks (Priority: P2)

As a user with routine responsibilities, I want tasks to automatically reappear after I complete them (daily, weekly, or monthly), so I don't have to manually re-enter them.

**Why this priority**: Automation of routine tasks significantly reduces manual overhead and ensures consistency in habits/work.

**Independent Test**: Can be tested by marking a "Daily" recurring task as complete and verifying a new instance of the task is automatically created for the next day.

**Acceptance Scenarios**:

1. **Given** a task marked as recurring (Daily), **When** I complete the task, **Then** a new identical task should be generated with the due date shifted by 1 day.
2. **Given** a task with a "Weekly" recurrence, **When** it is completed, **Then** the new task should be scheduled for the same day next week.

---

### User Story 3 - Notification Fallback (Priority: P3)

As a console user, if my operating system blocks notifications, I want a clear terminal-based reminder when I next interact with the app, so I still stay informed.

**Why this priority**: Reliability is key; users must be able to trust the system even when environmental factors (OS permissions) interfere.

**Independent Test**: Disable system notifications and verify that starting the app or checking the list shows a "LATE/REMINDER" banner for overdue tasks.

**Acceptance Scenarios**:

1. **Given** notifications are disabled/unavailable, **When** a task's reminder time is reached, **Then** the app must record the missed reminder and show it prominently upon the next terminal interaction.

---

### Edge Cases

- **Missed Reminders**: How does the system handle a reminder that should have triggered while the app was closed? (Assumption: Show as "Overdue" or "Missed" next time the app opens).
- **Skipped Recurrence**: What happens if a user completes a task that was due 2 days ago but is set to "Daily"? Does it schedule for "Today" or "Yesterday + 1 day"? (Assumption: Reschedule relative to the original due date to maintain cadence).
- **Invalid Date Input**: How does the system handle "February 30th" or malformed strings? (Assumption: Reject with a clear error message and re-prompt for input).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to assign a Specific Date (YYYY-MM-DD) and Time (HH:MM) to any task.
- **FR-002**: System MUST allow tasks to be marked with a Recurrence Type: None, Daily, Weekly, Monthly.
- **FR-003**: System MUST automatically generate the "Next Instance" of a recurring task immediately upon completion of the current instance.
- **FR-004**: System MUST attempt to trigger a Desktop/System notification 0-15 minutes before a task deadline.
- **FR-005**: System MUST differentiate between recurring and one-time tasks in the console view (e.g., using a [R] symbol).
- **FR-006**: System MUST persist the "Last Reminder Sent" timestamp to avoid duplicate notifications.
- **FR-007**: System MUST support tasks without deadlines (backward compatibility with Phase I/II).

### Key Entities *(include if feature involves data)*

- **Task**:
  - `due_datetime`: Optional timestamp for deadline.
  - `recurrence`: Enum (DAILY, WEEKLY, MONTHLY, NONE).
  - `base_task_id`: Link to parent if it's a generated recurring instance (for tracking history).
  - `reminder_sent`: Boolean to track notification state.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can set a recurring task and its deadline in under 15 seconds via the console menu.
- **SC-002**: 100% of tasks marked as recurring successfully generate a new instance upon completion.
- **SC-003**: System notifications trigger within 30 seconds of the scheduled reminder time when the app is active.
- **SC-004**: Users can view all "Overdue" tasks as a filtered list in a single command.
