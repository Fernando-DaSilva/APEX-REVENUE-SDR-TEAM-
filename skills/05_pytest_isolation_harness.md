# SHARED SKILL: Pytest Multi-Tenant Isolation & Sub-Minute Harness

## Core Principles

- **Test Isolation**: Every test fixture provisions an isolated schema/database context with distinct `organization_id`.
- **Cross-Tenant Assertions**: Tests explicitly verify that Tenant A cannot read, mutate, or leak Tenant B's data (returning HTTP 404 Not Found).
- **Harness Coverage Target**: `pytest` coverage $> 90\%$ enforced via `--cov-fail-under=90`.
- **Execution Speed**: Full harness executes sub-minute ($< 60\text{s}$). Includes `pytest`, `ruff check`, `ruff format`, and Alembic migration round-trip (`upgrade head -> downgrade -1 -> upgrade head`).
