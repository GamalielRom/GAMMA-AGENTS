from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.agent import Agent
from app.models.agent_config import AgentConfig
from app.schemas.agent_config import AgentConfigResponse, AgentConfigCreate
from app.models.agent_tool import AgentTool
from app.schemas.agent_tool import AgentToolResponse, AgentToolCreate

router = APIRouter(prefix="/agents", tags=["Agent Tools"])

@router.get("/{agent_id}/tools", response_model=list[AgentToolResponse])
def get_agent_tools(agent_id: UUID, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    tools = db.query(AgentTool).filter(AgentTool.agent_id == agent.id).all()
    return tools

@router.post("/{agent_id}/tools", response_model=AgentToolResponse)
def create_agent_tool(
    agent_id:  UUID,
    payload: AgentToolCreate,
    db: Session = Depends(get_db)
):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    existing_tool = db.query(AgentTool).filter(AgentTool.agent_id == agent_id, AgentTool.tool_name == payload.tool_name).first()
    if existing_tool:
        raise HTTPException(status_code=400, detail="Agent tool alerady exists")
    
    tool= AgentTool(
        agent_id=agent_id,
        tool_name=payload.tool_name,
        tool_type=payload.tool_type,
        config=payload.config,
        is_enabled=payload.is_enabled
    )

    db.add(tool)
    db.commit()
    db.refresh(tool)

    return tool