"""
Knowledge & Memory Models — RAG Documents, Vector Chunks, and Long-Term Lead Memories
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class KnowledgeDocument(SQLModel, table=True):
    __tablename__ = "knowledge_documents"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    name: str = Field(index=True, nullable=False)
    category: str = Field(index=True, nullable=False) # Tabelas de Preços, Playbook de Vendas, Políticas & LGPD, Manuais & FAQs
    file_type: str = Field(default="PDF") # PDF, DOCX, XLSX
    size_bytes: int = Field(default=0)
    chunks_count: int = Field(default=0)
    status: str = Field(default="Indexed", index=True) # Indexed, Processing, Error
    last_reindexed_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class KnowledgeChunk(SQLModel, table=True):
    __tablename__ = "knowledge_chunks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    document_id: uuid.UUID = Field(
        foreign_key="knowledge_documents.id", index=True, nullable=False
    )
    chunk_index: int = Field(default=0, nullable=False)
    content: str = Field(nullable=False)
    embedding_vector_json: List[float] = Field(
        default_factory=list, sa_column=Column(JSON, nullable=False)
    )
    token_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class LeadMemory(SQLModel, table=True):
    __tablename__ = "lead_memories"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id", index=True, nullable=False
    )
    lead_id: uuid.UUID = Field(
        foreign_key="leads.id", index=True, nullable=False
    )
    category: str = Field(index=True, nullable=False) # Fatos Financeiros/Orçamento, Restrições & Datas, Preferências, Histórico de Objeções
    memory_key: str = Field(index=True, nullable=False)
    memory_value: str = Field(nullable=False)
    confidence_score: int = Field(default=95) # 0 to 100
    source: str = Field(default="Zap IA")
    verified: bool = Field(default=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
