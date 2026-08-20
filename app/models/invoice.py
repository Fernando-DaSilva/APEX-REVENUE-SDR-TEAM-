"""
Invoice & Payment Method Models — White-label Subscription Billing
"""
from datetime import datetime
from typing import Any, Dict, Optional
import uuid
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Invoice(SQLModel, table=True):
    __tablename__ = "invoices"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    invoice_number: str = Field(index=True, nullable=False) # e.g. "INV-2026-07"
    description: str = Field(nullable=False)
    amount: float = Field(default=0.0, nullable=False)
    payment_method_type: str = Field(default="pix", index=True) # pix, credit_card, boleto
    status: str = Field(default="Paga", index=True, nullable=False) # Paga, Pendente, Cancelada
    due_date: Optional[datetime] = Field(default=None, index=True)
    paid_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class PaymentMethod(SQLModel, table=True):
    __tablename__ = "payment_methods"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    method_type: str = Field(default="pix", index=True, nullable=False) # pix, credit_card, boleto
    title: str = Field(nullable=False)
    subtitle: Optional[str] = Field(default=None)
    is_primary: bool = Field(default=False, index=True)
    details_json: Dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSON, nullable=False)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
