# SHARED SKILL: Supabase Managed PostgreSQL & Hybrid Vector RAG

## Core Principles

- **Database Engine**: Supabase Managed PostgreSQL 16+ using Supavisor connection pooler.
- **Hybrid RAG Engine**:
  - `pgvector` HNSW index for dense vector similarity ($< 15\text{ ms}$).
  - `tsvector` BM25 full-text search for sparse keyword matching.
  - Reciprocal Rank Fusion (RRF) algorithm combining vector and keyword search scores.
- **Row Level Security (RLS)**: PostgreSQL RLS policies enabled on all organization domain tables as a database-level safety net.
- **Alembic Migrations**: PostgreSQL DDL migrations using Alembic batch alter table format.
