# Implementation Tasks: Phase I Intermediate - Todo Console App Enhancement

**Feature Branch**: `002-intermediate-todo`
**Created**: 2026-01-06
**Spec**: [spec.md](spec.md)
**Plan**: [plan.md](plan.md)

## Overview

This document contains executable implementation tasks organized by user story. Each task is specific enough for an LLM to complete without additional context.

### Task Summary

| Metric | Count |
|--------|-------|
| Total Tasks | 42 |
| Setup Tasks | 5 |
| Foundational Tasks | 6 |
| User Story Tasks | 27 |
| Polish Tasks | 4 |

### User Story Summary

| Story | Priority | Tasks | Independent Test |
|-------|----------|-------|------------------|
| US1: Add Tasks with Priority/Tags | P1 | 5 | Add task with priority and tags, verify display |
| US2: Update Priority/Tags | P1 | 3 | Update task, verify changes reflected |
| US3: Search Tasks | P1 | 4 | Search, verify matching tasks shown |
| US4: Filter Tasks | P1 | 5 | Filter, verify only matching tasks shown |
| US5: Sort Tasks | P2 | 4 | Sort, verify correct order |
| US6: Clear Filters | P2 | 2 | Clear, verify all tasks shown |
| US7: Persistence | P1 | 4 | Restart app, verify tasks loaded |

---

## Phase 1: Setup

**Objective**: Initialize project structure and prepare for development.

### Tasks

- [X] T001 Create extended Task dataclass in src/models/task.py with priority, tags, due_date, order fields
- [X] T002 Create TaskFilter class in src/models/task_filter.py for filter state management
- [X] T003 Create SortMode enum in src/models/sort_mode.py with priority, alpha, date_added, manual values
- [X] T004 Add validation methods to Task dataclass for priority enum and tag format
- [X] T005 Add JSON serialization methods to Task dataclass for persistence

---

## Phase 2: Foundational

**Objective**: Implement core service layer and persistence. MUST complete before user story phases.

### Tasks

- [X] T006 Extend TodoService in src/services/todo_service.py with search, filter, sort state attributes
- [X] T007 Implement TodoService.load_tasks() method to load tasks from tasks.json on startup
- [X] T008 Implement TodoService.save_tasks() method to save tasks to tasks.json file
- [X] T009 Implement TodoService.get_tasks() method applying search, filter, and sort settings
- [X] T010 Create validation functions in src/services/validation.py for priority and tag input
- [X] T011 Create error messages module in src/services/errors.py for user-friendly messages

---

## Phase 3: User Story 1 - Add Tasks with Priority and Tags

**Priority**: P1
**Goal**: Users can add tasks with priority levels and tags.
**Independent Test**: Add task with priority and tags, then view to verify priority displayed and tags visible.

### Tests (Pre-implementation)

- [ ] T012 [P] [US1] Write unit tests for Task dataclass in tests/unit/test_task.py covering priority and tags

### Implementation

- [ ] T013 [US1] Extend add_task() method in src/services/todo_service.py to accept priority and tags parameters
- [ ] T014 [US1] Add priority and tags prompts to add command handler in src/cli/handlers.py
- [ ] T015 [US1] Update view command to display tasks in table format with priority, tags columns in src/cli/handlers.py
- [ ] T016 [US1] Auto-save to JSON after adding task with new fields
- [ ] T017 [US1] Test complete add workflow with priority and tags in integration test

---

## Phase 4: User Story 2 - Update Task Priority and Tags

**Priority**: P1
**Goal**: Users can modify priority and tags on existing tasks.
**Independent Test**: Add task, update priority and tags, verify changes reflected.

### Tests (Pre-implementation)

- [ ] T018 [P] [US2] Write unit tests for update_task method covering priority and tags updates

### Implementation

- [ ] T019 [US2] Extend update_task() method in src/services/todo_service.py to accept priority and tags
- [ ] T020 [US2] Add priority and tags prompts to update command handler in src/cli/handlers.py
- [ ] T021 [US2] Auto-save to JSON after updating task

---

## Phase 5: User Story 3 - Search Tasks by Keyword

**Priority**: P1
**Goal**: Users can search tasks by keyword (case-insensitive, title OR description).
**Independent Test**: Add multiple tasks, search, verify only matching tasks shown.

### Tests (Pre-implementation)

- [ ] T022 [P] [US3] Write unit tests for search_tasks method in tests/unit/test_service.py

### Implementation

- [ ] T023 [US3] Implement search_tasks() method in src/services/todo_service.py with case-insensitive matching
- [ ] T024 [US3] Add search command handler in src/cli/handlers.py accepting keyword argument
- [ ] T025 [US3] Update get_tasks() to apply active search term when returning tasks
- [ ] T026 [US3] Display "No tasks found" message when search yields no results

---

## Phase 6: User Story 4 - Filter Tasks

**Priority**: P1
**Goal**: Users can filter tasks by status, priority, and tag.
**Independent Test**: Add tasks with different attributes, apply filters, verify only matching tasks shown.

### Tests (Pre-implementation)

