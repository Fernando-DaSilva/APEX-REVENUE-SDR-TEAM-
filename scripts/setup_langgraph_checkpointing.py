"""
LangGraph AsyncPostgresSaver Checkpointer Setup Script

Provision persistent state tables directly in Supabase Managed PostgreSQL
for stateful AI Sales Brain conversation graphs.
"""
import asyncio
import os
import sys
from dotenv import load_dotenv
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set in environment.")
    sys.exit(1)

# Convert SQLAlchemy asyncpg URL to standard PostgreSQL connection string for psycopg3
# e.g., postgresql+asyncpg://user:pass@host:port/db -> postgresql://user:pass@host:port/db
POSTGRES_CONN_STRING = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")


async def main():
    print(f"Connecting to Supabase PostgreSQL for LangGraph Checkpointer setup...")
    print(f"Connection string: {POSTGRES_CONN_STRING.split('@')[-1]}")

    async with AsyncConnectionPool(conninfo=POSTGRES_CONN_STRING, max_size=5, kwargs={"autocommit": True}) as pool:
        checkpointer = AsyncPostgresSaver(pool)
        print("Provisioning LangGraph checkpointer tables (checkpoints, checkpoint_blobs, checkpoint_writes, checkpoint_migrations)...")
        await checkpointer.setup()
        print("SUCCESS: LangGraph persistent checkpointer tables created and verified successfully in Supabase PostgreSQL!")


if __name__ == "__main__":
    asyncio.run(main())
