"""
Cadence & Automation Models — Workflows, Cadence Steps, and Lead Enrollments
"""
from datetime import datetime
from typing import Any, Dict, Optional
import uuid
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Cadence(SQLModel, table=True):
    __tablename__ = "cadences"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    name: str = Field(index=True, nullable=False)
    description: Optional[str] = Field(default=None)
    channel: str = Field(default="Zap", index=True, nullable=False)
    is_active: bool = Field(default=True, index=True, nullable=False)
    agent_id: Optional[uuid.UUID] = Field(default=None, foreign_key="ai_agents.id", index=True)
    target_audience: Optional[str] = Field(default=None)
    metrics_json: Dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSON, nullable=False)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class CadenceStep(SQLModel, table=True):
    __tablename__ = "cadence_steps"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    cadence_id: uuid.UUID = Field(
        foreign_key="cadences.id", index=True, nullable=False
    )
    step_order: int = Field(default=1, nullable=False)
    step_type: str = Field(nullable=False) # ai_message, delay, condition_bant, email, voice_call, human_task
    title: str = Field(nullable=False)
    icon: str = Field(default="💬")
    delay_duration: Optional[str] = Field(default=None) # e.g. "2 horas", "Imediato"
    condition_expr: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class LeadCadence(SQLModel, table=True):
    __tablename__ = "lead_cadences"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    lead_id: uuid.UUID = Field(
        foreign_key="leads.id", index=True, nullable=False
    )
    cadence_id: uuid.UUID = Field(
        foreign_key="cadences.id", index=True, nullable=False
    )
    current_step_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="cadence_steps.id", index=True
    )
    status: str = Field(default="active", index=True, nullable=False) # active, paused, completed, disqualified
    enrolled_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    last_executed_at: Optional[datetime] = Field(default=None)
