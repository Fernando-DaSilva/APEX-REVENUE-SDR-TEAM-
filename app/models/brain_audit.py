"""
Brain Audit Model — Chain-of-Thought (CoT) & AI Decision Audit Logs
"""
from datetime import datetime
from typing import Optional
import uuid
from sqlmodel import Field, SQLModel


class BrainAuditLog(SQLModel, table=True):
    __tablename__ = "brain_audit_logs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    lead_id: uuid.UUID = Field(
        foreign_key="leads.id", index=True, nullable=False
    )
    conversation_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="conversations.id", index=True
    )
    channel: str = Field(default="Zap", index=True)
    intent: str = Field(nullable=False)
    confidence: int = Field(default=95) # 0 to 100
    guardrail_status: str = Field(default="approved", index=True) # approved, adjusted, blocked
    
    input_text: str = Field(nullable=False)
    rag_context: Optional[str] = Field(default=None)
    lead_memories_injected: Optional[str] = Field(default=None)
    generated_response: str = Field(nullable=False)
    guardrail_check: Optional[str] = Field(default=None)
    feedback: Optional[str] = Field(default=None) # thumbs_up, thumbs_down, null
    
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
