from sqlalchemy import String, Text, Boolean, TIMESTAMP, ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.session import Base
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class Agent(Base):
    __tablename__ = "agents"

    
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    company_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False
    )
    agent_name: Mapped[str] = mapped_column(String(150), nullable=False)
    agent_type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="idle")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )