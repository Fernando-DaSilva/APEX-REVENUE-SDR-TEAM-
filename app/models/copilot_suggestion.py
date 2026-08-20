"""
Copilot Suggestion Model — Real-time AI response recommendations & objection handling
"""
from datetime import datetime
from typing import Optional
import uuid
from sqlmodel import Field, SQLModel


class CopilotSuggestion(SQLModel, table=True):
    __tablename__ = "copilot_suggestions"

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
    suggestion_type: str = Field(default="qa", index=True, nullable=False) # qa, docs, objection_counter, closing
    category: str = Field(nullable=False)
    title: str = Field(nullable=False)
    text: str = Field(nullable=False)
    confidence: int = Field(default=90) # 0 to 100
    source_doc: Optional[str] = Field(default=None)
    status: str = Field(default="suggested", index=True, nullable=False) # suggested, accepted, rejected, modified
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
