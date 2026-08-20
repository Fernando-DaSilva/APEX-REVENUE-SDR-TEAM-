"""
Webhook Models — Webhook Subscriptions and Event Delivery Logs
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class WebhookConfig(SQLModel, table=True):
    __tablename__ = "webhook_configs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    endpoint_url: str = Field(nullable=False)
    secret_token: str = Field(nullable=False)
    events_json: List[str] = Field(
        default_factory=list, sa_column=Column(JSON, nullable=False)
    ) # ["lead.created", "conversation.message", "dhs.updated"]
    is_active: bool = Field(default=True, index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class WebhookEvent(SQLModel, table=True):
    __tablename__ = "webhook_events"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    webhook_id: uuid.UUID = Field(
        foreign_key="webhook_configs.id", index=True, nullable=False
    )
    origin: str = Field(nullable=False) # e.g. "Formulário Site Inbound", "Meta Ads Webhook"
    payload_json: Dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSON, nullable=False)
    )
    status_code: int = Field(default=200, index=True)
    response_body: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
