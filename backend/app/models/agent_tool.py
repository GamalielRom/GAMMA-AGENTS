from datetime import datetime
from uuid import UUID
from sqlalchemy import String, Text, TIMESTAMP, ForeignKey, func, text, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base

class AgentTool(Base):
    __tablename__ = "agent_tools"
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    agent_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("agents.id", ondelete="CASCADE"),
        nullable=False
    )
    tool_name: Mapped[str] = mapped_column(String(150), nullable=False)
    tool_type: Mapped[str] = mapped_column(String(100), nullable=False)
    config: Mapped[dict | list | None] = mapped_column(JSONB, nullable=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )