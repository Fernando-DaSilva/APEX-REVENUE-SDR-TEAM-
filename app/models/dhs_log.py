"""
DHS Log Model — Deal Health Score history & trend tracking
"""
from datetime import datetime
from typing import Optional
import uuid
from sqlmodel import Field, SQLModel


class DHSLog(SQLModel, table=True):
    __tablename__ = "dhs_logs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    lead_id: uuid.UUID = Field(
        foreign_key="leads.id", index=True, nullable=False
    )
    score: int = Field(index=True, nullable=False) # -100 to +100
    trend: str = Field(default="stable", index=True, nullable=False) # up, down, stable
    variation: Optional[str] = Field(default=None) # e.g. "+15 pts"
    reason: Optional[str] = Field(default=None)
    recorded_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
