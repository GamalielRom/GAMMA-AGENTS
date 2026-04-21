from uuid import UUID
from pydantic import BaseModel, EmailStr


class ChatRequest(BaseModel):
    conversation_id: UUID | None = None
    company_id: UUID
    lead_id: UUID | None = None
    message_content: str
    external_contact_name: str | None = None
    external_contact_email: str | None = None
    channel: str = "web"


class ChatResponse(BaseModel):
    conversation_id: UUID
    human_message_id: UUID
    agent_message_id: UUID
    agent_response: str

    