from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    sender_type: str
    sender_name: str | None
    message_content: str
    message_metadata: dict | list | None
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageCreate(BaseModel):
    sender_type: str
    sender_name: str | None = None
    message_content: str
    message_metadata: dict | list | None = None
