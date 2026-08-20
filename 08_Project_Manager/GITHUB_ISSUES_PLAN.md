# GITHUB ISSUES POPULATION PLAN — Pax (`08_Project_Manager`)

> **Directive Source**: User (Fernando) via Selena (`09_Team_Secretary`)  
> **Target Repository**: [APEX-REVENUE-SDR-TEAM- GitHub Issues](https://github.com/Fernando-DaSilva/APEX-REVENUE-SDR-TEAM-/issues)  
> **Status**: QUEUED (To be populated at Pax's strategic discretion)  

---

## 1. Milestones Structure

| Milestone Name | Timeframe | Micro-Sprints Scope | Focus Area |
|---|---|---|---|
| `Milestone: Week 1` | Days 1–7 | Micro-Sprints 02.1 – 02.8 | Lead Brain & Memory Brain Foundation |
| `Milestone: Week 2` | Days 8–14 | Micro-Sprints 03.1 – 03.8 | Conversations & Opportunity Brain + Meta 24h HSM |
| `Milestone: Week 3` | Days 15–21 | Micro-Sprints 04.1 – 04.8 | AI Sales SDR Brain & LangGraph StateGraph |
| `Milestone: Week 4` | Days 22–28 | Micro-Sprints 05.1 – 05.8 | Human Handoff & Hypermedia UI Desconstruction |
| `Milestone: Week 5` | Days 29–35 | Micro-Sprints 06.1 – 06.8 | Whisper Voice Processing & Zap Copilot |
| `Milestone: Week 6` | Days 36–42 | Micro-Sprints 07.1 – 07.8 | Post-Conversation Analytics & Cold Data Warehouse |
| `Milestone: Week 7` | Days 43–49 | Micro-Sprints 08.1 – 08.8 | Omnichannel Engine Expansion |
| `Milestone: Week 8` | Days 50–60 | Micro-Sprints 09.1 – 10.8 | Automated VPS Deployment & Marketplace Release |

---

## 2. Stream & Subagent Labels Taxonomy

| Label Name | Assigned Lead Subagent | Domain Scope |
|---|---|---|
| `stream:architecture` | Aria (`01_Enterprise_Architect`) | Modular System Design, ADR Governance & Monolith Desconstruction |
| `stream:ai-systems` | Atlas (`02_AI_Systems_Engineer`) | LangGraph StateGraph, Memory Extraction, Hybrid RAG & Whisper |
| `stream:backend` | Bruno (`03_Backend_Async_Engineer`) | Taskiq Workers, Z-API Webhooks, FastHTTP Routing & Cadence Engine |
| `stream:frontend` | Fiona (`04_Frontend_Hypermedia_Engineer`) | Jinja2 + HTMX Templates, White-Label Themes & Zap Copilot |
| `stream:security` | Sentinel (`05_Security_DevSecOps_Engineer`) | Zero-Trust RLS, Token Encryption, Rate Limiting & Auth |
| `stream:qa` | Quinn (`06_QA_Harness_Director`) | Sub-Minute CI Harness, Cross-Tenant Isolation Tests & Benchmark Audits |
| `stream:database` | Silas (`07_Database_Supabase_Specialist`) | SQLModel Schemas, Alembic Migrations, Supabase RLS & Cold DW |
| `stream:pm` | Pax (`08_Project_Manager`) | Sprint Sequencing, Micro-Sprint Sizing & Delivery Gatekeeping |
| `stream:secretary` | Selena (`09_Team_Secretary`) | Human Escalation Protocol, Approval Registry & Milestone Digests |
| `stream:hr` | Helena (`10_HR_AI_Specialist`) | Subagent Capability Reviews, Performance Audits & Skill Upgrades |

---

## 3. Micro-Sprint Issues Breakdown (64 Micro-Sprints)

Each issue will follow standard title formatting:
`[Micro-Sprint XX.Y] <Title>` with appropriate milestone, stream label, and assignee subagent.

### Week 1 (Days 1–7): Lead Brain & Memory Brain Foundation
- `[Micro-Sprint 02.1] Update SQLModel Schemas for Supabase PostgreSQL` (`stream:database`, `stream:backend`)
- `[Micro-Sprint 02.2] ContextVar Tenant Persistence in Taskiq Middleware` (`stream:backend`, `stream:security`)
- `[Micro-Sprint 02.3] Lead Brain Schema & Multi-Tenant Field Enforcement` (`stream:database`, `stream:architecture`)
- `[Micro-Sprint 02.4] Memory Brain Pipeline using Instructor + Pydantic v2` (`stream:ai-systems`)
- `[Micro-Sprint 02.5] User and Organization Account Provisions in Supabase` (`stream:database`)
- `[Micro-Sprint 02.6] Sub-Minute Harness Test Coverage for Lead/Memory Brain` (`stream:qa`)
- `[Micro-Sprint 02.7] Zero-Trust RLS Policy Audit on Lead/Memory Tables` (`stream:security`)
- `[Micro-Sprint 02.8] Week 1 Integration Benchmark & Tenant Leakage Test` (`stream:qa`, `stream:pm`)

---

## 4. Execution Command Reference (`gh` CLI)

When Pax initiates issue population:
```bash
# Example gh issue creation pattern
gh issue create \
  --repo "Fernando-DaSilva/APEX-REVENUE-SDR-TEAM-" \
  --title "[Micro-Sprint 02.1] Update SQLModel Schemas for Supabase PostgreSQL" \
  --body "Deliverable: Update app/organizations/ & app/users/ SQLModel schemas for live Supabase PostgreSQL compliance." \
  --label "stream:database,stream:backend" \
  --milestone "Week 1: Lead & Memory Brain Foundation"
```
