"""001 Initial Core Multi-Tenant Tables

Revision ID: 001_initial_tables
Revises: 
Create Date: 2026-08-11 15:45:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel

revision: str = '001_initial_tables'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Organizations
    op.create_table(
        'organizations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('domain', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_organizations_domain'), 'organizations', ['domain'], unique=False)
    op.create_index(op.f('ix_organizations_name'), 'organizations', ['name'], unique=False)
    op.create_index(op.f('ix_organizations_slug'), 'organizations', ['slug'], unique=True)

    # 2. Users
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_organization_id'), 'users', ['organization_id'], unique=False)
    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)

    # 3. Leads
    op.create_table(
        'leads',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('company_name', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('metadata_json', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leads_company_name'), 'leads', ['company_name'], unique=False)
    op.create_index(op.f('ix_leads_email'), 'leads', ['email'], unique=False)
    op.create_index(op.f('ix_leads_name'), 'leads', ['name'], unique=False)
    op.create_index(op.f('ix_leads_organization_id'), 'leads', ['organization_id'], unique=False)
    op.create_index(op.f('ix_leads_phone'), 'leads', ['phone'], unique=False)
    op.create_index(op.f('ix_leads_score'), 'leads', ['score'], unique=False)
    op.create_index(op.f('ix_leads_status'), 'leads', ['status'], unique=False)

    # 4. Conversations
    op.create_table(
        'conversations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('lead_id', sa.UUID(), nullable=False),
        sa.Column('channel', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('thread_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversations_channel'), 'conversations', ['channel'], unique=False)
    op.create_index(op.f('ix_conversations_lead_id'), 'conversations', ['lead_id'], unique=False)
    op.create_index(op.f('ix_conversations_organization_id'), 'conversations', ['organization_id'], unique=False)
    op.create_index(op.f('ix_conversations_status'), 'conversations', ['status'], unique=False)
    op.create_index(op.f('ix_conversations_thread_id'), 'conversations', ['thread_id'], unique=False)

    # 5. Opportunities
    op.create_table(
        'opportunities',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('lead_id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('stage', sa.String(), nullable=False),
        sa.Column('closed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_opportunities_lead_id'), 'opportunities', ['lead_id'], unique=False)
    op.create_index(op.f('ix_opportunities_organization_id'), 'opportunities', ['organization_id'], unique=False)
    op.create_index(op.f('ix_opportunities_stage'), 'opportunities', ['stage'], unique=False)
    op.create_index(op.f('ix_opportunities_title'), 'opportunities', ['title'], unique=False)


def downgrade() -> None:
    op.drop_table('opportunities')
    op.drop_table('conversations')
    op.drop_table('leads')
    op.drop_table('users')
    op.drop_table('organizations')
