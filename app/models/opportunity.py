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
    
    # Financial MRR Pipeline Metrics
    mrr_estimated: float = Field(default=0.0)
    setup_fee: float = Field(default=0.0)
    probability_percent: int = Field(default=50) # 0 to 100
    weighted_value: float = Field(default=0.0)
    expected_close_date: Optional[datetime] = Field(default=None, index=True)
    
    closed_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

