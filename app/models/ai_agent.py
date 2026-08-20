"""
AI Agent Model — Configurable AI SDR Personas & Autonomous Bot Settings
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class AIAgent(SQLModel, table=True):
    __tablename__ = "ai_agents"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    name: str = Field(index=True, nullable=False)
    role: str = Field(nullable=False)
    avatar: str = Field(default="🤖")
    llm_model: str = Field(default="Gemini 1.5 Pro", index=True) # Gemini 1.5 Pro, GPT-4o, DeepSeek
    autonomy_level: int = Field(default=100) # 0 to 100
    autonomy_mode: str = Field(default="autonomo", index=True) # autonomo, semi, copiloto
    tone_of_voice: str = Field(default="Consultivo & Empático")
    channels_json: List[str] = Field(
        default_factory=list, sa_column=Column(JSON, nullable=False)
    ) # ["Zap", "E-mail", "LinkedIn"]
    max_simultaneous: int = Field(default=50)
    avg_response_time: str = Field(default="3.2s")
    system_prompt: str = Field(nullable=False)
    guardrails_json: Dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSON, nullable=False)
    )
    is_active: bool = Field(default=True, index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
