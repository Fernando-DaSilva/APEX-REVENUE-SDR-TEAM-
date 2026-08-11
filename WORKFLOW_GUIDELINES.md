# WORKFLOW GUIDELINES & HARNESS SPECIFICATION

> **Standard Operating Procedure for All 10 Autonomous Subagents**  
> **Strict Execution Model**: 6-Layer Development Workflow, Micro-Sprints (1h-4h), Sub-Minute (<60s) CI Verification  

---

## 1. The 6-Layer Coding Workflow (ADR-033, ADR-034)

Every subagent executing code modifications in `Revenue_SDR_OS` must strictly follow this 6-step pipeline:

```
+-----------------------------------------------------------------------------------+
| 1. Read Specs & ADRs (FOUNDATION.md, ARCHITECTURE.md, Sprint Prompts)            |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 2. Database Schema & Migration (SQLModel -> alembic revision --autogenerate Batch)|
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 3. Domain Service Layer (app/*/service.py with mandatory organization_id filter)  |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 4. Schemas & Input Validation (Pydantic v2 / Instructor with strict validation)   |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 5. Presentation Layer & API (FastAPI thin routes / Jinja2 + HTMX pages)          |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 6. Harness Sub-Minute (< 60s) (pytest >90% + tenant 100% + ruff + alembic)        |
+-----------------------------------------------------------------------------------+
```

---

## 2. Pre-Commit Harness Execution Commands (< 60s Verification)

Before declaring any micro-sprint task completed, subagents must run and pass 100% of the verification suite:

```bash
# 1. Pytest suite: Coverage >90% + 100% cross-tenant isolation
pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=90

# 2. Ruff code formatting & linting
ruff check app/ tests/ scripts/ alembic/
ruff format --check app/ tests/ scripts/

# 3. Migration round-trip integrity test
alembic upgrade head && alembic downgrade -1 && alembic upgrade head

# 4. App Factory Boot & Health check
./start &
curl http://127.0.0.1:8000/api/v1/health/
```

---

## 3. Strict Anti-Patterns (Forbidden Actions)

```
[X] Query without organization_id filter       -> ALWAYS filter .where(Model.org_id == org_id)
[X] Returning HTTP 403 on cross-tenant lookup  -> Use generic HTTP 404 Not Found to prevent probing
[X] Extracting tenant_id from payload          -> ALWAYS read from ContextVar (current_organization)
[X] Dispatching Taskiq jobs without middleware  -> ALWAYS decorate broker with TenantTaskiqMiddleware
[X] Using MemorySaver checkpointer in Prod     -> ALWAYS use AsyncPostgresSaver checkpointer in Supabase
[X] LLM Router primary timeout > 900ms         -> Maintain <= 900ms for P95 SDR Agent SLA < 1.2s
[X] Sending freeform WhatsApp msgs after 24h   -> Enforce Meta 24h HSM template rule
[X] Micro-sprints exceeding 4 hours           -> Decompose into 1h-4h atomic tasks
[X] Raw HTTPException in service logic         -> Use AppError subclasses
[X] Manual JSON parsing of LLM outputs         -> Use Instructor + Pydantic v2 schemas
[X] Executing DB operations inside HTTP routes -> Move logic to app/*/service.py
[X] Bypassing Alembic PostgreSQL migrations     -> Use Alembic batch alter table DDL
```

---

## 4. Human Escalation & HR Evaluation Protocol

- **Human Escalation**: Managed by **Selena** (`09_Team_Secretary`). Unresolved blockers trigger emails to `fernando8cfo@gmail.com`.
- **HR Performance Governance**: Managed by **Helena** (`10_HR_AI_Specialist`). Evaluates task execution time, harness compliance, and skill upgrades.
