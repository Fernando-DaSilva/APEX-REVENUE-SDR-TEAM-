# MASTER DELIVERABLES CALENDAR — REVENUE SDR OS

> **Timeline**: 60 Days / 8 Weeks (Hyper-Accelerated Delivery Model)  
> **Execution Strategy**: 5 Parallel Streams, Micro-Sprints (1h to 4h), Sub-Minute CI Harness  
> **Manager**: Pax (`08_Project_Manager`)  

---

## 1. Roadmap Schedule Overview

```
MÊS 1 (SEMANAS 1 A 4 / DIAS 1 A 28) — CORE ENGINE & IA MULTI-AGENTE
Semana 1 [Micro-Sprints 02.1 - 02.8] Lead Brain + Memory Brain + Taskiq Tenant (ADR-030)
Semana 2 [Micro-Sprints 03.1 - 03.8] Conversations + Opportunity Brain + Cadence Engine + Meta 24h HSM (ADR-032)
Semana 3 [Micro-Sprints 04.1 - 04.8] AI Sales Brain + Persistent AsyncPostgresSaver + Z-API WhatsApp Anti-Ban
Semana 4 [Micro-Sprints 05.1 - 05.8] Handoff Humano-IA + Desconstrução HTML Monólito + Google Calendar

MÊS 2 (SEMANAS 5 A 8 / DIAS 29 A 60) — REALTIME, OMNICHANNEL & SCALE
Semana 5 [Micro-Sprints 06.1 - 06.8] Transcrição Whisper + Fix Memory Leak Chart.js Zap + Stream SSE Real-Time
Semana 6 [Micro-Sprints 07.1 - 07.8] Análise Pós-Conversa + Data Warehouse ETL/CDC + Reidratação Cold DW (ADR-031)
Semana 7 [Micro-Sprints 08.1 - 08.8] Engine Omnichannel Completo (Instagram DM, E-mail, Agente de Voz)
Semana 8 [Micro-Sprints 09.1 - 10.8] Automação VPS Single-Tenant + MyraOS Console + Playbooks Verticais & Marketplace
```

---

## 2. Weekly Deliverables Breakdown & Responsible Subagents

### Week 1 (Days 1–7): Lead Brain & Memory Brain Foundation
- **Deliverables**:
  - `app/organizations/` & `app/users/` SQLModel schemas updated for Supabase PostgreSQL.
  - Lead Brain schema & ContextVar tenant persistence in Taskiq queue (`TenantTaskiqMiddleware`).
  - Memory Brain memory extraction pipeline (`Instructor` + Pydantic v2 schemas).
- **Assigned Agents**: Silas (Supabase), Bruno (Backend), Atlas (AI Systems), Quinn (QA).

### Week 2 (Days 8–14): Conversations & Opportunity Brain + Meta 24h HSM
- **Deliverables**:
  - Conversations Brain & stage tracking (`app/conversations/`, `app/opportunities/`).
  - Cadence Engine with Meta 24-Hour Window enforcement & approved HSM templates.
  - Z-API Webhook receiver returning HTTP 202 in $< 50\text{ ms}$.
- **Assigned Agents**: Bruno (Backend), Atlas (AI Systems), Sentinel (Security), Silas (Supabase).

### Week 3 (Days 15–21): AI Sales SDR Brain & LangGraph StateGraph
- **Deliverables**:
  - AI Sales SDR Grafo LangGraph with `AsyncPostgresSaver` checkpointer in Supabase.
  - Hybrid RAG engine (`pgvector` HNSW + `tsvector` BM25 RRF).
  - LLM Router fallback (<900ms primário: Gemini 2.5 -> Sonnet -> GPT-4o-mini).
  - Z-API anti-ban rate limiting (1 msg/3-5s with 2s-6s jitter & `composing` status).
- **Assigned Agents**: Atlas (AI Systems), Silas (Supabase), Bruno (Backend), Quinn (QA).

### Week 4 (Days 22–28): Human Handoff & Hypermedia UI Desconstruction
- **Deliverables**:
  - Human-in-the-Loop Handoff (`interrupt()` trigger in LangGraph state).
  - Desconstruction of `01_SDR_Prototype` into modular Jinja2/HTMX templates.
  - 5 White-Label themes engine (`Obsidian Night`, `Emerald Garden`, `Ocean Breeze`, `Sakura Bloom`, `Amber Warmth`).
  - Google Calendar two-way OAuth2 synchronization.
- **Assigned Agents**: Fiona (Frontend), Atlas (AI Systems), Aria (Architect), Sentinel (Security).

### Week 5 (Days 29–35): Whisper Voice Processing & Zap Copilot Integration
- **Deliverables**:
  - Whisper API transcription worker for inbound audio messages.
  - Zap Web Copilot 3-Column UI integration from `02_ZAP_Prototype`.
  - Fix Chart.js memory leak in DHS Sentiment score gauge widget.
  - Real-time SSE broker (`app/realtime/`) for chat stream updates.
- **Assigned Agents**: Fiona (Frontend), Bruno (Backend), Atlas (AI Systems), Quinn (QA).

### Week 6 (Days 36–42): Post-Conversation Analytics & Cold Data Warehouse
- **Deliverables**:
  - Post-conversation sales coach agent & performance auditor.
  - Cold Data Warehouse ETL/CDC synchronization pipeline.
  - Manager & Revenue Brain analytics dashboards.
- **Assigned Agents**: Atlas (AI Systems), Silas (Supabase), Bruno (Backend), Pax (PM).

### Week 7 (Days 43–49): Omnichannel Engine Expansion
- **Deliverables**:
  - Instagram DM webhook & cadence integration.
  - Email outbound/inbound cadences with tracking.
  - Voice agent WebRTC channel bridge.
- **Assigned Agents**: Bruno (Backend), Atlas (AI Systems), Sentinel (Security).

### Week 8 (Days 50–60): Automated VPS Deployment & Marketplace Release
- **Deliverables**:
  - Automated single-tenant VPS provisioning scripts (`systemd` + update daemon).
  - MyraOS Platform Console integration.
  - Vertical playbooks & marketplace templates.
  - Full end-to-end QA audit with 100% tenant isolation & 0 regressions.
- **Assigned Agents**: Sentinel (Security), Aria (Architect), Quinn (QA), Helena (HR).
