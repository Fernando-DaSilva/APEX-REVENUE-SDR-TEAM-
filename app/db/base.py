"""
Database Engine & Session Management Module
"""
import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres.emqlmsjpltiwoqfbovgi:ng0BpU2dbSJZsVre@aws-0-sa-east-1.pooler.supabase.com:6543/postgres",
)
DATABASE_SYNC_URL = os.getenv(
    "DATABASE_SYNC_URL",
    "postgresql://postgres.emqlmsjpltiwoqfbovgi:ng0BpU2dbSJZsVre@aws-0-sa-east-1.pooler.supabase.com:6543/postgres",
)

# Async SQLAlchemy Engine for FastAPI & Service Layer
async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Sync Engine for Alembic & DDL Migrations
sync_engine = create_engine(
    DATABASE_SYNC_URL,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for providing AsyncSession instances."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
