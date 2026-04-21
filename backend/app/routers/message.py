from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.message import MessageResponse, MessageCreate

router = APIRouter(prefix="/conversations", tags=["Messages"])


@router.post("/{conversation_id}/messages", response_model=MessageResponse)
def create_message(
    conversation_id: UUID,
    payload: MessageCreate,
    db: Session = Depends(get_db)
):
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    message = Message(
        conversation_id=conversation_id,
        sender_type=payload.sender_type,
        sender_name=payload.sender_name,
        message_content=payload.message_content,
        message_metadata=payload.message_metadata,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


@router.get("/{conversation_id}/messages", response_model=list[MessageResponse])
def get_conversation_messages(conversation_id: UUID, db: Session = Depends(get_db)):
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    return messages