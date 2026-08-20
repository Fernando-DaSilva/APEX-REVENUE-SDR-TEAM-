"""
Financial Contact Model — Directory & Log History for Tenant Billing
"""
from datetime import datetime
from typing import Any, List, Optional
import uuid
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class FinancialContact(SQLModel, table=True):
    __tablename__ = "financial_contacts"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    name: str = Field(index=True, nullable=False)
    role: str = Field(nullable=False)
    department: str = Field(default="Financeiro", index=True)
    email: str = Field(index=True, nullable=False)
    phone: Optional[str] = Field(default=None)
    extension: Optional[str] = Field(default=None)
    zap: Optional[str] = Field(default=None)
    is_primary: bool = Field(default=False, index=True)
    status: str = Field(default="Ativo", index=True)
    notes: Optional[str] = Field(default=None)
    
    history_logs_json: List[Any] = Field(
        default_factory=list, sa_column=Column(JSON, nullable=False)
    )
    
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
