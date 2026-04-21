from datetime import datetime
from uuid import UUID

from sqlalchemy import String, Text, TIMESTAMP, ForeignKey, func, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    conversation_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False
    )
    sender_type: Mapped[str] = mapped_column(String(20), nullable=False)
    sender_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    message_content: Mapped[str] = mapped_column(Text, nullable=False)
    message_metadata: Mapped[dict | list | None] = mapped_column("metadata", JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )