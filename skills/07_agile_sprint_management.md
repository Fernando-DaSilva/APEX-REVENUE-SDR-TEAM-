# SHARED SKILL: Agile Strategy & Micro-Sprint Management

## Core Principles

- **Micro-Sprint Sizing**: All tasks decomposed into atomic 1h to 4h deliverables.
- **5-Stream Coordination**: Sprints 01 through 10 scheduled across 5 parallel streams without blocking cross-stream deliverables (using OpenAPI 3.1 contracts).
- **Definition of Done (DoD)**:
  1. Code implemented in proper layer (`app/*/service.py`, `app/*/api.py`, `app/web/pages/`).
  2. Alembic migration batch tested round-trip.
  3. Sub-minute harness clean (`pytest >90%`, `ruff`, health check HTTP 200).
  4. Documentation updated in subagent `TASKS.md`.
