# Data Model: Advanced Todo

## Entities

### Task (Extended)
Represents a single task, either one-time or an instance of a recurring task.

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | Integer | Unique identifier (existing) |
| `description` | String | Task content (existing) |
| `is_complete` | Boolean | Completion status (existing) |
| `due_datetime` | DateTime (Optional) | The deadline for the task |
| `recurrence` | Enum | DAILY, WEEKLY, MONTHLY, NONE |
| `parent_id` | Integer (Optional) | ID of the task this instance was generated from |
| `reminder_sent` | Boolean | True if the system notification has been triggered |

## Relationships
- **Self-referential**: A task can have a `parent_id` pointing to the task that preceded it in a recurrence chain.
- **Lineage**: This allows tracing the history of a recurring task through multiple completions.

## Validation Rules
- `due_datetime` must be a valid future or past timestamp.
- `recurrence` can only be one of the specified enum values.
- If `recurrence` is not NONE, `due_datetime` is RECOMMENDED but not strictly required (defaults to creation time if missing).
