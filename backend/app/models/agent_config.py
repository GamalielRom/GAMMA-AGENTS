from datetime import datetime
from uuid import UUID
from sqlalchemy import String, Text, TIMESTAMP, ForeignKey, func, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base

class AgentConfig(Base):
    __tablename__  = "agent_configs"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    agent_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("agents.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False, default=0.70)
    tone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    goals: Mapped[dict | list | None] = mapped_column(JSONB, nullable=True)
    agent_constraints: Mapped[dict | list | None] = mapped_column(JSONB, nullable=True)
    escalation_rules: Mapped[dict | list | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )