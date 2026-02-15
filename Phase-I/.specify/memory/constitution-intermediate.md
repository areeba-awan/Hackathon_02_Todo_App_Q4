# Evolution of Todo Constitution: Intermediate Level Supplement

**Supplements**: Global Constitution v1.0.0+ | **Phase**: II (Full-Stack Web Application)
**Effective**: 2026-01-06 | **Version**: 1.0.0

This document is an addendum to the Global Constitution and governs all Phase II Intermediate Level development. In cases of conflict, the Global Constitution takes precedence.

---

## Core Principles (Phase II Extensions)

### I. Spec-Driven Development (Phase II Extension)

All Phase II development MUST follow the extended SDD workflow:

1. **Global Constitution** → The supreme governing document
2. **Intermediate Spec Update** → Feature specifications for priorities, tags, search, filter, sort
3. **Plan Revision** → Updated architectural decisions for web stack (FastAPI + Next.js)
4. **Tasks** → Testable tasks for intermediate features
5. **Implement** → Code execution following Red-Green-Refactor

**Rule**: No code changes without updated specs approved via `/sp.specify`. Deviations require spec re-review.

**Model Extension Requirements**:
- Priority field MUST be added as enum: `high` | `medium` | `low`
- Tags field MUST be added as array of strings
- Existing CRUD operations MUST remain functional (no breaking changes)
- All new fields MUST be optional for backward compatibility

**Rationale**: Ensures intermediate features extend rather than break the Phase I foundation.

---

### II. Agent Behavior Rules (Phase II Reinforcement)

Agents operating on Phase II Intermediate features MUST adhere to:

1. **No Feature Invention Beyond Scope**: Agents MUST NOT introduce features not in the intermediate spec.
   - Prohibited: Recurring tasks, reminders, notifications, sharing/collaboration
   - These are Phase III+ features and are strictly blocked
2. **No Specification Deviation**: Implementation MUST exactly match intermediate specifications
3. **Refinement at Spec Level**: Filter logic, search algorithms, or sort behavior changes require spec amendment
4. **Phase Isolation**: Architecture decisions MUST NOT include hooks for future-phase features

**Rationale**: Prevents scope leakage and maintains clean phase boundaries.

---

### III. Phase Governance (Intermediate Scope)

#### 3.1 Feature Scope (Phase II Only)

The following intermediate features are approved for Phase II:

| Feature | Description | Boundaries |
|---------|-------------|------------|
| **Priorities** | Assign priority levels to tasks | Values: `high`, `medium`, `low`. Default: `medium` |
| **Tags/Categories** | User-assignable labels | Free-form strings. Examples: `work`, `home`, `personal` |
| **Search** | Keyword-based search | Fields: `title`, `description`. Case-insensitive |
| **Filter** | Filter by status, priority, tag, date | Status: complete/incomplete. Date: due date range |
| **Sort** | Sort by due date, priority, alphabetical | Priority sort: high → medium → low |

#### 3.2 Integration Requirements

Intermediate features MUST integrate with basic Phase I features:

- **Add Task**: Include optional priority and tags inputs
- **Update Task**: Allow modifying priority and tags
- **View Task**: Display priority (visual indicator) and tags
- **Mark Complete**: Works unchanged; filters can exclude completed

#### 3.3 Architecture Evolution (Phase I → Phase II)

| Aspect | Phase I (Console) | Phase II (Web) |
|--------|-------------------|----------------|
| **Persistence** | In-memory Python list | Neon DB (PostgreSQL) |
| **Backend** | Python CLI | FastAPI REST APIs |
| **Frontend** | Console menu | Next.js dynamic UI |
| **State** | Runtime only | Database persisted |

**Rule**: All intermediate work MUST transition from in-memory to persistent storage.

---

### IV. Technology Stack Constraints (Phase II Specific)

#### 4.1 Approved Technologies

| Layer | Technology | Usage |
|-------|------------|-------|
| **Backend** | Python 3.11+ | Application logic |
| **Framework** | FastAPI | REST API endpoints |
| **ORM** | SQLModel | Database models and migrations |
| **Database** | Neon DB | PostgreSQL-compatible cloud persistence |
| **Frontend** | Next.js | Interactive web UI (task list, filters, sort) |
| **AI Framework** | OpenAI Agents SDK | Spec generation only (not runtime) |
| **Integration** | MCP | Tool/external system integration |

#### 4.2 Technology Prohibitions (Phase II)

The following are NOT approved for Phase II:

- Kafka or any message queue (Phase V)
- Kubernetes orchestration (Phase IV)
- Docker containers (Phase IV)
- AI/LLM in runtime application (Phase III)
- WebSocket or real-time updates (Phase III+)
- Authentication/user accounts (Phase III+)

#### 4.3 Database Schema Extensions

The Task model MUST be extended as follows:

```python
# New fields added to base Task model (backward compatible)
priority: Optional[str] = Field(default="medium", regex="^(high|medium|low)$")
tags: Optional[List[str]] = Field(default_factory=list, sa_column=JSON)
```

**Rationale**: Explicit schema ensures consistency across backend and frontend.

---

### V. Quality Principles (Phase II Application)

All Phase II code MUST adhere to these quality standards:

#### 5.1 Clean Architecture

- **API Layer**: FastAPI routes in `backend/src/api/`
- **Service Layer**: Business logic in `backend/src/services/`
- **Model Layer**: SQLModel entities in `backend/src/models/`
- **Frontend Components**: Next.js components in `frontend/src/components/`

#### 5.2 API Design Principles

- **Stateless**: All APIs MUST be stateless (no server-side session)
- **RESTful**: Standard HTTP methods (GET, POST, PUT, DELETE)
- **Validation**: Pydantic models for request/response validation
- **Error Handling**: Structured error responses with appropriate HTTP status codes

#### 5.3 Observability Requirements

All intermediate features MUST emit structured logs:

- **Search Operations**: Log query, result count, duration
- **Filter Operations**: Log filter criteria, result count
- **Sort Operations**: Log sort field and direction
- **Error Logging**: Log all failures with context

```python
# Example logging pattern
logger.info("Task filtered", extra={"filter": filter_params, "count": len(results)})
```

#### 5.4 Frontend Quality

- **Responsive Design**: Works on desktop and mobile
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages
- **Accessibility**: Basic ARIA labels and keyboard navigation

---

## Development Workflow (Phase II)

### Phase Transition Requirements (Phase I → II)

Before advancing from Phase I to Phase II:

1. ✅ All Phase I `tasks.md` items marked complete
2. ✅ All Phase I tests pass (unit and integration)
3. ✅ Code passes linting and security scanning
4. ✅ Phase I documentation reflects completion
5. ✅ Intermediate specs created and approved
6. ✅ Plan revision completed
7. ✅ Tasks generated for intermediate features

### Phase Transition Requirements (Phase II → III)

Before advancing from Phase II to Phase III (AI Chatbot):

1. ✅ All Phase II `tasks.md` items marked complete
2. ✅ All Phase II tests pass (unit, integration, E2E)
3. ✅ Web UI fully functional for all intermediate features
4. ✅ API endpoints tested and documented
5. ✅ Database migrations applied and verified
6. ✅ Phase III specs created and approved

### Specification Amendment Process (Phase II)

To modify an intermediate specification:

1. Identify the specific section requiring change
2. Document rationale: problem, impact, alternatives considered
3. Obtain stakeholder approval for the amendment
4. Update spec, plan, and tasks accordingly
5. Re-run affected task chains
6. Version increment following semantic versioning rules

**Rule**: Unapproved specification changes are prohibited.

---

## Governance

### Constitution Supremacy

This supplement is subordinate to the Global Constitution. In cases of conflict:
- Global Constitution rules apply
- This supplement provides Phase II specific extensions only

### Amendment Process

Constitutional amendments for Phase II require:

1. Documentation of proposed change with rationale
2. Review by all active contributors
3. Explicit user consent before adoption
4. Version increment following semantic versioning rules
5. Propagation to dependent templates and artifacts

### Compliance Verification

All code contributions MUST be verified for:
- Phase scope compliance (no Phase III+ features)
- Technology stack compliance (approved technologies only)
- Clean architecture compliance (separation of concerns)
- Observability compliance (logging for search/filter/sort)

### Versioning

| Version | Type | Description |
|---------|------|-------------|
| 1.0.0 | Initial | Initial Intermediate Level supplement |
| 1.0.0 | Ratified | 2026-01-06 |

---

## Sync Impact Report

### Version Change
- **Previous**: N/A (new document)
- **New**: 1.0.0
- **Bump Type**: Initial creation (no previous version)

### Templates Verified
| Template | Status | Notes |
|----------|--------|-------|
| `.specify/templates/spec-template.md` | ✅ Compatible | User story format works for intermediate features |
| `.specify/templates/plan-template.md` | ✅ Compatible | Constitution check section covers Phase II rules |
| `.specify/templates/tasks-template.md` | ✅ Compatible | Task organization by user story applies |

### Dependencies
This supplement depends on:
- Global Constitution v1.0.0 (supreme document)
- Phase II feature specifications (to be created)
- FastAPI + Next.js project structure (from plan template)

---

**End of Intermediate Level Supplement**
