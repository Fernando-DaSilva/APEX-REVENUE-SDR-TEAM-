"""
Integration Model — External Channel & CRM Integrations Configuration
"""
from datetime import datetime
from typing import Any, Dict, Optional
import uuid
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Integration(SQLModel, table=True):
    __tablename__ = "integrations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    provider: str = Field(index=True, nullable=False) # whatsapp_zapi, google_workspace, hubspot, pipedrive, rdstation, salesforce
    status: str = Field(default="connected", index=True, nullable=False) # connected, disconnected, error
    credentials_json: Dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSON, nullable=False)
    )
    config_json: Dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSON, nullable=False)
    )
    last_synced_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
