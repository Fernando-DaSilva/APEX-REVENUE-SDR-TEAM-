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
    status: str = Field(default="new", index=True, nullable=False)
    score: int = Field(default=0, index=True, nullable=False)
    metadata_json: Dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSON, nullable=False)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
