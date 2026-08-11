# APEX REVENUE SDR SOFTWARE TEAM (Codename: AGENCY-SDR-ENGINEERS)

Welcome to the **05_SDR_Software_Team** workspace directory. This folder houses the multi-agent software engineering team structure, individual subagent workspaces, shared technical skills, workflow rules, and calendar of deliverables for building the **Revenue SDR OS** project.

---

## 1. Team Overview & Named Roster

The **APEX REVENUE SDR SOFTWARE TEAM** is composed of 10 specialized autonomous subagent roles collaborating under a hyper-accelerated 60-day roadmap across 5 parallel development streams.

| Subagent Directory | Agent Name | Primary Role & Specialization | Key Responsibilities |
|---|---|---|---|
| [`01_Enterprise_Architect`](file:///Volumes/Workspace_iOS/AGENCIA/05_SDR_Software_Team/01_Enterprise_Architect/MANIFEST.md) | **Aria** | Principal Enterprise & System Architect | Topology in 5 streams (ADR-035), OpenAPI 3.1 contracts, zero-trust invariants, architecture decisions (ADRs). |
| [`02_AI_Systems_Engineer`](file:///Volumes/Workspace_iOS/AGENCIA/05_SDR_Software_Team/02_AI_Systems_Engineer/MANIFEST.md) | **Atlas** | AI Multi-Agent & RAG Systems Lead | LangChain & LangGraph StateGraph, 6 AI Brains, Instructor/Pydantic schemas, fallback LLM router (900ms). |
| [`03_Backend_Async_Engineer`](file:///Volumes/Workspace_iOS/AGENCIA/05_SDR_Software_Team/03_Backend_Async_Engineer/MANIFEST.md) | **Bruno** | Senior Backend & Async Data Lead | FastAPI domain services (`app/*/service.py`), Taskiq background jobs with `TenantTaskiqMiddleware`, SSE broker. |
| [`04_Frontend_Hypermedia_Engineer`](file:///Volumes/Workspace_iOS/AGENCIA/05_SDR_Software_Team/04_Frontend_Hypermedia_Engineer/MANIFEST.md) | **Fiona** | Senior Frontend & Hypermedia UX Lead | Jinja2 + HTMX + Alpine.js hypermedia desconstruction, White-label themes (`01_SDR_Prototype`), 3-Column Zap Copilot & Chart.js (`02_ZAP_Prototype`). |
| [`05_Security_DevSecOps_Engineer`](file:///Volumes/Workspace_iOS/AGENCIA/05_SDR_Software_Team/05_Security_DevSecOps_Engineer/MANIFEST.md) | **Sentinel** | Zero-Trust Security & DevSecOps Lead | Supabase PostgreSQL RLS policies, Argon2id/PyJWT auth, OWASP Top 10 API Security, single-tenant VPS automation. |
| [`06_QA_Harness_Director`](file:///Volumes/Workspace_iOS/AGENCIA/05_SDR_Software_Team/06_QA_Harness_Director/MANIFEST.md) | **Quinn** | QA Director & Verification Harness Lead | Multi-tenant Pytest isolation (>90% coverage), ruff linting, sub-minute (<60s) migration round-trip harness, visual QA. |
| [`07_Database_Supabase_Specialist`](file:///Volumes/Workspace_iOS/AGENCIA/05_SDR_Software_Team/07_Database_Supabase_Specialist/MANIFEST.md) | **Silas** | Supabase PostgreSQL & Vector Specialist | Supabase Managed PostgreSQL 16+, Supavisor pooler, `pgvector` HNSW + `tsvector` BM25 RRF, Alembic batch migrations, query P95 SLA (<15ms). |
| [`08_Project_Manager`](file:///Volumes/Workspace_iOS/AGENCIA/05_SDR_Software_Team/08_Project_Manager/MANIFEST.md) | **Pax** | Agile Strategy & Sprint Sequence Manager | Agile strategy, 60-day roadmap orchestrator, sprint sequencing (Sprints 01-10), 5-stream sync coordinator, micro-sprint sizing (1h-4h). |
| [`09_Team_Secretary`](file:///Volumes/Workspace_iOS/AGENCIA/05_SDR_Software_Team/09_Team_Secretary/MANIFEST.md) | **Selena** | Team Secretary & Human Liaison | Human dimension requests, email communication with Fernando (`fernando8cfo@gmail.com`), human-in-the-loop escalation & administrative tracking. |
| [`10_HR_AI_Specialist`](file:///Volumes/Workspace_iOS/AGENCIA/05_SDR_Software_Team/10_HR_AI_Specialist/MANIFEST.md) | **Helena** | AI HR & Capacity Governance Specialist | Team roster control, agent capacity & provisioning, skill gap analysis, agent task performance evaluation & skill upgrades. |

---

## 2. Directory Structure

```
05_SDR_Software_Team/
├── README.md                              # Master overview & team directory guide
├── TEAM_CHARTER.md                        # Team manifest, named roster, invariants & stream map
├── DELIVERABLES_CALENDAR.md               # 60-Day deliverables calendar (Sprints 01 to 10)
├── WORKFLOW_GUIDELINES.md                 # 6-Layer micro-sprint coding workflow & harness rules
├── skills/                                # Consolidated domain skills & technical context
│   ├── 01_revenue_sdr_os_architecture.md  # Core Architecture, 37 ADRs & Invariants
│   ├── 02_ai_langgraph_multiagent.md       # LangChain & LangGraph StateGraph Skill
│   ├── 03_fastapi_tenancy_taskiq.md       # Multi-tenant FastAPI & Taskiq Skill
│   ├── 04_hypermedia_uidesign_zap.md      # Jinja2/HTMX/Alpine White-Label & Zap Copilot Skill
│   ├── 05_pytest_isolation_harness.md    # Multi-tenant Pytest Isolation & Harness Skill
│   ├── 06_supabase_postgresql_vector.md   # Supabase PostgreSQL, Supavisor & pgvector Skill
│   ├── 07_agile_sprint_management.md      # Agile Strategy & Micro-Sprint Management Skill
│   ├── 08_human_liaison_communication.md  # Human Interface & Email Escalation Skill
│   └── 09_ai_hr_performance_skills.md     # AI HR Capacity & Skill Upgrade Skill
├── 01_Enterprise_Architect/               # Workspace for Aria
│   ├── MANIFEST.md
│   ├── SKILLS.md
│   └── TASKS.md
├── 02_AI_Systems_Engineer/                # Workspace for Atlas
│   ├── MANIFEST.md
│   ├── SKILLS.md
│   └── TASKS.md
├── 03_Backend_Async_Engineer/             # Workspace for Bruno
│   ├── MANIFEST.md
│   ├── SKILLS.md
│   └── TASKS.md
├── 04_Frontend_Hypermedia_Engineer/        # Workspace for Fiona
│   ├── MANIFEST.md
│   ├── SKILLS.md
│   └── TASKS.md
├── 05_Security_DevSecOps_Engineer/        # Workspace for Sentinel
│   ├── MANIFEST.md
│   ├── SKILLS.md
│   └── TASKS.md
├── 06_QA_Harness_Director/                # Workspace for Quinn
│   ├── MANIFEST.md
│   ├── SKILLS.md
│   └── TASKS.md
├── 07_Database_Supabase_Specialist/       # Workspace for Silas
│   ├── MANIFEST.md
│   ├── SKILLS.md
│   └── TASKS.md
├── 08_Project_Manager/                    # Workspace for Pax
│   ├── MANIFEST.md
│   ├── SKILLS.md
│   └── TASKS.md
├── 09_Team_Secretary/                     # Workspace for Selena
│   ├── MANIFEST.md
│   ├── SKILLS.md
│   └── TASKS.md
└── 10_HR_AI_Specialist/                   # Workspace for Helena
    ├── MANIFEST.md
    ├── SKILLS.md
    └── TASKS.md
```

---

## 3. Core Project Documentation References

- Architecture Specification: [`00_SDR_architecture`](file:///Volumes/Workspace_iOS/AGENCIA/00_SDR_architecture/README.md)
- White-Label UI Prototype: [`01_SDR_Prototype`](file:///Volumes/Workspace_iOS/AGENCIA/01_SDR_Prototype/README.md)
- Zap Web Copilot Prototype: [`02_ZAP_Prototype`](file:///Volumes/Workspace_iOS/AGENCIA/02_ZAP_Prototype/README.md)
