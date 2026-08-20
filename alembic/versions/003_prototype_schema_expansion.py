"""003 Prototype Schema Expansion (01_SDR_Prototype & 02_ZAP_Prototype Gap Resolution)

Revision ID: 003_prototype_schema_expansion
Revises: 002_enable_rls_policies
Create Date: 2026-08-11 16:20:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '003_prototype_schema_expansion'
down_revision: Union[str, None] = '002_enable_rls_policies'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

NEW_TENANT_TABLES = [
    'messages',
    'dhs_logs',
    'copilot_suggestions',
    'ai_agents',
    'cadences',
    'lead_cadences',
    'knowledge_documents',
    'knowledge_chunks',
    'lead_memories',
    'guardrails',
    'brain_audit_logs',
    'integrations',
    'webhook_configs',
    'webhook_events',
    'financial_contacts',
    'invoices',
    'payment_methods',
]


def upgrade() -> None:
    # 1. Expand `organizations`
    op.add_column('organizations', sa.Column('tax_id', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('primary_color', sa.String(), server_default='#EC4899', nullable=False))
    op.add_column('organizations', sa.Column('secondary_color', sa.String(), server_default='#7E22CE', nullable=False))
    op.add_column('organizations', sa.Column('logo_url', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('dark_logo_url', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('favicon_url', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('theme_preset', sa.String(), server_default='obsidian_night', nullable=False))
    op.add_column('organizations', sa.Column('theme_tokens_json', sa.JSON(), server_default='{}', nullable=False))
    op.add_column('organizations', sa.Column('remove_branding', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('organizations', sa.Column('footer_text', sa.String(), nullable=True))
    op.add_column('organizations', sa.Column('timezone', sa.String(), server_default='America/Sao_Paulo', nullable=False))
    op.add_column('organizations', sa.Column('language', sa.String(), server_default='pt-BR', nullable=False))
    op.add_column('organizations', sa.Column('plan_name', sa.String(), server_default='Enterprise Growth', nullable=False))
    op.add_column('organizations', sa.Column('billing_cycle', sa.String(), server_default='monthly', nullable=False))
    op.add_column('organizations', sa.Column('plan_status', sa.String(), server_default='active', nullable=False))

    op.create_index(op.f('ix_organizations_tax_id'), 'organizations', ['tax_id'], unique=False)
    op.create_index(op.f('ix_organizations_theme_preset'), 'organizations', ['theme_preset'], unique=False)
    op.create_index(op.f('ix_organizations_plan_name'), 'organizations', ['plan_name'], unique=False)

    # 2. Expand `users`
    op.add_column('users', sa.Column('avatar_url', sa.String(), nullable=True))
    op.add_column('users', sa.Column('department', sa.String(), nullable=True))
    op.add_column('users', sa.Column('workload_active_leads', sa.Integer(), server_default='0', nullable=False))
    op.add_column('users', sa.Column('status', sa.String(), server_default='online', nullable=False))
    op.add_column('users', sa.Column('last_access_at', sa.DateTime(), nullable=True))

    op.create_index(op.f('ix_users_department'), 'users', ['department'], unique=False)
    op.create_index(op.f('ix_users_status'), 'users', ['status'], unique=False)

    # 3. Expand `leads`
    op.add_column('leads', sa.Column('avatar_url', sa.String(), nullable=True))
    op.add_column('leads', sa.Column('initials', sa.String(), nullable=True))
    op.add_column('leads', sa.Column('role_title', sa.String(), nullable=True))
    op.add_column('leads', sa.Column('channel', sa.String(), server_default='zap', nullable=False))
    op.add_column('leads', sa.Column('dhs_score', sa.Integer(), server_default='50', nullable=False))
    op.add_column('leads', sa.Column('dhs_trend', sa.String(), server_default='stable', nullable=False))
    op.add_column('leads', sa.Column('dhs_variation', sa.String(), nullable=True))
    op.add_column('leads', sa.Column('bant_score', sa.Integer(), server_default='0', nullable=False))
    op.add_column('leads', sa.Column('budget_amount', sa.Float(), nullable=True))
    op.add_column('leads', sa.Column('assigned_user_id', sa.UUID(), nullable=True))
    op.add_column('leads', sa.Column('assigned_agent_id', sa.UUID(), nullable=True))
    op.add_column('leads', sa.Column('ai_mode', sa.String(), server_default='copiloto', nullable=False))
    op.add_column('leads', sa.Column('unread_count', sa.Integer(), server_default='0', nullable=False))
    op.add_column('leads', sa.Column('last_message_at', sa.DateTime(), nullable=True))

    op.create_foreign_key('fk_leads_assigned_user', 'leads', 'users', ['assigned_user_id'], ['id'], ondelete='SET NULL')
    op.create_index(op.f('ix_leads_channel'), 'leads', ['channel'], unique=False)
    op.create_index(op.f('ix_leads_dhs_score'), 'leads', ['dhs_score'], unique=False)
    op.create_index(op.f('ix_leads_dhs_trend'), 'leads', ['dhs_trend'], unique=False)
    op.create_index(op.f('ix_leads_bant_score'), 'leads', ['bant_score'], unique=False)
    op.create_index(op.f('ix_leads_assigned_user_id'), 'leads', ['assigned_user_id'], unique=False)
    op.create_index(op.f('ix_leads_assigned_agent_id'), 'leads', ['assigned_agent_id'], unique=False)
    op.create_index(op.f('ix_leads_ai_mode'), 'leads', ['ai_mode'], unique=False)

    # 4. Expand `conversations`
    op.add_column('conversations', sa.Column('sdr_agent_name', sa.String(), nullable=True))
    op.add_column('conversations', sa.Column('ai_mode', sa.String(), server_default='autonomo', nullable=False))
    op.add_column('conversations', sa.Column('bant_score', sa.String(), nullable=True))
    op.add_column('conversations', sa.Column('budget_str', sa.String(), nullable=True))
    op.add_column('conversations', sa.Column('cadence_name', sa.String(), nullable=True))
    op.add_column('conversations', sa.Column('funnel_stage', sa.String(), nullable=True))
    op.add_column('conversations', sa.Column('unread_count', sa.Integer(), server_default='0', nullable=False))
    op.add_column('conversations', sa.Column('last_message_text', sa.String(), nullable=True))
    op.add_column('conversations', sa.Column('last_message_at', sa.DateTime(), nullable=True))

    op.create_index(op.f('ix_conversations_sdr_agent_name'), 'conversations', ['sdr_agent_name'], unique=False)
    op.create_index(op.f('ix_conversations_ai_mode'), 'conversations', ['ai_mode'], unique=False)
    op.create_index(op.f('ix_conversations_cadence_name'), 'conversations', ['cadence_name'], unique=False)
    op.create_index(op.f('ix_conversations_funnel_stage'), 'conversations', ['funnel_stage'], unique=False)

    # 5. Expand `opportunities`
    op.add_column('opportunities', sa.Column('mrr_estimated', sa.Float(), server_default='0.0', nullable=False))
    op.add_column('opportunities', sa.Column('setup_fee', sa.Float(), server_default='0.0', nullable=False))
    op.add_column('opportunities', sa.Column('probability_percent', sa.Integer(), server_default='50', nullable=False))
    op.add_column('opportunities', sa.Column('weighted_value', sa.Float(), server_default='0.0', nullable=False))
    op.add_column('opportunities', sa.Column('expected_close_date', sa.DateTime(), nullable=True))

    op.create_index(op.f('ix_opportunities_expected_close_date'), 'opportunities', ['expected_close_date'], unique=False)

    # 6. Create `messages` Table
    op.create_table(
        'messages',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('conversation_id', sa.UUID(), nullable=False),
        sa.Column('sender_type', sa.String(), server_default='lead', nullable=False),
        sa.Column('sender_name', sa.String(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('is_ai', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('is_human_operator', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('synced', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('source_doc', sa.String(), nullable=True),
        sa.Column('metadata_json', sa.JSON(), server_default='{}', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_organization_id'), 'messages', ['organization_id'], unique=False)
    op.create_index(op.f('ix_messages_conversation_id'), 'messages', ['conversation_id'], unique=False)
    op.create_index(op.f('ix_messages_sender_type'), 'messages', ['sender_type'], unique=False)
    op.create_index(op.f('ix_messages_is_ai'), 'messages', ['is_ai'], unique=False)

    # 7. Create `dhs_logs` Table
    op.create_table(
        'dhs_logs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('lead_id', sa.UUID(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('trend', sa.String(), server_default='stable', nullable=False),
        sa.Column('variation', sa.String(), nullable=True),
        sa.Column('reason', sa.String(), nullable=True),
        sa.Column('recorded_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dhs_logs_organization_id'), 'dhs_logs', ['organization_id'], unique=False)
    op.create_index(op.f('ix_dhs_logs_lead_id'), 'dhs_logs', ['lead_id'], unique=False)
    op.create_index(op.f('ix_dhs_logs_score'), 'dhs_logs', ['score'], unique=False)

    # 8. Create `copilot_suggestions` Table
    op.create_table(
        'copilot_suggestions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('lead_id', sa.UUID(), nullable=False),
        sa.Column('conversation_id', sa.UUID(), nullable=True),
        sa.Column('suggestion_type', sa.String(), server_default='qa', nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('confidence', sa.Integer(), server_default='90', nullable=False),
        sa.Column('source_doc', sa.String(), nullable=True),
        sa.Column('status', sa.String(), server_default='suggested', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_copilot_suggestions_organization_id'), 'copilot_suggestions', ['organization_id'], unique=False)
    op.create_index(op.f('ix_copilot_suggestions_lead_id'), 'copilot_suggestions', ['lead_id'], unique=False)

    # 9. Create `ai_agents` Table
    op.create_table(
        'ai_agents',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('avatar', sa.String(), server_default='🤖', nullable=False),
        sa.Column('llm_model', sa.String(), server_default='Gemini 1.5 Pro', nullable=False),
        sa.Column('autonomy_level', sa.Integer(), server_default='100', nullable=False),
        sa.Column('autonomy_mode', sa.String(), server_default='autonomo', nullable=False),
        sa.Column('tone_of_voice', sa.String(), server_default='Consultivo & Empático', nullable=False),
        sa.Column('channels_json', sa.JSON(), server_default='[]', nullable=False),
        sa.Column('max_simultaneous', sa.Integer(), server_default='50', nullable=False),
        sa.Column('avg_response_time', sa.String(), server_default='3.2s', nullable=False),
        sa.Column('system_prompt', sa.Text(), nullable=False),
        sa.Column('guardrails_json', sa.JSON(), server_default='{}', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_agents_organization_id'), 'ai_agents', ['organization_id'], unique=False)
    op.create_index(op.f('ix_ai_agents_name'), 'ai_agents', ['name'], unique=False)

    # 10. Create `cadences`, `cadence_steps`, `lead_cadences` Tables
    op.create_table(
        'cadences',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('channel', sa.String(), server_default='Zap', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('agent_id', sa.UUID(), nullable=True),
        sa.Column('target_audience', sa.String(), nullable=True),
        sa.Column('metrics_json', sa.JSON(), server_default='{}', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['agent_id'], ['ai_agents.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cadences_organization_id'), 'cadences', ['organization_id'], unique=False)
    op.create_index(op.f('ix_cadences_name'), 'cadences', ['name'], unique=False)

    op.create_table(
        'cadence_steps',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('cadence_id', sa.UUID(), nullable=False),
        sa.Column('step_order', sa.Integer(), server_default='1', nullable=False),
        sa.Column('step_type', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('icon', sa.String(), server_default='💬', nullable=False),
        sa.Column('delay_duration', sa.String(), nullable=True),
        sa.Column('condition_expr', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['cadence_id'], ['cadences.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cadence_steps_cadence_id'), 'cadence_steps', ['cadence_id'], unique=False)

    op.create_table(
        'lead_cadences',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('lead_id', sa.UUID(), nullable=False),
        sa.Column('cadence_id', sa.UUID(), nullable=False),
        sa.Column('current_step_id', sa.UUID(), nullable=True),
        sa.Column('status', sa.String(), server_default='active', nullable=False),
        sa.Column('enrolled_at', sa.DateTime(), nullable=False),
        sa.Column('last_executed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['cadence_id'], ['cadences.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['current_step_id'], ['cadence_steps.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lead_cadences_organization_id'), 'lead_cadences', ['organization_id'], unique=False)
    op.create_index(op.f('ix_lead_cadences_lead_id'), 'lead_cadences', ['lead_id'], unique=False)

    # 11. Create `knowledge_documents`, `knowledge_chunks`, `lead_memories` Tables
    op.create_table(
        'knowledge_documents',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('file_type', sa.String(), server_default='PDF', nullable=False),
        sa.Column('size_bytes', sa.Integer(), server_default='0', nullable=False),
        sa.Column('chunks_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('status', sa.String(), server_default='Indexed', nullable=False),
        sa.Column('last_reindexed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_knowledge_documents_organization_id'), 'knowledge_documents', ['organization_id'], unique=False)
    op.create_index(op.f('ix_knowledge_documents_name'), 'knowledge_documents', ['name'], unique=False)

    op.create_table(
        'knowledge_chunks',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('document_id', sa.UUID(), nullable=False),
        sa.Column('chunk_index', sa.Integer(), server_default='0', nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('embedding_vector_json', sa.JSON(), server_default='[]', nullable=False),
        sa.Column('token_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['document_id'], ['knowledge_documents.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_knowledge_chunks_organization_id'), 'knowledge_chunks', ['organization_id'], unique=False)
    op.create_index(op.f('ix_knowledge_chunks_document_id'), 'knowledge_chunks', ['document_id'], unique=False)

    op.create_table(
        'lead_memories',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('lead_id', sa.UUID(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('memory_key', sa.String(), nullable=False),
        sa.Column('memory_value', sa.Text(), nullable=False),
        sa.Column('confidence_score', sa.Integer(), server_default='95', nullable=False),
        sa.Column('source', sa.String(), server_default='Zap IA', nullable=False),
        sa.Column('verified', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lead_memories_organization_id'), 'lead_memories', ['organization_id'], unique=False)
    op.create_index(op.f('ix_lead_memories_lead_id'), 'lead_memories', ['lead_id'], unique=False)

    # 12. Create `guardrails`, `brain_audit_logs`, `integrations`, `webhook_configs`, `webhook_events`, `financial_contacts`, `invoices`, `payment_methods` Tables
    op.create_table(
        'guardrails',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('lgpd_strict', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('block_financial_promises', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('business_hours_only', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('max_discount_percent', sa.Integer(), server_default='15', nullable=False),
        sa.Column('prohibited_words_json', sa.JSON(), server_default='[]', nullable=False),
        sa.Column('handoff_triggers_json', sa.JSON(), server_default='[]', nullable=False),
        sa.Column('objection_matrix_json', sa.JSON(), server_default='[]', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_guardrails_organization_id'), 'guardrails', ['organization_id'], unique=False)

    op.create_table(
        'brain_audit_logs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('lead_id', sa.UUID(), nullable=False),
        sa.Column('conversation_id', sa.UUID(), nullable=True),
        sa.Column('channel', sa.String(), server_default='Zap', nullable=False),
        sa.Column('intent', sa.String(), nullable=False),
        sa.Column('confidence', sa.Integer(), server_default='95', nullable=False),
        sa.Column('guardrail_status', sa.String(), server_default='approved', nullable=False),
        sa.Column('input_text', sa.Text(), nullable=False),
        sa.Column('rag_context', sa.Text(), nullable=True),
        sa.Column('lead_memories_injected', sa.Text(), nullable=True),
        sa.Column('generated_response', sa.Text(), nullable=False),
        sa.Column('guardrail_check', sa.Text(), nullable=True),
        sa.Column('feedback', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_brain_audit_logs_organization_id'), 'brain_audit_logs', ['organization_id'], unique=False)
    op.create_index(op.f('ix_brain_audit_logs_lead_id'), 'brain_audit_logs', ['lead_id'], unique=False)

    op.create_table(
        'integrations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('provider', sa.String(), nullable=False),
        sa.Column('status', sa.String(), server_default='connected', nullable=False),
        sa.Column('credentials_json', sa.JSON(), server_default='{}', nullable=False),
        sa.Column('config_json', sa.JSON(), server_default='{}', nullable=False),
        sa.Column('last_synced_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_integrations_organization_id'), 'integrations', ['organization_id'], unique=False)
    op.create_index(op.f('ix_integrations_provider'), 'integrations', ['provider'], unique=False)

    op.create_table(
        'webhook_configs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('endpoint_url', sa.String(), nullable=False),
        sa.Column('secret_token', sa.String(), nullable=False),
        sa.Column('events_json', sa.JSON(), server_default='[]', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_webhook_configs_organization_id'), 'webhook_configs', ['organization_id'], unique=False)

    op.create_table(
        'webhook_events',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('webhook_id', sa.UUID(), nullable=False),
        sa.Column('origin', sa.String(), nullable=False),
        sa.Column('payload_json', sa.JSON(), server_default='{}', nullable=False),
        sa.Column('status_code', sa.Integer(), server_default='200', nullable=False),
        sa.Column('response_body', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['webhook_id'], ['webhook_configs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_webhook_events_organization_id'), 'webhook_events', ['organization_id'], unique=False)
    op.create_index(op.f('ix_webhook_events_webhook_id'), 'webhook_events', ['webhook_id'], unique=False)

    op.create_table(
        'financial_contacts',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('department', sa.String(), server_default='Financeiro', nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('extension', sa.String(), nullable=True),
        sa.Column('zap', sa.String(), nullable=True),
        sa.Column('is_primary', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('status', sa.String(), server_default='Ativo', nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('history_logs_json', sa.JSON(), server_default='[]', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_financial_contacts_organization_id'), 'financial_contacts', ['organization_id'], unique=False)
    op.create_index(op.f('ix_financial_contacts_name'), 'financial_contacts', ['name'], unique=False)

    op.create_table(
        'invoices',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('invoice_number', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('amount', sa.Float(), server_default='0.0', nullable=False),
        sa.Column('payment_method_type', sa.String(), server_default='pix', nullable=False),
        sa.Column('status', sa.String(), server_default='Paga', nullable=False),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('paid_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_invoices_organization_id'), 'invoices', ['organization_id'], unique=False)
    op.create_index(op.f('ix_invoices_invoice_number'), 'invoices', ['invoice_number'], unique=False)

    op.create_table(
        'payment_methods',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('method_type', sa.String(), server_default='pix', nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('subtitle', sa.String(), nullable=True),
        sa.Column('is_primary', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('details_json', sa.JSON(), server_default='{}', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payment_methods_organization_id'), 'payment_methods', ['organization_id'], unique=False)

    # 13. Enable RLS Policies on all new multi-tenant tables
    for table in NEW_TENANT_TABLES:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;")
        op.execute(f"DROP POLICY IF EXISTS tenant_isolation_policy ON {table};")
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
    # Drop RLS policies & new tables
    for table in NEW_TENANT_TABLES:
        op.execute(f"DROP POLICY IF EXISTS tenant_isolation_policy ON {table};")
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;")

    op.drop_table('payment_methods')
    op.drop_table('invoices')
    op.drop_table('financial_contacts')
    op.drop_table('webhook_events')
    op.drop_table('webhook_configs')
    op.drop_table('integrations')
    op.drop_table('brain_audit_logs')
    op.drop_table('guardrails')
    op.drop_table('lead_memories')
    op.drop_table('knowledge_chunks')
    op.drop_table('knowledge_documents')
    op.drop_table('lead_cadences')
    op.drop_table('cadence_steps')
    op.drop_table('cadences')
    op.drop_table('ai_agents')
    op.drop_table('copilot_suggestions')
    op.drop_table('dhs_logs')
    op.drop_table('messages')

    # Remove expanded columns from core tables
    op.drop_column('opportunities', 'expected_close_date')
    op.drop_column('opportunities', 'weighted_value')
    op.drop_column('opportunities', 'probability_percent')
    op.drop_column('opportunities', 'setup_fee')
    op.drop_column('opportunities', 'mrr_estimated')

    op.drop_column('conversations', 'last_message_at')
    op.drop_column('conversations', 'last_message_text')
    op.drop_column('conversations', 'unread_count')
    op.drop_column('conversations', 'funnel_stage')
    op.drop_column('conversations', 'cadence_name')
    op.drop_column('conversations', 'budget_str')
    op.drop_column('conversations', 'bant_score')
    op.drop_column('conversations', 'ai_mode')
    op.drop_column('conversations', 'sdr_agent_name')

    op.drop_column('leads', 'last_message_at')
    op.drop_column('leads', 'unread_count')
    op.drop_column('leads', 'ai_mode')
    op.drop_column('leads', 'assigned_agent_id')
    op.drop_column('leads', 'assigned_user_id')
    op.drop_column('leads', 'budget_amount')
    op.drop_column('leads', 'bant_score')
    op.drop_column('leads', 'dhs_variation')
    op.drop_column('leads', 'dhs_trend')
    op.drop_column('leads', 'dhs_score')
    op.drop_column('leads', 'channel')
    op.drop_column('leads', 'role_title')
    op.drop_column('leads', 'initials')
    op.drop_column('leads', 'avatar_url')

    op.drop_column('users', 'last_access_at')
    op.drop_column('users', 'status')
    op.drop_column('users', 'workload_active_leads')
    op.drop_column('users', 'department')
    op.drop_column('users', 'avatar_url')

    op.drop_column('organizations', 'plan_status')
    op.drop_column('organizations', 'billing_cycle')
    op.drop_column('organizations', 'plan_name')
    op.drop_column('organizations', 'language')
    op.drop_column('organizations', 'timezone')
    op.drop_column('organizations', 'footer_text')
    op.drop_column('organizations', 'remove_branding')
    op.drop_column('organizations', 'theme_tokens_json')
    op.drop_column('organizations', 'theme_preset')
    op.drop_column('organizations', 'favicon_url')
    op.drop_column('organizations', 'dark_logo_url')
    op.drop_column('organizations', 'logo_url')
    op.drop_column('organizations', 'secondary_color')
    op.drop_column('organizations', 'primary_color')
    op.drop_column('organizations', 'tax_id')
