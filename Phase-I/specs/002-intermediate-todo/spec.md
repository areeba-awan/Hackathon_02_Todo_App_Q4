# Feature Specification: Phase I Intermediate - Todo Console App Enhancement

**Feature Branch**: `002-intermediate-todo`
**Created**: 2026-01-06
**Status**: Draft
**Input**: User description: "Update specifications for Intermediate Level in "Evolution of Todo" project (Phase I console app). Extend existing basic features ONLY with intermediate usability features while staying in-memory Python console app."

## User Scenarios & Testing

### User Story 1 - Add Tasks with Priority and Tags (Priority: P1)

As a user, I want to add tasks with priority levels and tags so that I can organize and categorize my tasks by importance and context.

**Why this priority**: Priority and tags are the foundation of all intermediate features. Without them, filtering and sorting by these criteria is impossible.

**Independent Test**: Can be fully tested by adding a task with priority and tags, then viewing the task list to verify priority is displayed and tags are visible.

**Acceptance Scenarios**:

1. **Given** the user is adding a task, **When** they specify a priority (HIGH, MEDIUM, LOW), **Then** the task is stored with that priority and displayed appropriately.
2. **Given** the user is adding a task, **When** they specify up to 5 tags in lowercase hyphenated format, **Then** the task is stored with those tags.
3. **Given** the user adds a task without specifying priority, **When** the task is created, **Then** the default priority is MEDIUM.
4. **Given** the user adds a task without specifying tags, **When** the task is created, **Then** the tags list is empty.
5. **Given** the user attempts to add more than 5 tags, **When** they enter a 6th tag, **Then** the system displays an error and does not add the task.

---

### User Story 2 - Update Task Priority and Tags (Priority: P1)

As a user, I want to modify the priority and tags of existing tasks so that I can adjust task organization as priorities change.

**Why this priority**: Users need flexibility to change task attributes after creation as work evolves.

**Independent Test**: Can be fully tested by adding a task, updating its priority and tags, and verifying the changes are reflected.

**Acceptance Scenarios**:

1. **Given** the user has a task, **When** they update the priority, **Then** the task's priority changes to the new value.
2. **Given** the user has a task, **When** they update tags, **Then** the task's tags are replaced with the new list.
3. **Given** the user attempts to update a non-existent task, **When** they provide an invalid task ID, **Then** an error message is displayed.
4. **Given** the user attempts to add more than 5 tags, **When** they provide 6+ tags, **Then** an error message is displayed and tags are not updated.

---

### User Story 3 - Search Tasks by Keyword (Priority: P1)

As a user, I want to search for tasks by keyword so that I can quickly find specific tasks without scrolling through the entire list.

**Why this priority**: Search is a core usability feature that saves time when users have many tasks.

**Independent Test**: Can be fully tested by adding multiple tasks with different titles/descriptions, performing a search, and verifying only matching tasks are shown.

**Acceptance Scenarios**:

1. **Given** the user has tasks with various titles and descriptions, **When** they search for a keyword, **Then** tasks with that keyword in title OR description are shown.
2. **Given** the user searches for a keyword, **When** the search is performed, **Then** the matching is case-insensitive.
3. **Given** no tasks match the search keyword, **When** the user searches, **Then** a message indicating no tasks found is displayed.
4. **Given** the user has an active search, **When** they view tasks, **Then** only matching tasks are displayed.

---

### User Story 4 - Filter Tasks (Priority: P1)

As a user, I want to filter tasks by status, priority, and tag so that I can focus on specific subsets of tasks.

**Why this priority**: Filtering helps users manage large task lists by showing only relevant items.

**Independent Test**: Can be fully tested by adding tasks with different statuses, priorities, and tags, applying filters, and verifying only matching tasks are shown.

**Acceptance Scenarios**:

1. **Given** the user has tasks in various states, **When** they filter by status (all/pending/complete), **Then** only tasks matching that status are displayed.
2. **Given** the user has tasks with different priorities, **When** they filter by priority (all/HIGH/MEDIUM/LOW), **Then** only tasks with that priority are displayed.
3. **Given** the user has tasks with tags, **When** they filter by tag (exact match), **Then** only tasks containing that tag are displayed.
4. **Given** the user applies multiple filters, **When** they view tasks, **Then** all filter criteria are applied (AND logic).
5. **Given** the user clears filters, **When** they view tasks, **Then** all tasks are displayed regardless of filters.

