from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.conversation import Conversation
from app.schemas.conversation import conversationCreate, conversationResponse
from app.models.agent import Agent
from app.models.company import Company
from app.models.lead import Lead
from uuid import UUID

router = APIRouter(prefix="/conversations", tags=["Conversations"])

@router.post("/", response_model=conversationResponse)
def create_conversation(payload: conversationCreate, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == payload.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    agent = db.query(Agent).filter(Agent.id == payload.agent_id).first()
    if not agent: 
        raise HTTPException(status_code=404, detail="Agent not found")
    
    
    if payload.lead_id is not None:
        lead = db.query(Lead).filter(Lead.id == payload.lead_id).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
    
    
    conversation = Conversation(
        company_id=payload.company_id,
        agent_id=payload.agent_id,
        lead_id=payload.lead_id,
        channel=payload.channel,
        external_contact_name=payload.external_contact_name,
        external_contact_email=payload.external_contact_email,
        status=payload.status,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation

@router.get("/{conversation_id}", response_model=conversationResponse)
def get_conversation(conversation_id: UUID, db: Session = Depends(get_db)):
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversation

@router.delete("/{conversation_id}")
def delete_conversation(conversation_id: UUID, db: Session = Depends(get_db)):
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db.delete(conversation)
    db.commit()

    return{"message":"Conversation deleted successfully"}

@router.get("/", response_model=list[conversationResponse])
def list_conversation(agent_id: UUID | None = None, db: Session = Depends(get_db)):
    query = db.query(Conversation)

    if agent_id is not None:
        query = query.filter(Conversation.agent_id == agent_id)
    
    conversations = query.order_by(Conversation.created_at.desc()).all()

    return conversations