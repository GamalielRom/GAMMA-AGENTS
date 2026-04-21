from sqlalchemy import String, Text, Boolean, TIMESTAMP, ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.session import Base
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class Conversation(Base):
    __tablename__="conversations"

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
    agent_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("agents.id", ondelete="CASCADE"),
        nullable=False
    )
    lead_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False
    )
    channel: Mapped[str] = mapped_column(String(50), nullable=False, default="web")
    external_contact_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    external_contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open")
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )
    ended_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)