---

### User Story 5 - Sort Tasks (Priority: P2)

As a user, I want to sort tasks by priority, alphabetical order, date added, or manually so that I can view tasks in my preferred order.

**Why this priority**: Sorting helps users focus on what matters most and is essential for task prioritization.

**Independent Test**: Can be fully tested by adding tasks with different priorities/dates, changing sort mode, and verifying tasks appear in the correct order.

**Acceptance Scenarios**:

1. **Given** the user sorts by priority, **When** viewing tasks, **Then** tasks appear in order HIGH → MEDIUM → LOW.
2. **Given** the user sorts alphabetically, **When** viewing tasks, **Then** tasks appear in A-Z order by title.
3. **Given** the user sorts by date added, **When** viewing tasks, **Then** newest tasks appear first.
4. **Given** the user sorts manually, **When** they use "up" and "down" commands, **Then** task order changes accordingly.
5. **Given** the user has a due date set, **When** they view tasks, **Then** the due date is displayed if set.

---

### User Story 6 - Clear Search and Filters (Priority: P2)

As a user, I want to clear all search and filter criteria with a single command so that I can return to viewing all tasks.

**Why this priority**: Users need an easy way to reset their view after searching or filtering.

**Independent Test**: Can be fully tested by applying search/filter, using the clear command, and verifying all tasks are shown.

**Acceptance Scenarios**:

1. **Given** the user has active search or filters, **When** they use the clear command, **Then** all search and filter criteria are removed.
2. **Given** the user clears filters, **When** they view tasks, **Then** all tasks are displayed without any filtering.

---

### User Story 7 - Persistent Task Storage (Priority: P1)

As a user, I want my tasks to persist between app sessions so that I can close and reopen the application without losing data.

**Why this priority**: Without persistence, users lose all data when closing the app, making the application impractical for real use.

**Independent Test**: Can be fully tested by adding tasks, closing the app, reopening it, and verifying tasks are still present.

**Acceptance Scenarios**:

1. **Given** the user has added tasks, **When** they exit and restart the application, **Then** all tasks are loaded from storage.
2. **Given** the user modifies tasks, **When** they exit the application, **Then** all changes are automatically saved.
3. **Given** the storage file is corrupted, **When** the application starts, **Then** a user-friendly error message is displayed and the app continues with an empty list.

---

### Edge Cases

- What happens when the user enters an invalid priority value?
  - System displays an error message listing valid options (HIGH, MEDIUM, LOW).
- What happens when the user enters tags with invalid characters?
  - System validates tags are lowercase with hyphens; displays error for invalid format.
- What happens when tasks are filtered and then a new task is added?
  - The new task is subject to current filter criteria and may or may not appear depending on filter state.
- How does the system handle sorting when tasks have the same priority or title?
  - Tasks maintain their relative order from previous operations (stable sort).
- What happens when the user tries to move a task beyond the boundaries during manual sort?
  - System displays an error and does not move the task.
- What happens when the storage file is missing on first run?
  - System creates a new empty storage file and proceeds normally.

## Requirements

### Functional Requirements

