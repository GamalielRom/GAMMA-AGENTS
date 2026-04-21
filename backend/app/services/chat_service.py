from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.llm_service import generate_agent_response
from app.models.agent import Agent
from app.models.agent_config import AgentConfig
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.task_run import TaskRun
from app.models.tool_execution import ToolExecution
from app.models.agent_tool import AgentTool
from app.schemas.chat import ChatRequest, ChatResponse
from datetime import datetime, timedelta
from app.services.calendar_service import create_demo_event
from app.services.datetime_parser import parse_requested_datetime
from app.services.calendar_service import create_demo_event
from app.services.schedule_extractor import extract_schedule_datetime_with_llm

#Here we build the agent with the response, name and config
def build_dummy_response(agent: Agent, config: AgentConfig, user_message: str) -> str:
    tone = config.tone or "default"

    return (
        f"{agent.agent_name}: I received your message: '{user_message}'. "
        f"My configured tone is '{tone}', and I can help you with your request."
    )

def get_agent_and_config(db: Session, agent_id: UUID) -> tuple[Agent, AgentConfig]:
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent: 
        raise HTTPException(status_code=404, detail="Agent not found")
    
    config =  db.query(AgentConfig).filter(AgentConfig.agent_id == agent_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Agent config not found")
    
    return agent, config

def get_or_create_conversation(
        db: Session,
        agent_id: UUID,
        payload:ChatRequest,
) -> Conversation:
    if payload.conversation_id:
        conversation = (
            db.query(Conversation).filter(Conversation.id == payload.conversation_id).first()
        )
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation
    
    conversation = Conversation(
        company_id=payload.company_id,
        agent_id=agent_id,
        lead_id=payload.lead_id,
        channel=payload.channel,
        external_contact_name=payload.external_contact_name,
        external_contact_email=payload.external_contact_email,
        status="open",
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def save_human_message(db: Session, conversation_id: UUID, payload: ChatRequest) -> Message:
    human_message = Message(
        conversation_id=conversation_id,
        sender_type="human",
        sender_name=payload.external_contact_name,
        message_content=payload.message_content,
        message_metadata={"channel": payload.channel},
    )
    db.add(human_message)
    db.commit()
    db.refresh(human_message)

    return human_message

def build_conversation_history(db: Session, conversation_id: UUID) -> list[dict]:
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    history = []
    for msg in messages:
        role = "assistant" if msg.sender_type == "agent" else "user"
        history.append({
            "role": role,
            "content": msg.message_content
        })

    return history

def save_agent_message(
    db: Session,
    conversation_id: UUID,
    agent_name: str,
    response_text: str,
    channel: str,
) -> Message:
    agent_message = Message(
        conversation_id=conversation_id,
        sender_type="agent",
        sender_name=agent_name,
        message_content=response_text,
        message_metadata={
            "channel": channel,
            "generated_by": "dummy_chat_flow",
        },
    )
    db.add(agent_message)
    db.commit()
    db.refresh(agent_message)

    return agent_message

def handle_chat(db: Session, agent_id: UUID, payload: ChatRequest) -> ChatResponse:
    agent, config = get_agent_and_config(db, agent_id)
    conversation = get_or_create_conversation(db, agent_id, payload)
    human_message = save_human_message(db, conversation.id, payload)
    task_type, required_tool_name = detect_tool_intent(payload.message_content)

    tool_result_note = ""

    if task_type and required_tool_name:
        tool = get_agent_tool_by_name(db, agent_id, required_tool_name)

        if tool:
            #create the task and tool execution records
            create_task_and_tool_execution(
                db=db,
                agent_id=agent_id,
                conversation_id=conversation.id,
                task_type=task_type,
                tool=tool,
                user_message=payload.message_content,
            )
            if required_tool_name == "calendar_scheduler":
                start_date = extract_schedule_datetime_with_llm(
                    user_msg=payload.message_content,
                    model_name=config.model_name,
                    timezone="America/Toronto"
                )

                print("Parsed datetime:", start_date)
                
                event_result = create_demo_event(
                    summary=f"Demo with {payload.external_contact_name or 'Lead'}",
                    description=f"Requested via agent. \n\nMessage: {payload.message_content}",
                    start_date=start_date,
                    duration_minutes=30,
                    timezone="America/Toronto"
                )

                tool_result_note = (
                    f"\n\nA demo event was created successfully. "
                    f"Event status: {event_result['status']}. "
                    f"Link: {event_result.get('html_link')}"
                )
            else:
                tool_result_note = (
                    f"\n\nTool action detected: '{required_tool_name}' was registered successfully."
                )
        else:
            tool_result_note = (
                f"\n\nThe request looks like it needs the tool '{required_tool_name}', but unfortunately this tool is not enabled for this agent."
            )
        


    history = build_conversation_history(db, conversation.id)

    agent_response_text = generate_agent_response(
        system_prompt= config.system_prompt,
        conversation_messages= history,
        model_name=config.model_name,
    )
    #append the tool note so it can be possible to confirm the action flow in the MVP
    agent_response_text += tool_result_note

    agent_message = save_agent_message(
        db=db,
        conversation_id=conversation.id,
        agent_name=agent.agent_name,
        response_text=agent_response_text,
        channel=payload.channel,
    )

    return ChatResponse(
        conversation_id=conversation.id,
        human_message_id=human_message.id,
        agent_message_id=agent_message.id,
        agent_response=agent_response_text,
    )

#tool execution

def detect_tool_intent(user_message: str) -> tuple[str | None, str |  None]:
    """
    A keyword intent detector
    returns:
    task_type,
    required_tool_name

    This can be also replaced with an LLM-based tool selection
    """
    message = user_message.lower()

    if "email" in message:
        return "send_email", "email_sender"
    if "schedule" in message:
        return "schedule_demo", "calendar_scheduler"
    
    return None, None

def get_agent_tool_by_name(db:Session, agent_id:UUID, tool_name: str) -> AgentTool  | None:
    """
    Find a tool that is configured and enabled for this agent
    """

    return (
        db.query(AgentTool)
        .filter(
            AgentTool.agent_id == agent_id,
            AgentTool.tool_name == tool_name,
            AgentTool.is_enabled == True
        )
        .first()
    )

def create_task_and_tool_execution(
    db:Session,
    agent_id: UUID,
    conversation_id: UUID,
    task_type: str,
    tool: AgentTool,
    user_message: str,
) -> tuple[TaskRun, ToolExecution]:
    """
    Create a task_run and a tool_execution record.
    For now this simulates the action instead of executing a real tool.
    """
     #Save the high-level task record
    task_run = TaskRun(
        agent_id=agent_id,
        conversation_id=conversation_id,
        task_type=task_type,
        input_data={"user_message": user_message},
        output_data={"result": "simulated"},
        status="completed",
        completed_at=datetime.utcnow(),
    )
    db.add(task_run)
    db.commit()
    db.refresh(task_run)

    #Save the specific tool execution linked to the task
    tool_execution = ToolExecution(
        task_run_id=task_run.id,
        agent_tool_id=tool.id,
        tool_name=tool.tool_name,
        input_payload={"user_message": user_message},
        output_payload={"result": "simulated tool execution"},
        status="success",
    )
    db.add(tool_execution)
    db.commit()
    db.refresh(tool_execution)

    return task_run, tool_execution