- [ ] T027 [P] [US4] Write unit tests for filter_tasks method covering status, priority, tag filters

### Implementation

- [ ] T028 [US4] Implement filter_tasks() method in src/services/todo_service.py for chainable filters
- [ ] T029 [US4] Add filter status command handler in src/cli/handlers.py
- [ ] T030 [US4] Add filter priority command handler in src/cli/handlers.py
- [ ] T031 [US4] Add filter tag command handler in src/cli/handlers.py
- [ ] T032 [US4] Update get_tasks() to apply all active filters with AND logic

---

## Phase 7: User Story 5 - Sort Tasks

**Priority**: P2
**Goal**: Users can sort tasks by priority, alpha, date_added, or manual.
**Independent Test**: Add tasks with different priorities/dates, change sort mode, verify correct order.

### Tests (Pre-implementation)

- [ ] T033 [P] [US5] Write unit tests for sort_tasks method covering all sort modes

### Implementation

- [ ] T034 [US5] Implement priority sort in src/services/todo_service.py (HIGH → MEDIUM → LOW)
- [ ] T035 [US5] Implement alpha sort in src/services/todo_service.py (A-Z by title)
- [ ] T036 [US5] Implement date_added sort in src/services/todo_service.py (newest first by ID)
- [ ] T037 [US5] Implement manual sort in src/services/todo_service.py (by order field)

---

## Phase 8: User Story 6 - Clear Search and Filters

**Priority**: P2
**Goal**: Users can reset all search and filter criteria with single command.
**Independent Test**: Apply search/filter, use clear command, verify all tasks shown.

### Implementation

- [ ] T038 [US6] Implement clear_filters() method in src/services/todo_service.py
- [ ] T039 [US6] Add clear command handler in src/cli/handlers.py

---

## Phase 9: User Story 7 - Persistent Task Storage

**Priority**: P1
**Goal**: Tasks persist between app sessions via JSON file.
**Independent Test**: Add tasks, restart app, verify tasks still present.

### Tests (Pre-implementation)

- [ ] T040 [P] [US7] Write integration tests for persistence in tests/integration/test_persistence.py

### Implementation

- [ ] T041 [US7] Implement JSON schema for tasks.json with version field
- [ ] T042 [US7] Handle corrupted/missing tasks.json gracefully with user-friendly error
- [ ] T043 [US7] Ensure all modifications trigger auto-save to JSON
- [ ] T044 [US7] Test complete persistence workflow (add, exit, restart, verify)

---

## Phase 10: Polish & Cross-Cutting Concerns

**Objective**: Final refinements and validation.

### Tasks

- [ ] T045 Write integration tests for manual reorder (up/down) commands in tests/integration/test_reorder.py
- [ ] T046 Implement move_task() method in src/services/todo_service.py for manual sorting
- [ ] T047 Add up and down command handlers in src/cli/handlers.py
- [ ] T048 Run all tests and verify 100% pass rate

---

## Dependency Graph

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational) ──────┐
    │                        │
    ▼                        │
US1 (Add Priority/Tags) ◄────┤ (depends on Phase 1, 2)
    │                        │
    ▼                        │
US2 (Update Priority/Tags) ◄─┤ (depends on US1)
    │                        │
    ▼                        │
US3 (Search) ◄───────────────┤ (depends on Phase 2)
    │                        │
    ▼                        │
US4 (Filter) ◄───────────────┤ (depends on Phase 2)
    │                        │
    ▼                        │
US5 (Sort) ◄─────────────────┤ (depends on Phase 2)
    │                        │
    ▼                        │
US6 (Clear) ◄────────────────┤ (depends on US3, US4)
    │                        │
    ▼                        │
US7 (Persistence) ◄──────────┤ (depends on Phase 1, 2)
    │                        │
    ▼                        │
Phase 10 (Polish) ◄──────────┘
```

---

## Parallel Execution Opportunities

### Within Phase 2 (Foundational)
- T006, T010, T011 can run in parallel (different files, no dependencies)

### Within User Stories
- Tests (T012, T018, T022, T027, T033, T040) can run in parallel with implementation tasks for same story
- US3 and US4 can be developed in parallel (both depend on Phase 2 only)

### Suggested MVP Scope
- Start with Phase 1, Phase 2, then US1 (Add Priority/Tags)
- This provides immediate value and validates the core model extension
- Then proceed through remaining user stories in priority order

---

## Implementation Strategy

### MVP (Minimum Viable Product)
1. Complete Phase 1 and Phase 2
2. Implement US1 (Add Tasks with Priority and Tags)
3. Verify Task model extension works correctly
4. This validates the data model and basic CRUD with new fields

### Incremental Delivery
After MVP, deliver features in this order:
1. US2 (Update Priority/Tags) - Complements US1
2. US7 (Persistence) - Critical for usability
3. US3 (Search) - Core usability feature
4. US4 (Filter) - Core usability feature
5. US5 (Sort) - Secondary usability
6. US6 (Clear) - Complements search/filter
7. Phase 10 (Polish) - Final refinements