- **FR-001**: System MUST allow users to set task priority as HIGH, MEDIUM, or LOW during task creation.
- **FR-002**: System MUST default to MEDIUM priority when no priority is specified during task creation.
- **FR-003**: System MUST allow users to add up to 5 tags per task during task creation.
- **FR-004**: System MUST validate that tags are lowercase strings with hyphenated multi-word support.
- **FR-005**: System MUST reject task creation or updates with more than 5 tags and display an error.
- **FR-006**: System MUST allow users to update priority and tags on existing tasks.
- **FR-007**: System MUST provide case-insensitive search across task titles and descriptions.
- **FR-008**: System MUST display only matching tasks when a search is active.
- **FR-009**: System MUST filter tasks by status (all, pending, complete).
- **FR-010**: System MUST filter tasks by priority (all, HIGH, MEDIUM, LOW).
- **FR-011**: System MUST filter tasks by exact tag match.
- **FR-012**: System MUST apply all active filters simultaneously (AND logic).
- **FR-013**: System MUST provide a clear command to remove all search and filter criteria.
- **FR-014**: System MUST sort tasks by priority (HIGH → MEDIUM → LOW).
- **FR-015**: System MUST sort tasks alphabetically (A-Z by title).
- **FR-016**: System MUST sort tasks by date added (newest first).
- **FR-017**: System MUST support manual sorting with up/down commands by task ID.
- **FR-018**: System MUST provide optional due date field in YYYY-MM-DD format.
- **FR-019**: System MUST auto-save tasks to tasks.json on every modification.
- **FR-020**: System MUST load tasks from tasks.json on application startup.
- **FR-021**: System MUST display tasks in table format showing ID, title, priority, tags, status, and due date if set.
- **FR-022**: System MUST maintain search/filter/sort state when navigating between views.
- **FR-023**: System MUST provide user-friendly error messages for all validation failures.
- **FR-024**: System MUST preserve all existing basic features (add, view, update, delete, mark complete/incomplete).

### Key Entities

- **Task**: Represents a single todo item with intermediate features
  - `id` (integer, unique, auto-assigned): Unique identifier for the task
  - `title` (string, required): The task title
  - `description` (string, optional): Additional details about the task
  - `completed` (boolean): Whether the task is completed (default: false)
  - `priority` (string, enum): Priority level - HIGH, MEDIUM, or LOW (default: MEDIUM)
  - `tags` (list of strings): User-assigned labels, max 5, lowercase hyphenated format
  - `due_date` (string, optional): Due date in YYYY-MM-DD format for sorting purposes only
  - `order` (integer): Numeric value for manual sorting (default: 0)

- **TaskFilter**: Represents current filter state
  - `status` (string): all, pending, or complete
  - `priority` (string): all, HIGH, MEDIUM, or LOW
  - `tag` (string, optional): Exact tag to filter by

- **SortMode**: Enum for sorting behavior
  - `priority`: Sort by priority (HIGH → MEDIUM → LOW)
  - `alpha`: Sort alphabetically by title (A-Z)
  - `date_added`: Sort by creation date (newest first)
  - `manual`: Sort by order field with up/down commands

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can add a task with priority and tags within 10 seconds of starting the operation.
- **SC-002**: Users can search for tasks and see results within 2 seconds of submitting the search.
- **SC-003**: Users can apply or clear filters and see updated task list within 2 seconds.
- **SC-004**: Users can sort tasks by any mode and see results within 2 seconds.
- **SC-005**: 95% of users successfully add priority and tags on the first attempt.
- **SC-006**: 100% of valid operations succeed without system errors or crashes.
- **SC-007**: All error messages clearly indicate what the user did wrong and how to fix it.
- **SC-008**: Tasks persist correctly between sessions with 100% data integrity.
- **SC-009**: View commands respect current search/filter/sort settings.
- **SC-010**: Existing basic features (add, view, update, delete, mark complete/incomplete) remain fully functional.

## Assumptions

- The application runs in a standard terminal environment with minimum 80x24 character display.
- Tags follow the pattern: lowercase words separated by hyphens (e.g., "work-projects", "home-errands").
- Due dates are stored as strings in YYYY-MM-DD format but not validated for real dates or used for notifications.
- Manual sorting uses an integer order field that can be incremented/decremented with up/down commands.
- All search, filter, and sort operations are applied to the in-memory task list after loading from storage.
- Storage file (tasks.json) is located in the same directory as the application script.
- Task IDs remain stable and are not reused after deletion.
- The table view shows priority (H/M/L indicators), tags (comma-separated), status (X or space), and due date if set.

## Out of Scope

The following are explicitly out of scope for this intermediate enhancement:

- Recurring tasks or task repetition
- Reminders or notifications
- Web interface or API endpoints
- Database persistence (uses JSON file only)
- Multiple user accounts or authentication
- Task sharing or collaboration
- Task dependencies or sub-tasks
- Export or import functionality
- Undo/redo functionality
- Bulk operations (batch add, delete all)
- Color-coded terminal output (implementation detail)
- Date validation or calendar integration for due dates
- Time-based sorting or filtering
- Automatic sorting by due date
