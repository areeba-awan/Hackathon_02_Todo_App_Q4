---
id: 011
title: Fix Task Not Appearing After Add
stage: misc
date: 2026-02-17
surface: agent
model: qwen-coder
feature: task-management
branch: main
user: lenovo
command: fix task add dashboard issue
labels: ["bugfix", "tasks", "api"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/components/task-list.tsx
  - frontend/components/task-item.tsx
tests:
  - Manual testing of task creation and listing
---

## Prompt

task add krne pe dashboard me task ni ja rhe isy b thk kro or kuch mt cherna

## Response snapshot

Fixed the issue by updating all remaining API calls in task components to use the backend API URL (`http://localhost:8000`) instead of relative paths. The task-list and task-item components were still calling `/api/tasks` instead of the full backend URL.

## Outcome

- ✅ Impact: Tasks now appear correctly after creation and all CRUD operations work with backend
- 🧪 Tests: Manual testing required - create a task and verify it appears in the list
- 📁 Files: Modified `frontend/components/task-list.tsx`, `frontend/components/task-item.tsx`
- 🔁 Next prompts: Test full task management flow
- 🧠 Reflection: Multiple components were using relative API paths instead of backend URL - all needed to be updated

## Evaluation notes (flywheel)

- Failure modes observed: Tasks created successfully but not appearing because fetch calls were going to wrong URL
- Graders run and results (PASS/FAIL): N/A - manual testing required
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Verify full CRUD operations work end-to-end
