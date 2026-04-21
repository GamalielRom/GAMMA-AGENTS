from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.agent import Agent
from app.models.agent_config import AgentConfig
from app.schemas.agent_config import AgentConfigResponse, AgentConfigCreate

router = APIRouter(prefix="/agents", tags=["Agent Configs"])


@router.get("/{agent_id}/config", response_model=AgentConfigResponse)
def get_agent_config(agent_id: UUID, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    config = db.query(AgentConfig).filter(AgentConfig.agent_id == agent_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Agent config not found")

    return config


@router.post("/{agent_id}/config", response_model=AgentConfigResponse)
def create_agent_config(
    agent_id: UUID,
    payload: AgentConfigCreate,
    db: Session = Depends(get_db)
):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    existing_config = db.query(AgentConfig).filter(AgentConfig.agent_id == agent_id).first()
    if existing_config:
        raise HTTPException(status_code=400, detail="Agent already has a config")

    config = AgentConfig(
        agent_id=agent_id,
        system_prompt=payload.system_prompt,
        model_name=payload.model_name,
        temperature=payload.temperature,
        tone=payload.tone,
        goals=payload.goals,
        agent_constraints=payload.agent_constraints,
        escalation_rules=payload.escalation_rules,
    )

    db.add(config)
    db.commit()
    db.refresh(config)

    return config