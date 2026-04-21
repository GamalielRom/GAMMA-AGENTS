import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3")


def generate_agent_response(
    system_prompt: str,
    conversation_messages: list[dict],
    model_name: str | None = None
) -> str: 
    model = model_name or OLLAMA_MODEL

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_messages)

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": model,
            "messages": messages,
            "stream": False,
        },
        timeout=120,
    )
    response.raise_for_status()

    data = response.json()
    return data["message"]["content"]
    