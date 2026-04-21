from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import handle_chat

router = APIRouter(prefix="/agents", tags=["Chat"])


@router.post("/{agent_id}/chat", response_model=ChatResponse)
def chat_with_agent(
    agent_id: UUID,
    payload: ChatRequest,
    db: Session = Depends(get_db),
):
    return handle_chat(db=db, agent_id=agent_id, payload=payload)