# Data Model: Phase I Intermediate - Todo Console App Enhancement

## Overview

This document defines the data structures and entities required for intermediate-level features. All models extend the Phase I base models without breaking existing functionality.

---

## Entities

### Task

**Purpose**: Represents a single todo item with intermediate features.

**Fields**:

| Field | Type | Required | Default | Validation | Notes |
|-------|------|----------|---------|------------|-------|
| `id` | int | Yes | auto | Unique, positive | Immutable after creation |
| `title` | str | Yes | - | Non-empty, max 200 chars | Primary identifier |
| `description` | str | No | "" | Max 1000 chars | Optional details |
| `completed` | bool | No | False | - | Task status |
| `priority` | str | No | "MEDIUM" | Enum: HIGH, MEDIUM, LOW | Task importance |
| `tags` | list[str] | No | [] | Max 5, lowercase hyphenated | Categorization |
| `due_date` | str | No | None | YYYY-MM-DD format | For display only |
| `order` | int | No | 0 | Integer | Manual sort order |

**Relationships**:
- Belongs to a TaskList (parent collection)
- No foreign keys (single-user, in-memory)

**State Transitions**:
- `completed`: `False` → `True` (via complete command)
- `completed`: `True` → `False` (via incomplete command)
- `priority`: Any → Any (via update command)
- `tags`: Any → Any (via update command)

**Example Instance**:
```python
Task(
    id=1,
    title="Buy groceries",
    description="Milk, eggs, bread",
    completed=False,
    priority="HIGH",
    tags=["personal-errands", "home"],
    due_date="2026-01-15",
    order=0
)
```

---

### TaskFilter

**Purpose**: Encapsulates the current filter state for viewing tasks.

**Fields**:

| Field | Type | Required | Default | Validation | Notes |
|-------|------|----------|---------|------------|-------|
| `status` | str | No | "all" | Enum: all, pending, complete | Task completion status |
| `priority` | str | No | "all" | Enum: all, HIGH, MEDIUM, LOW | Priority filter |
| `tag` | str | No | None | Exact tag match or None | Specific tag filter |

**Behavior**:
- All filters apply simultaneously (AND logic)
- `all` means no filtering on that criteria
- `None` tag means no tag filter active

**Example Instance**:
```python
TaskFilter(
    status="pending",
    priority="HIGH",
    tag=None
)
```

---

### SortMode

**Purpose**: Enumeration of available sorting behaviors.

**Values**:

| Value | Sort Key | Sort Direction | Notes |
|-------|----------|----------------|-------|
| `priority` | Priority enum value | HIGH → MEDIUM → LOW | By importance |
| `alpha` | Title (lowercase) | A → Z | Alphabetical |
| `date_added` | id | Descending | Newest first |
| `manual` | order field | Ascending | User-defined |

**Usage**: Passed to service layer to determine task display order.

---

## Validation Rules

### Priority Validation

```python
valid_priorities = {"HIGH", "MEDIUM", "LOW"}
# Input is normalized to uppercase
# Invalid values rejected with error message
```

### Tag Validation

```python
# Max 5 tags per task
max_tags = 5

# Tag format: lowercase letters and hyphens
# Pattern: ^[a-z]+(-[a-z]+)*$
# Examples: "work", "personal-errands", "home-projects"
```

### Due Date Format

```python
# Format: YYYY-MM-DD
# No validation of actual date validity
# Stored as string for display purposes
# Example: "2026-01-15"
```

---

## Persistence Schema

### JSON Storage Format

**File**: `tasks.json`

**Structure**:
```json
{
  "version": "2.0",
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "priority": "HIGH",
      "tags": ["personal-errands", "home"],
      "due_date": "2026-01-15",
      "order": 0
    }
  ],
  "next_id": 2,
  "filter_state": {
    "status": "all",
    "priority": "all",
    "tag": null
  },
  "sort_mode": "date_added"
}
```

**Notes**:
- `version` enables future migrations
- `filter_state` and `sort_mode` persist view preferences
- `next_id` tracks ID assignment for new tasks

---

## Service Layer Data Flow

### TodoService State

| Attribute | Type | Purpose |
|-----------|------|---------|
| `tasks` | list[Task] | In-memory task collection |
| `next_id` | int | ID counter for new tasks |
| `current_filter` | TaskFilter | Active filter criteria |
| `current_sort` | SortMode | Active sort mode |
| `search_term` | str \| None | Active search keyword |

### Operation: Add Task

```
Input: title, description, priority, tags, due_date
1. Create Task with next_id
2. Set order=0 for new task
3. Append to tasks list
4. Increment next_id
5. Persist to JSON
Output: Task instance
```

### Operation: Search

```
Input: keyword (string)
1. Set search_term = keyword.lower()
2. Return filtered tasks where keyword in title OR description
Output: list of matching Task instances
```

### Operation: Filter

```
Input: filter_type (status/priority/tag), value
1. Update current_filter.{filter_type} = value
2. Return tasks matching all filter criteria
Output: list of filtered Task instances
```

### Operation: Sort

```
Input: sort_mode (priority/alpha/date_added/manual)
1. Set current_sort = sort_mode
2. Sort tasks according to mode (stable sort)
Output: sorted list of Task instances
```

---

## UI Display Models

### Table Row Format

| Column | Width | Format | Notes |
|--------|-------|--------|-------|
| ID | 3 | Right-aligned | |
| Title | 20 | Left-aligned | Truncated if longer |
| Priority | 8 | Center-aligned | H/M/L indicator |
| Tags | 15 | Left-aligned | Comma-separated |
| Status | 8 | Center-aligned | [ ] or [x] |
| Due Date | 10 | - | YYYY-MM-DD or empty |

**Example Output**:
```
ID | Title                | Priority | Tags            | Status  | Due Date
1  | Buy groceries        | H        | home, personal  | [ ]     | 2026-01-15
2  | Call dentist         | M        | health          | [x]     |
```
