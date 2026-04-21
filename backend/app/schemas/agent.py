from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

#class to get the agent in the base model
class AgentResponse(BaseModel):
    id: UUID
    company_id: UUID
    agent_name: str 
    agent_type: str
    description: str | None
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
#class to create the agent in the base model
class AgentCreate(BaseModel):
    company_id: UUID
    agent_name: str
    agent_type: str
    description: str | None = None
    status: str = "idle"
    is_active: bool = True
