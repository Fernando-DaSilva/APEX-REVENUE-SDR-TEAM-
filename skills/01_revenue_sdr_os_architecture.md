# SHARED SKILL: Revenue SDR OS System Architecture (ADR Summary)

## Core Architectural Overview

The **Revenue SDR OS** is built on a Zero-Trust multi-tenant architecture designed to process autonomous sales interactions.

### Key Architectural Components & ADR Highlights
- **ADR-001 - ADR-009**: Zero-Trust Multi-Tenancy via ContextVar `organization_id` & ASGI TenantResolutionMiddleware.
- **ADR-010 - ADR-012**: PostgreSQL Schema migrations via Alembic Batch mode; SQLModel table definition.
- **ADR-013 - ADR-015**: Hypermedia UI Jinja2/HTMX/Alpine.js with 5 White-Label themes & Structlog JSON logging.
- **ADR-018 - ADR-021**: JWT Auth with Argon2id + Taskiq background job queue powered by `TenantTaskiqMiddleware`.
- **ADR-022 - ADR-025**: RAG Engine with Supabase `pgvector` HNSW + Pydantic v2 `Instructor` schemas.
- **ADR-026 - ADR-029**: LangChain / LangGraph multi-agent orchestration, `AsyncPostgresSaver` persistent checkpointers, LangSmith telemetry.
- **ADR-030 - ADR-032**: TenantTaskiqMiddleware context propagation, Meta 24h WhatsApp HSM enforcement, Z-API anti-ban rate limiting (1 msg/3-5s).
- **ADR-033 - ADR-037**: Micro-Sprints (1h-4h), 5 Parallel Streams (ADR-035), Supabase Managed PostgreSQL 16+ integration (ADR-036, ADR-037).
