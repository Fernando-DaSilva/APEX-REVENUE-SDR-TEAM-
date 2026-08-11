# SHARED SKILL: LangChain & LangGraph Multi-Agent Orchestration

## Core Principles

- **Framework**: `langchain-core` + `langgraph` StateGraph.
- **State Checkpointing**: `AsyncPostgresSaver` backed by Supabase Managed PostgreSQL. `MemorySaver` is strictly forbidden in production.
- **Thread Isolation**: `thread_id` formatted as `f"{organization_id}:{lead_id}"`.
- **Structured Output**: Extractor chains use `Instructor` + Pydantic v2 schemas.
- **LLM Fallback Router**:
  - Primary LLM: Gemini 2.5 (Timeout: 900ms).
  - Secondary Fallback: Claude 3.5 Sonnet.
  - Tertiary Fallback: GPT-4o-mini.
- **Human-in-the-Loop**: Escalation triggered via `interrupt()` in LangGraph state node when confidence is low or human takeover is requested.
