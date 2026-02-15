# Research: Advanced Todo Features

## Decision: Notification Strategy
**Chosen**: `plyer` or `notifypy` for cross-platform desktop notifications.
**Rationale**: These libraries provide a simple, Pythonic way to trigger system notifications on Windows, macOS, and Linux without external system dependencies.
**Alternatives Considered**:
- `win10toast`: Windows only (rejected for cross-platform support).
- `subprocess` with `notify-send`: Linux only (rejected).

## Decision: Recurrence Calculation
**Chosen**: Standard `datetime` and `relativedelta` from `python-dateutil`.
**Rationale**: `relativedelta` handles "Monthly" recurrence correctly (e.g., handles different month lengths and leap years) which standard `timedelta` cannot do easily.
**Alternatives Considered**:
- Custom logic with `timedelta`: Error-prone for months.

## Decision: Background Monitoring
**Chosen**: Simple polling mechanism within the main loop or a lightweight background thread.
**Rationale**: Given the "Console Application" constraint, a full background daemon is out of scope. We will check deadlines whenever the user interacts or using a short-lived thread while the app is open.
**Alternatives Considered**:
- `cron`/`systemd`: Too complex for an in-memory console app.

## Decision: Data Model Extension
**Chosen**: Update `Task` class with optional fields and a `recurring_parent_id`.
**Rationale**: Maintains backward compatibility while allowing tracking of the "lineage" of recurring tasks.
