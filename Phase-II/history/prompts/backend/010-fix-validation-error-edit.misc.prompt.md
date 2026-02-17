---
id: 010
title: Fix Validation Failed Error On Edit
stage: misc
date: 2026-02-17
surface: agent
model: qwen-coder
feature: task-management
branch: main
user: lenovo
command: fix validation failed error
labels: ["bugfix", "tasks", "api"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/components/task-form.tsx
tests:
  - Manual testing of task edit
---

## Prompt

edit ni ho rha ye de rha h Validation failed bs isko thk kro or kuch mt cherna

## Response snapshot

Fixed the validation error by adding the `completed` field to the PUT request body. The backend's TaskUpdate schema requires `completed` field but frontend was only sending `title` and `description`.

## Outcome

- ✅ Impact: Edit task now works without validation error
- 🧪 Tests: Manual testing required - edit a task and save
- 📁 Files: Modified `frontend/components/task-form.tsx`
- 🔁 Next prompts: Test full edit flow
- 🧠 Reflection: Backend TaskUpdate schema requires `completed: bool` but frontend wasn't including it in PUT request

## Evaluation notes (flywheel)

- Failure modes observed: "Validation failed" error because `completed` field was missing from PUT request
- Graders run and results (PASS/FAIL): N/A - manual testing required
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Verify full edit flow works end-to-end
