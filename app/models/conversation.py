"""
Conversation Model — Multi-channel interactions with leads
"""
from datetime import datetime
from typing import Optional
import uuid
from sqlmodel import Field, SQLModel


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    lead_id: uuid.UUID = Field(
        foreign_key="leads.id", index=True, nullable=False
    )
    channel: str = Field(default="whatsapp", index=True, nullable=False)  # whatsapp, email, sms
    status: str = Field(default="active", index=True, nullable=False)    # active, paused, closed
    thread_id: Optional[str] = Field(default=None, index=True)
    
    # SDR Agent & Pipeline State
    sdr_agent_name: Optional[str] = Field(default=None, index=True)
    ai_mode: str = Field(default="autonomo", index=True)
    bant_score: Optional[str] = Field(default=None) # e.g. "94/100"
    budget_str: Optional[str] = Field(default=None) # e.g. "R$ 45k/mês"
    cadence_name: Optional[str] = Field(default=None, index=True)
    funnel_stage: Optional[str] = Field(default=None, index=True) # e.g. "Reunião Agendada", "Qualificação BANT"
    
    unread_count: int = Field(default=0)
    last_message_text: Optional[str] = Field(default=None)
    last_message_at: Optional[datetime] = Field(default=None)
    
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

