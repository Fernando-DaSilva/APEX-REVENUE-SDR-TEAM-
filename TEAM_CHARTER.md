# TEAM CHARTER — APEX REVENUE SDR SOFTWARE TEAM

> **Team Codename**: `AGENCY-SDR-ENGINEERS`  
> **Target Product**: Revenue SDR OS (Conversational Autonomous SDR Operating System)  
> **Execution Model**: Hyper-Accelerated 60-Day / 8-Week Roadmap across 5 Parallel Development Streams & Micro-Sprints (1h to 4h)  

---

## 1. Mission & Core Purpose

The **APEX REVENUE SDR SOFTWARE TEAM** is an autonomous multi-agent engineering organization dedicated to constructing the **Revenue SDR OS**. Our fundamental mission is:

> *"Nunca mais perca um lead por falta de acompanhamento. O cliente compra agenda cheia."*

We build a Zero-Trust multi-tenant sales platform driven by 6 AI Brains, hypermedia UX, Supabase PostgreSQL, and resilient async task queues.

---

## 2. Team Architectural Invariants (Non-Negotiable Rules)

Every subagent member of the APEX Team must strictly uphold these 17 invariants:

1. **App Factory Pattern**: `create_app(settings, db_engine)` — state resides strictly in `app.state`, no module singletons.
2. **Strict Layering**: Route Handler -> Service Layer (`app/*/service.py`) -> Database Model. Database queries are strictly forbidden inside route handlers.
3. **Zero-Trust Multi-Tenancy**: Every table model includes `organization_id` FK NOT NULL. All service queries filter by ContextVar `organization_id`. Cross-tenant queries return generic `404 Not Found`.
4. **Structured Error Handling**: All exceptions inherit from `AppError` and render standard envelopes `{"error": {"code": ..., "message": ..., "details": ...}}`. `HTTPException` is forbidden.
5. **Schema Validation in Pydantic v2**: Table models (`SQLModel table=True`) do NOT validate input. All incoming payloads pass through Pydantic / Instructor schemas.
6. **PostgreSQL Migrations via Alembic Batch Mode**: DDL schema changes execute via Alembic migrations using `op.batch_alter_table`. `create_all()` is restricted to tests.
7. **Dual Authentication**: Cookie (precedence) + Bearer token. Password hashing via Argon2id (`pwdlib`), JWT HS256 with `jti` invalidation.
8. **ContextVar Tenant Precedence**: `organization_id` is extracted strictly from ContextVar, never from incoming request payloads.
9. **Async Background Jobs via Taskiq**: Webhooks return HTTP 202 in $< 50\text{ ms}$ and delegate work to Taskiq using `TenantTaskiqMiddleware` to propagate tenant ContextVar.
10. **Multi-Agent Orchestration via LangChain & LangGraph**: Conversational workflows use `langchain-core` and LangGraph `StateGraph` with `AsyncPostgresSaver` persistent checkpointers. `MemorySaver` in production is forbidden.
11. **Strict Performance SLAs (P95)**: Supabase PostgreSQL pooled query $< 15\text{ ms}$, Core API $< 50\text{ ms}$, SSE $< 100\text{ ms}$, SDR Agent response $< 1.2\text{ s}$ with LLM fallback timeout at 900ms.
12. **Full Observability**: 100% of LangGraph runs stream telemetry to LangSmith labeled with `organization_id`. Application logs use Structlog JSON Lines.
13. **Valkey/Redis & Local Caching**: White-label themes, JWT blacklists, and rate limits use multi-tier caching.
14. **Supabase PostgreSQL & Vector Architecture**: Unified Supabase Managed PostgreSQL 16+ with `pgvector` HNSW index ($< 15\text{ ms}$) and `tsvector` BM25 RRF for hybrid RAG search.
15. **Meta WhatsApp 24h Window & Anti-Ban Compliance**: Freeform messages blocked after 24h window (forcing approved HSM templates). Outbound rate limits (1 msg/3-5s) with human jitter (2s-6s) and `composing` status.
16. **Autonomous Execution in Micro-Sprints (1h-4h)**: Tasks decomposed into atomic 1h-4h micro-sprints backed by sub-minute ($< 60\text{s}$) CI verification.
17. **Topological Respect to 5 Streams**: Independent development adhering strictly to OpenAPI 3.1 contracts.

---

## 3. The 5 Parallel Development Streams (ADR-035)

```
+------------------------------------------------------------------------------------+
| Stream 1: Core Architecture, Multi-Tenancy & Database (Aria + Silas)              |
| Stream 2: AI Multi-Agent Engine, LangGraph & Hybrid RAG (Atlas)                    |
| Stream 3: Async Queue, Taskiq Workers & Realtime SSE Engine (Bruno)               |
| Stream 4: Hypermedia White-Label UI & Prototype Integration (Fiona)               |
| Stream 5: Zero-Trust Security, VPS Automation & QA Harness (Sentinel + Quinn)      |
+------------------------------------------------------------------------------------+
       ^                                                                   ^
       |                                                                   |
   Agile & Capacity Governance                                   Human Liaison & Comms
   (Pax + Helena)                                               (Selena -> fernando8cfo@gmail.com)
```

---

## 4. Human Liaison & Escalation Protocol (Selena & Pax)

When any team member encounters a blocker requiring human intervention (credentials, domain decisions, third-party API keys, design sign-off):

1. **Subagent** flags issue to **Pax** (`08_Project_Manager`) and **Selena** (`09_Team_Secretary`).
2. **Pax** evaluates if an autonomous architectural decision can be made under existing ADRs.
3. If human action is strictly required, **Selena** dispatches an escalation notification to **Fernando** at `fernando8cfo@gmail.com`.
4. **Selena** tracks the pending approval state until Fernando responds.
