"""
User Model — Multi-tenant system users & SDR operators
"""
from datetime import datetime
from typing import Optional
import uuid
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    email: str = Field(index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    full_name: str = Field(nullable=False)
    role: str = Field(default="sdr", index=True, nullable=False)
    avatar_url: Optional[str] = Field(default=None)
    department: Optional[str] = Field(default=None, index=True)
    workload_active_leads: int = Field(default=0)
    status: str = Field(default="online", index=True) # online, busy, offline, suspended
    is_active: bool = Field(default=True, nullable=False)
    last_access_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

