from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class AgentToolResponse(BaseModel):
    id: UUID
    agent_id: UUID
    tool_name: str
    tool_type: str
    config: dict | list | None
    is_enabled: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AgentToolCreate(BaseModel):
    tool_name: str
    tool_type: str
    config: dict | list | None = None
    is_enabled: bool = True