"""
Organization Model — Primary Tenant Container
"""
from datetime import datetime
from typing import Any, Dict, Optional
import uuid
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Organization(SQLModel, table=True):
    __tablename__ = "organizations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str = Field(index=True, nullable=False)
    slug: str = Field(unique=True, index=True, nullable=False)
    domain: Optional[str] = Field(default=None, index=True)
    
    # White-Label & Branding Parameters
    tax_id: Optional[str] = Field(default=None, index=True) # CNPJ / CPF
    primary_color: str = Field(default="#EC4899")
    secondary_color: str = Field(default="#7E22CE")
    logo_url: Optional[str] = Field(default=None)
    dark_logo_url: Optional[str] = Field(default=None)
    favicon_url: Optional[str] = Field(default=None)
    theme_preset: str = Field(default="obsidian_night", index=True)
    theme_tokens_json: Dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSON, nullable=False)
    )
    remove_branding: bool = Field(default=False)
    footer_text: Optional[str] = Field(default=None)
    timezone: str = Field(default="America/Sao_Paulo")
    language: str = Field(default="pt-BR")
    
    # Billing & Plan Status
    plan_name: str = Field(default="Enterprise Growth", index=True)
    billing_cycle: str = Field(default="monthly") # monthly, yearly
    plan_status: str = Field(default="active", index=True) # active, paused, cancelled
    
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

