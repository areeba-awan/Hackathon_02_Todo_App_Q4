---
id: "002-001"
title: "Create intermediate features spec"
stage: "spec"
date: "2026-01-06"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "002-intermediate-todo"
branch: "002-intermediate-todo"
user: "Claude Code User"
command: "/sp.specify"
labels: ["spec-driven-development", "todo-app", "intermediate-features", "phase-1"]
links:
  spec: "specs/002-intermediate-todo/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/002-intermediate-todo/spec.md"
  - "specs/002-intermediate-todo/checklists/requirements.md"
tests:
  - "null"
---

## Prompt

Update specifications for Intermediate Level in "Evolution of Todo" project (Phase I console app). Current date: 2026-01-06. Extend existing basic features ONLY with intermediate usability features while staying in-memory Python console app.
Strictly follow global constitution (id:001) and intermediate supplement:

Spec-driven: Approve this spec first → plan → tasks → code.
No advanced features (no recurring tasks, no reminders).
No web/DB tech yet (keep pure Python console).
Prepare model for future Phase II migration.

Intermediate Features to Add:

Priorities & Tags
Priority: enum "HIGH" | "MEDIUM" | "LOW" (default "MEDIUM")
Tags: list[str] (max 5, lowercase, hyphenated multi-word, e.g. "personal-errands")
Add during task creation, editable via update

Search & Filter
Search: case-insensitive keyword in title/description
Filters (chainable): status (all/pending/complete), priority (all/HIGH/MEDIUM/LOW), tag (exact)
Commands: search <keyword>, filter status <value>, filter priority <value>, filter tag <value>, clear

Sort Tasks
Sort modes: priority (HIGH → LOW), alpha (title A-Z), date_added (newest first), manual
Add optional due_date (YYYY-MM-DD string) for future sort only (no validation/notification)
Manual reorder: up <id>, down <id>
Command: sort <priority|alpha|date_added|manual>


Updated Task Model (dataclass):
Python@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    priority: str = "MEDIUM"      # HIGH, MEDIUM, LOW
    tags: list[str] = field(default_factory=list)
    due_date: str | None = None   # YYYY-MM-DD, optional, sort only
    order: int = 0                # for manual sort
Requirements:

Persistence: auto save/load to tasks.json
View: table format showing priority, tags, status, due_date if set
Respect current search/filter/sort when viewing
Input validation + friendly error messages
Basic features remain fully functional

Deliverables:

Updated spec file: .specify/specs/phase1-intermediate.yaml
After approval: plan → implementation → tests

No code until spec approved. Store spec and proceed to /sp.plan next.

## Response snapshot

Created comprehensive specification for Phase I Intermediate features including:
- Extended Task model with priority (HIGH/MEDIUM/LOW), tags (max 5), due_date, and order fields
- Search functionality: case-insensitive keyword search in title/description
- Filter functionality: chainable filters for status, priority, and tag
- Sort functionality: priority, alpha, date_added, and manual sort modes
- Manual reorder with up/down commands by task ID
- JSON file persistence (auto save/load to tasks.json)
- Table view format showing all new fields
- Preserved all existing Phase I basic features
- Created quality checklist validating all requirements
- No [NEEDS CLARIFICATION] markers - spec is complete and ready for planning

## Outcome

- ✅ Impact: Created specification document for intermediate-level todo app enhancement extending Phase I console app with priorities, tags, search, filter, and sort capabilities
- 🧪 Tests: N/A - specification phase, no code implemented yet
- 📁 Files: specs/002-intermediate-todo/spec.md, specs/002-intermediate-todo/checklists/requirements.md
- 🔁 Next prompts: /sp.plan - proceed to architectural planning
- 🧠 Reflection: Specification follows spec-driven development methodology with user stories, acceptance scenarios, functional requirements, and measurable success criteria. All mandatory sections completed with no clarification needed.

## Evaluation notes (flywheel)

- Failure modes observed: "null"
- Graders run and results (PASS/FAIL): "null"
- Prompt variant (if applicable): "null"
- Next experiment (smallest change to try): "null"
