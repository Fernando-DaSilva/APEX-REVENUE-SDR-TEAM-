"""
Guardrail Model — Safety Rules, Prohibited Words, and Escalation Triggers
"""
from datetime import datetime
from typing import Any, Dict, List
import uuid
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Guardrail(SQLModel, table=True):
    __tablename__ = "guardrails"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    lgpd_strict: bool = Field(default=True, nullable=False)
    block_financial_promises: bool = Field(default=True, nullable=False)
    business_hours_only: bool = Field(default=True, nullable=False)
    max_discount_percent: int = Field(default=15, nullable=False)
    
    prohibited_words_json: List[str] = Field(
        default_factory=list, sa_column=Column(JSON, nullable=False)
    ) # ["garantia 100%", "sem risco", "desconto secreto"]
    
    handoff_triggers_json: List[Dict[str, Any]] = Field(
        default_factory=list, sa_column=Column(JSON, nullable=False)
    )
    
    objection_matrix_json: List[Dict[str, Any]] = Field(
        default_factory=list, sa_column=Column(JSON, nullable=False)
    )
    
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
