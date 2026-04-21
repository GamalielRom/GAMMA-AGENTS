from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr

class conversationResponse(BaseModel):
    id: UUID
    company_id: UUID
    agent_id: UUID
    lead_id: UUID | None
    channel: str 
    external_contact_name: str | None
    external_contact_email : str | None
    status: str
    created_at: datetime
    ended_at: datetime | None

    model_config= {
        "from_attributes": True
    }

class conversationCreate(BaseModel):
    company_id: UUID
    agent_id: UUID
    lead_id: UUID | None = None
    channel: str = "web"
    external_contact_name: str | None = None
    external_contact_email: EmailStr | None = None
    status: str = "open"