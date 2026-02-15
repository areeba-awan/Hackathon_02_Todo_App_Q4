# Research & Design Decisions: Phase I Intermediate - Todo Console App Enhancement

## Overview

This document captures the technical design decisions made for implementing intermediate-level features in the Phase I todo console application.

---

## 1. Task Data Model Extension

### Decision: Extend Task dataclass with new fields

**Chosen Approach**: Add new fields to existing Task dataclass while preserving backward compatibility.

| Field | Type | Default | Validation |
|-------|------|---------|------------|
| `id` | int | auto-increment | Unique, immutable |
| `title` | str | - | Non-empty, max 200 chars |
| `description` | str | "" | Optional, max 1000 chars |
| `completed` | bool | False | - |
| `priority` | str | "MEDIUM" | Enum: HIGH, MEDIUM, LOW |
| `tags` | list[str] | [] | Max 5, lowercase hyphenated |
| `due_date` | str \| None | None | YYYY-MM-DD format |
| `order` | int | 0 | Integer for manual sorting |

**Rationale**:
- Maintains existing Phase I structure with minimal changes
- New fields are optional to preserve backward compatibility
- Field ordering puts core fields first, new intermediate fields last

**Alternatives Considered**:
- Separate PriorityTask and TaggedTask classes → Rejected (complexity)
- JSON-only storage of new fields → Rejected (inconsistent with existing pattern)

---

## 2. Priority Enum

### Decision: Store as uppercase string enum

**Chosen Format**: `HIGH`, `MEDIUM`, `LOW` (stored as strings)

**Rationale**:
- Simple string comparison for sorting (HIGH > MEDIUM > LOW)
- Human-readable in JSON storage
- No additional enum library needed

**Alternatives Considered**:
- Integer mapping (3, 2, 1) → Rejected (less readable)
- Python Enum class → Rejected (adds complexity for simple use case)

**Sort Order**: HIGH (3) > MEDIUM (2) > LOW (1)

---

## 3. Tag Validation

### Decision: Enforce lowercase hyphenated format

**Chosen Format**: Regex pattern `^[a-z]+(-[a-z]+)*$`

**Examples**:
- ✅ `work`, `home`, `personal-errands`
- ❌ `Work`, `home errand`, `personal errand`

**Rationale**:
- Consistent storage (no case variations)
- Multi-word tags supported via hyphens
- Simple to validate and display

**Alternatives Considered**:
- Allow any string → Rejected (inconsistent)
- Space-separated multi-word → Rejected (harder to parse)

---

## 4. Due Date Storage

### Decision: Store as string in YYYY-MM-DD format, no validation

**Chosen Approach**: Optional string field with no date validation

**Rationale**:
- Format matches ISO 8601 for future compatibility
- No validation needed per spec (for future sort only)
- Simple string comparison if sorting by date

**Limitations** (by design):
- No date validity check (invalid dates accepted)
- No notification or reminder functionality
- Not used for sorting per spec

---

## 5. Manual Sort Order Field

### Decision: Integer field with increment/decrement

**Chosen Approach**: `order` integer field, tasks sorted by order ascending

**Rationale**:
- Simple integer arithmetic for reordering
- Stable - gaps allow insertion without renumbering all tasks
- `order=0` means "use default position" (append to end)

**Operations**:
- `up <id>`: order += 1 (move down in list)
- `down <id>`: order -= 1 (move up in list)

**Alternatives Considered**:
- Linked list → Rejected (complexity)
- Floating point between neighbors → Rejected (precision issues)

---

## 6. Search Algorithm

### Decision: Case-insensitive substring match in title OR description

**Chosen Approach**: `keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower()`

**Rationale**:
- Simple and intuitive
- Matches user expectations for keyword search
- OR logic finds tasks matching in either field

**Behavior**:
- `search project` matches "Start project Alpha" and "Write documentation for the project"
- Search is applied after filters

---

## 7. Filter Logic

### Decision: Multi-criteria AND logic

**Chosen Approach**: All active filters apply simultaneously

**Filter Options**:

| Filter | Values | Default |
|--------|--------|---------|
| status | all, pending, complete | all |
| priority | all, HIGH, MEDIUM, LOW | all |
| tag | exact tag string | all |

**Examples**:
- `filter status pending` → Show only incomplete tasks
- `filter priority HIGH` → Show only high priority tasks
- `filter tag work` → Show only tasks with "work" tag
- Combined: `filter status pending` + `filter priority HIGH` → Show incomplete HIGH priority tasks

**Rationale**:
- AND logic is more intuitive than OR
- Users can narrow down progressively
- Clear command resets all filters at once

---

## 8. Sort Modes

### Decision: Four sort modes with stable sorting

**Sort Modes**:

| Mode | Key | Order |
|------|-----|-------|
| priority | priority value | HIGH → MEDIUM → LOW |
| alpha | title (lowercase) | A → Z |
| date_added | id | Newest first (higher id) |
| manual | order field | Ascending order value |

**Rationale**:
- Priority sort matches real-world importance ordering
- Alpha sort useful for finding specific tasks
- Date added uses existing ID (monotonically increasing)
- Manual sort allows custom ordering

**Stability**: When keys are equal, maintain relative order from previous state.

---

## 9. Persistence Format

### Decision: JSON file with array of task objects

**File**: `tasks.json` in application directory

**Format**:
```json
[
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
]
```

**Rationale**:
- Human-readable for debugging
- Standard Python json module (no dependencies)
- Append-friendly for atomic saves

**Operations**:
- Load: Read and parse JSON on startup
- Save: Write entire list to file after every modification

---

## 10. Table View Format

### Decision: Fixed-width columns with status indicators

**Display Format**:
```
ID | Title        | Priority | Tags         | Status | Due Date
1  | Buy groceries| H        | home,personal| [ ]    | 2026-01-15
2  | Call dentist | M        | health       | [x]    |
```

**Indicators**:
- Priority: `H` (HIGH), `M` (MEDIUM), `L` (LOW)
- Status: `[ ]` (incomplete), `[x]` (complete)
- Tags: Comma-separated, truncated if too long

**Rationale**:
- Compact yet readable
- Matches user expectations for todo apps
- Respect current search/filter/sort settings

---

## 11. Error Handling Strategy

### Decision: User-friendly messages with recovery suggestions

**Error Categories**:

| Category | Message Style | Example |
|----------|---------------|---------|
| Validation | "Error: <what> is invalid. <how to fix>" | "Error: Priority must be HIGH, MEDIUM, or LOW." |
| Not Found | "Error: Task <id> not found." | "Error: Task 5 not found." |
| Limit Exceeded | "Error: Maximum <n> <items> allowed. You have <current>." | "Error: Maximum 5 tags allowed. You have 6." |
| Invalid Input | "Error: <input> is not valid. <expected format>" | "Error: 'urgent' is not valid. Use HIGH, MEDIUM, or LOW." |

---

## 12. Integration with Basic Features

### Decision: Extend, not replace existing Phase I features

**Preserved Behaviors**:
- `add` command: Still works, new optional prompts for priority/tags
- `view` command: Still works, shows new columns
- `update` command: Still works, adds priority/tag modification options
- `delete` command: Unchanged
- `complete` / `incomplete` commands: Unchanged

**New Commands Added**:
- `search <keyword>`: Search tasks
- `filter <criteria>`: Filter tasks
- `sort <mode>`: Sort tasks
- `up <id>` / `down <id>`: Manual reorder
- `clear`: Reset search/filter/sort

**Backward Compatibility**: All existing workflows remain identical unless the user explicitly uses new features.
