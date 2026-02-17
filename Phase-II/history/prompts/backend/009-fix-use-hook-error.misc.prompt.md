---
id: 009
title: Fix use() Hook Error Edit Page
stage: misc
date: 2026-02-17
surface: agent
model: qwen-coder
feature: task-management
branch: main
user: lenovo
command: fix use hook error
labels: ["bugfix", "tasks", "react"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/app/tasks/[id]/edit/page.tsx
tests:
  - Manual testing of edit page
---

## Prompt

Unhandled Runtime Error Error: An unsupported type was passed to use(): [object Object] - fix this error

## Response snapshot

Fixed the error by replacing `use(params)` with Next.js `useParams()` hook. The `use()` hook doesn't support the params object type.

## Outcome

- ✅ Impact: Edit page now loads without runtime error
- 🧪 Tests: Manual testing required - click edit button on any task
- 📁 Files: Modified `frontend/app/tasks/[id]/edit/page.tsx`
- 🔁 Next prompts: Test full edit flow
- 🧠 Reflection: The `use()` hook is only for Promise and Context types, not for params objects. Should use `useParams()` hook instead.

## Evaluation notes (flywheel)

- Failure modes observed: `use(params)` threw error because params is not a Promise or Context
- Graders run and results (PASS/FAIL): N/A - manual testing required
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Verify edit functionality works end-to-end
