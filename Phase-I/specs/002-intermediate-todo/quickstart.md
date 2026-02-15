# Quickstart: Phase I Intermediate - Todo Console App Enhancement

## Overview

This guide helps you quickly understand and use the intermediate-level features added to the Todo Console App.

---

## What's New

### Priority Levels

Assign importance to your tasks:

| Priority | Indicator | Description |
|----------|-----------|-------------|
| HIGH | H | Urgent/important tasks |
| MEDIUM | M | Normal tasks (default) |
| LOW | L | Low priority tasks |

### Tags

Categorize your tasks with labels:

- Up to 5 tags per task
- Use lowercase with hyphens for multi-word: `personal-errands`, `work-projects`
- Examples: `work`, `home`, `health`, `finance`, `learning`

### Search

Find tasks quickly:

- Case-insensitive keyword search
- Searches both title and description
- Use: `search <keyword>`

### Filter

Narrow down your view:

- `filter status pending|complete|all`
- `filter priority HIGH|MEDIUM|LOW|all`
- `filter tag <tag_name>`
- Multiple filters combine with AND logic

### Sort

Control task order:

| Mode | Order |
|------|-------|
| `sort priority` | HIGH → MEDIUM → LOW |
| `sort alpha` | A → Z by title |
| `sort date_added` | Newest first |
| `sort manual` | Custom order |

### Manual Reorder

Fine-tune your task order:

- `up <id>` - Move task down in list
- `down <id>` - Move task up in list

### Persistence

Tasks now save automatically:

- Tasks persist between sessions
- Stored in `tasks.json` file
- Loads automatically on startup

---

## Usage Examples

### Adding Tasks with Priority and Tags

```
$ add
Enter task title: Buy groceries
Enter description (optional): Milk, eggs, bread, butter
Enter priority (HIGH/MEDIUM/LOW) [MEDIUM]: HIGH (
Enter tagscomma-separated, max 5): home, personal-errands
Task added successfully! [ID: 1]
```

### Searching for Tasks

```
$ search groceries
=== Search Results (1 task) ===
ID | Title       | Priority | Tags            | Status
1  | Buy groceries| H       | home, personal  | [ ]

$ search
Current search: "groceries"
```

### Filtering Tasks

```
$ filter status pending
Showing 3 pending tasks

$ filter priority HIGH
Showing 2 HIGH priority pending tasks

$ filter tag work
Showing 1 HIGH priority, pending, work task
```

### Sorting Tasks

```
$ sort priority
Tasks sorted by priority (HIGH → MEDIUM → LOW)

$ sort alpha
Tasks sorted alphabetically

$ sort date_added
Tasks sorted newest first (default)

$ sort manual
Tasks sorted by custom order
```

### Reordering Tasks Manually

```
$ view
ID | Title     | Priority
1  | Task A    | H
2  | Task B    | H
3  | Task C    | H

$ down 2
Task 2 moved up

$ view
ID | Title     | Priority
1  | Task A    | H
3  | Task C    | H
2  | Task B    | H
```

### Clearing All Filters

```
$ clear
All filters cleared. Showing all tasks.
Current sort: date_added
```

### Viewing the Table

```
$ view
=== All Tasks ===
ID | Title            | Priority | Tags         | Status | Due Date
1  | Buy groceries    | H        | home,personal| [ ]    | 2026-01-15
2  | Call dentist     | M        | health       | [x]    |
3  | Finish report    | H        | work         | [ ]    | 2026-01-20
```

---

## Command Reference

### New Commands

| Command | Description |
|---------|-------------|
| `search <keyword>` | Search tasks by keyword |
| `filter status <value>` | Filter by completion status |
| `filter priority <value>` | Filter by priority |
| `filter tag <value>` | Filter by tag |
| `sort <mode>` | Change sort mode |
| `up <id>` | Move task down in manual sort |
| `down <id>` | Move task up in manual sort |
| `clear` | Clear all search/filter/sort |

### Unchanged Commands

| Command | Description |
|---------|-------------|
| `add` | Add a new task |
| `view` | View all tasks |
| `update <id>` | Update a task |
| `delete <id>` | Delete a task |
| `complete <id>` | Mark complete |
| `incomplete <id>` | Mark incomplete |
| `help` | Show help |
| `exit` | Exit application |

---

## Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "Priority must be HIGH, MEDIUM, or LOW" | Invalid priority input | Use valid priority value |
| "Maximum 5 tags allowed" | Too many tags | Reduce to 5 or fewer |
| "Task X not found" | Invalid task ID | Check task ID with `view` |
| "Tags must be lowercase with hyphens" | Invalid tag format | Use format like `work-projects` |

---

## File Location

- **Storage file**: `tasks.json` (in same directory as application)
- **Auto-save**: Every modification is saved automatically
- **Backup**: File can be backed up manually if needed

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Enter | Submit input |
| Ctrl+C | Cancel current operation |
| Esc | Return to main menu |

---

## Next Steps

1. Review the [specification](spec.md) for full requirements
2. Review the [plan](plan.md) for implementation details
3. Run `/sp.tasks` to generate implementation tasks
4. Run `/sp.implement` to execute development
