"""
Message Model — Multi-channel chat messages & thread history
"""
from datetime import datetime
from typing import Any, Dict, Optional
import uuid
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    conversation_id: uuid.UUID = Field(
        foreign_key="conversations.id", index=True, nullable=False
    )
    sender_type: str = Field(default="lead", index=True, nullable=False) # lead, ai, human_sdr, system
    sender_name: str = Field(nullable=False)
    text: str = Field(nullable=False)
    
    is_ai: bool = Field(default=False, index=True, nullable=False)
    is_human_operator: bool = Field(default=False, index=True, nullable=False)
    synced: bool = Field(default=True, nullable=False)
    
    confidence_score: Optional[float] = Field(default=None)
    source_doc: Optional[str] = Field(default=None) # RAG citation document
    
    metadata_json: Dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSON, nullable=False)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
