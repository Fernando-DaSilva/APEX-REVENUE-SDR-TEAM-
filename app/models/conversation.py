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
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
