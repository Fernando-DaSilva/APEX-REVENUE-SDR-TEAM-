"""002 Enable Row Level Security (RLS) Policies

Revision ID: 002_enable_rls_policies
Revises: 001_initial_tables
Create Date: 2026-08-11 15:46:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002_enable_rls_policies'
down_revision: Union[str, None] = '001_initial_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TENANT_TABLES = ['users', 'leads', 'conversations', 'opportunities']


def upgrade() -> None:
    for table in TENANT_TABLES:
        # Enable engine-level Row Level Security
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;")
        
        # Drop existing policy if present (idempotent)
        op.execute(f"DROP POLICY IF EXISTS tenant_isolation_policy ON {table};")
        
        # Create zero-trust tenant isolation policy based on session ContextVar / setting
        op.execute(f"""
            CREATE POLICY tenant_isolation_policy ON {table}
            FOR ALL
            USING (
                organization_id = NULLIF(current_setting('app.current_organization_id', true), '')::uuid
            )
            WITH CHECK (
                organization_id = NULLIF(current_setting('app.current_organization_id', true), '')::uuid
            );
        """)


def downgrade() -> None:
    for table in TENANT_TABLES:
        op.execute(f"DROP POLICY IF EXISTS tenant_isolation_policy ON {table};")
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;")
