# Evolution of Todo: Advanced Level Quickstart

## Overview
This guide covers the advanced features introduced in Phase I:
1. **Due Dates & Time Reminders**
2. **Recurring Tasks** (Daily, Weekly, Monthly)
3. **Desktop Notifications**

## Prerequisites
- Python 3.13
- Virtual Environment with `python-dateutil` and `plyer`

```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install python-dateutil plyer
```

## Running the App
```bash
python3 src/cli/main.py
```

## Using Advanced Features

### Setting a Deadline
When adding or updating a task, you will be prompted for a due date and time.
- Format: `YYYY-MM-DD` and `HH:MM`
- Example: `2026-01-07` at `14:00`

### Setting Recurrence
Choose from the following options when prompted:
- `none`: One-time task
- `daily`: Reschedules for the same time tomorrow
- `weekly`: Reschedules for the same time next week
- `monthly`: Reschedules for the same time next month

### Notifications
- System/Desktop notifications will trigger 15 minutes before the deadline.
- If system notifications are unavailable, a banner will appear in the console.

## Backward Compatibility
Existing tasks without advanced fields will be displayed normally and can be updated to include deadlines or recurrence.
