"""
Organization Model — Primary Tenant Container
"""
from datetime import datetime
from typing import Optional
import uuid
from sqlmodel import Field, SQLModel


class Organization(SQLModel, table=True):
    __tablename__ = "organizations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str = Field(index=True, nullable=False)
    slug: str = Field(unique=True, index=True, nullable=False)
    domain: Optional[str] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
