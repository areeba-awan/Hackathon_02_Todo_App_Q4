# Evolution of Todo: Advanced Level Supplement

This document serves as a specialized extension of the core Evolution of Todo Constitution, focusing on the governance of advanced features introduced in Phase III (and refined in later stages).

## Advanced Level Scope

The Advanced Level focuses exclusively on:
1. **Recurring Tasks**: Logic for daily, weekly, monthly, and custom interval repetition.
2. **Due Dates & Time Reminders**: Precise temporal deadlines and notification triggers.

## Advanced Principles

### I. Optionality & Backward Compatibility (MANDATORY)
Advanced features MUST be implemented as opt-in or secondary attributes.
- Core Todo operations (CRUD) MUST remain functional without time-based data.
- System MUST be able to load tasks that do not contain advanced attributes (due dates/recurrence) without error.
- **Rationale**: Ensures the system remains robust and accessible for users who prefer a simple workflow.

### II. Deterministic Time-Based Behavior
All date/time calculations and reminder triggers MUST be deterministic and verifiable.
- Use system UTC or well-defined local timezone handling.
- Success criteria for recurrence MUST be calculated ahead of time and validated against transition rules.
- **Rationale**: Time is a critical failure point in systems; deterministic behavior prevents "ghost" tasks or missed deadlines due to logic errors.

### III. Isolation of Recurring Logic
Recurring tasks are treated as a series defined by a single template/rule.
- Completing a recurring task MUST trigger the generation of the "Next Occurrence" as a separate, distinct task instance.
- Recurrence metadata MUST be preserved to maintain the chain, but instances should be independent for status tracking.
- **Rationale**: Prevents data duplication and ensures task history for each occurrence is accurate.

### IV. Data Integrity & History
The system MUST maintain the integrity of the recurrence chain and due date history.
- Modification of a recurrence rule MUST clearly define if it impacts future instances or just the current series.
- System MUST NOT lose task descriptions or priorities during the automated rescheduling process.
- **Rationale**: Advanced features should enhance, not compromise, the reliability of user data.

### V. Operational Resilience (Time/Notifications)
The system MUST handle environment-related failures gracefully.
- If a notification cannot be sent (e.g. app closed, system alert failure), the task MUST still be visually marked as "Overdue" or "Due Soon" upon next app interaction.
- System time drift or manual time changes MUST NOT cause duplicate recurring task creation.
- **Rationale**: Ensures the app remains useful as a "source of truth" even when external notification mechanisms fail.

## Governance

This supplement is subject to the same Amendment Process and Compliance Verification as defined in the primary Evolution of Todo Constitution.

**Version**: 1.0.0 | **Ratified**: 2026-01-07 | **Last Amended**: 2026-01-07
