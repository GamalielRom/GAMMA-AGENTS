from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class AgentConfigResponse(BaseModel):
    id: UUID
    agent_id: UUID
    system_prompt: str
    model_name: str
    temperature: float
    tone: str | None
    goals: dict | list | None
    agent_constraints: dict | list | None
    escalation_rules: dict | list | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AgentConfigCreate(BaseModel):
    system_prompt: str
    model_name: str
    temperature: float = 0.70
    tone: str | None = None
    goals: dict | list | None = None
    agent_constraints: dict | list | None = None
    escalation_rules: dict | list | None = None