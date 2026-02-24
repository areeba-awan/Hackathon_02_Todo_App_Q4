---
id: 006
title: Fix Task Edit Button Functionality
stage: misc
date: 2026-02-17
surface: agent
model: qwen-coder
feature: task-management
branch: main
user: lenovo
command: fix edit button on tasks
labels: ["bugfix", "tasks", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/app/tasks/[id]/page.tsx
  - frontend/components/task-form.tsx
tests:
  - Manual testing of edit task flow
---

## Prompt

ab tasks me edit k button pe click krne pe km ni ho rha edit ka isy thk kro or kuch mt cherna

## Response snapshot

Fixed the edit button functionality by:
1. Updated `/tasks/[id]/page.tsx` to fetch actual task data from backend API instead of using mock data
2. Updated `task-form.tsx` to use PUT request for editing existing tasks and POST for creating new ones
3. Added proper API URL configuration to connect to backend at `http://localhost:8000`

## Outcome

- ✅ Impact: Edit button now correctly fetches task data from backend and allows updating tasks via PUT request
- 🧪 Tests: Manual testing required - click edit button on a task, modify fields, and save
- 📁 Files: Modified `frontend/app/tasks/[id]/page.tsx`, `frontend/components/task-form.tsx`
- 🔁 Next prompts: Test full edit flow with backend running
- 🧠 Reflection: The issue was that the edit page used hardcoded mock data instead of fetching from the API, and the form only supported POST (create) not PUT (update)

## Evaluation notes (flywheel)

- Failure modes observed: Edit page showed static mock data instead of actual task; form submission only had POST logic
- Graders run and results (PASS/FAIL): N/A - manual testing required
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Ensure backend is running on port 8000 before testing edit functionality
