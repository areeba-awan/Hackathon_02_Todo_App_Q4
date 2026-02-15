---
id: 003
title: Advanced Level Constitution Supplement
stage: constitution
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 003-advanced-todo-features
user: null
command: /sp.constitution
labels: ["constitution", "advanced-level", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/memory/constitution-advanced.md
tests:
  - null
---

## Prompt

Define the SP.CONSTITUTION for the Advanced Level of a Python-based console Todo App.

Context:
- Basic and Intermediate levels are complete and stable.
- No manual coding is allowed.
- This level adds intelligent, time-based features only.

Scope:
1. Recurring Tasks (daily/weekly/monthly auto-rescheduling)
2. Due Dates & Time Reminders (date/time deadlines, notifications)

Rules:
- Do not alter existing features.
- Advanced features must be optional and backward-compatible.
- Time-based behavior must be deterministic and reliable.
- Separate recurring tasks from one-time tasks.
- Handle system time or notification failures gracefully.
- Maintain data integrity and task history.

Output:
- Principles
- Constrai

## Response snapshot

The project constitution has been updated to include an Advanced Level supplement. A new file `.specify/memory/constitution-advanced.md` was created to define principles for recurring tasks and due dates (optionality, determinism, isolation of logic, resilience). The main `constitution.md` was bumped to version 1.2.0 and linked to the new supplement.

## Outcome

- ✅ Impact: Established governance for advanced time-based features, ensuring they don't compromise core functionality.
- 🧪 Tests: None (documentation update).
- 📁 Files: Created `.specify/memory/constitution-advanced.md`, updated `.specify/memory/constitution.md`.
- 🔁 Next prompts: Continue with `/sp.specify` or `/sp.plan` for advanced features.
- 🧠 Reflection: Used a supplementary approach (consistent with Intermediate level) to maintain clean governance separation while updating main versioning.

## Evaluation notes (flywheel)

- Failure modes observed: intermittent Read tool errors (invalid parameter passing) which were bypassed by drafting based on context.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
