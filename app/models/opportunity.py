"""
Opportunity Model — Sales pipeline opportunities & meeting bookings
"""
from datetime import datetime
from typing import Optional
import uuid
from sqlmodel import Field, SQLModel


class Opportunity(SQLModel, table=True):
    __tablename__ = "opportunities"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    lead_id: uuid.UUID = Field(
        foreign_key="leads.id", index=True, nullable=False
    )
    title: str = Field(index=True, nullable=False)
    value: float = Field(default=0.0, nullable=False)
    stage: str = Field(default="qualification", index=True, nullable=False) # qualification, demo_scheduled, closed_won, closed_lost
    closed_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
