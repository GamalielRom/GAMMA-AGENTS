from datetime import datetime
from uuid import UUID

from sqlalchemy import String, TIMESTAMP, ForeignKey, func, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base

class TaskRun(Base):
    __tablename__ = "task_runs"

    # The unique ID for each task execution record
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    #the agent that is triggered this task
    agent_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("agents.id", ondelete="CASCADE"),
        nullable=False
    )

    #Optional conversation linked to the task
    conversation_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="SET NULL"),
        nullable=True
    )

    #Example values: "Send_email" "schedule_demo"
    task_type: Mapped[str] = mapped_column(String(100), nullable=False)
    #input playload used to create the task
    input_data: Mapped[dict | list | None] = mapped_column(JSONB, nullable=False)
    #Output/result data from the task
    output_data: Mapped[dict | list | None] = mapped_column(JSONB, nullable=True)
    #Example values: "pending", "failed", "completed"
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")

    # Timestamp when the task started
    started_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )

    # Timestamp when the task finished, nullable for pending tasks
    completed_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)