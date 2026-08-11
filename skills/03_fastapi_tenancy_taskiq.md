# SHARED SKILL: FastAPI Multi-Tenancy & Taskiq Async Queue

## Core Principles

- **FastAPI Layering**: Route handlers in `app/*/api.py` remain thin. Business logic resides in `app/*/service.py`.
- **Tenant ContextVar**: Tenant resolution middleware sets ContextVar `current_organization`.
- **Taskiq Background Queue**: Webhooks return HTTP 202 in $< 50\text{ ms}$. Tasks are sent to Taskiq broker wrapped in `TenantTaskiqMiddleware` to serialize `organization_id` in `pre_send` and rehydrate it in `pre_execute`.
- **SSE Realtime Streaming**: Real-time event streaming implemented via `app/realtime/broker.py` delivering SSE events to hypermedia clients (HTMX).
