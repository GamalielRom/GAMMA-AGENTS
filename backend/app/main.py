from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.db.session import engine
from app.routers.agent import router as agent_router
from app.routers.agent_config import router as agent_config_router
from app.routers.agent_tool import router as agent_tool_router
from app.routers.conversation import router as conversation_router
from app.routers.message import router as message_router
from app.routers.chat import router as chat_router
import app.models

app = FastAPI(title="GAMMA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router)
app.include_router(agent_config_router)
app.include_router(agent_tool_router)
app.include_router(conversation_router)
app.include_router(message_router)
app.include_router(chat_router)

@app.get("/")
def root():
    return {"message" : "GAMMA backend running"}

@app.get("/health/db")
def db_health():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        value = result.scalar()

    return {
        "database": "connected",
        "result": value
    }