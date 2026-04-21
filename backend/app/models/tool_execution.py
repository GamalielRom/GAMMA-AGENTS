from datetime import datetime
from uuid import UUID

from sqlalchemy import String, TIMESTAMP, ForeignKey, func, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base

class ToolExecution(Base):
    __tablename__= "tool_executions"

    # Unique id for each tool execution record
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    # Parent task run that triggered this tool call
    task_run_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("task_runs.id", ondelete="CASCADE"),
        nullable=False
    )

    # Optional reference to the configured tool record
    agent_tool_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("agent_tools.id", ondelete="SET NULL"),
        nullable=True
    )

    # Tool name used for easy debugging / display
    tool_name: Mapped[str] = mapped_column(String(100), nullable=False)
    # Input payload sent to the tool
    input_payload: Mapped[dict | list | None] = mapped_column(JSONB, nullable=True)
    # Output payload returned by the tool
    output_payload: Mapped[dict | list | None] = mapped_column(JSONB, nullable=True)
    # Example values: "success", "failed"
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="success")
    # Execution timestamp
    executed_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )