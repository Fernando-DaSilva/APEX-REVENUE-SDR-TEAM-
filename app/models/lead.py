"""
Lead Model — Prospects & Contacts target for SDR outreach
"""
from datetime import datetime
from typing import Any, Dict, Optional
import uuid
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Lead(SQLModel, table=True):
    __tablename__ = "leads"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    name: str = Field(index=True, nullable=False)
    email: Optional[str] = Field(default=None, index=True)
    phone: Optional[str] = Field(default=None, index=True)
    company_name: Optional[str] = Field(default=None, index=True)
    avatar_url: Optional[str] = Field(default=None)
    initials: Optional[str] = Field(default=None)
    role_title: Optional[str] = Field(default=None)
    channel: str = Field(default="zap", index=True) # zap, email, linkedin, phone
    
    status: str = Field(default="new", index=True, nullable=False)
    score: int = Field(default=0, index=True, nullable=False)
    
    # Deal Health Score (DHS) Subsystem
    dhs_score: int = Field(default=50, index=True) # -100 to +100
    dhs_trend: str = Field(default="stable", index=True) # up, down, stable
    dhs_variation: Optional[str] = Field(default=None) # e.g. "+15 pts", "-80 pts"
    
    # BANT & Qualification Metrics
    bant_score: int = Field(default=0, index=True) # 0 to 100
    budget_amount: Optional[float] = Field(default=None)
    
    # Assignment & Copilot Mode
    assigned_user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id", index=True)
    assigned_agent_id: Optional[uuid.UUID] = Field(default=None, index=True)
    ai_mode: str = Field(default="copiloto", index=True) # autonomo, copiloto, handoff_solicitado, humano
    
    unread_count: int = Field(default=0)
    last_message_at: Optional[datetime] = Field(default=None)
    
    metadata_json: Dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSON, nullable=False)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

