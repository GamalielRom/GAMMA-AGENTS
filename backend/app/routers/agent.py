from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.agent import Agent
from app.schemas.agent import AgentResponse
from app.schemas.agent import AgentCreate
from uuid import UUID

router = APIRouter(prefix="/agents", tags=["Agents"])

#Get the agent
@router.get("/", response_model=list[AgentResponse])
def get_agents(db: Session = Depends(get_db)):
    agents = db.query(Agent).all()
    return agents

#Get the agent by ID
@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: UUID, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return agent

#Post or create a new agent
@router.post("/", response_model=AgentResponse)
def create_agent(payload: AgentCreate, db: Session = Depends(get_db)):
    agent = Agent(
        company_id=payload.company_id,
        agent_name=payload.agent_name,
        agent_type=payload.agent_type,
        description=payload.description,
        status=payload.status,
        is_active=payload.is_active
    )
    
    db.add(agent)
    db.commit()
    db.refresh(agent)

    return agent