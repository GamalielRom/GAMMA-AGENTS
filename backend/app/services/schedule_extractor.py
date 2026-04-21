from __future__ import annotations

import json
import re
from datetime import datetime
from zoneinfo import ZoneInfo

from app.services.llm_service import generate_agent_response
from app.services.datetime_parser import parse_requested_datetime, DEFAULT_TIMEZONE


def extract_json_block(text: str) -> dict |None:
    """
    Try to extract a Json from a raw LLM output.
    """
    text = text.strip()
    #Direct Json
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    #Json inside code fences or extra text

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        return None
    
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def extract_schedule_datetime_with_llm(
    user_msg: str,
    model_name: str | None = None,
    timezone: str = DEFAULT_TIMEZONE,
)-> datetime: 
    """
    The LLM should extract the schedule datetime in a structured JSON.
    But falls back to dateparser if extraction fails.
    """
    now = datetime.now(ZoneInfo(timezone)).isoformat()

    system_prompt = (
        "You exctract scheduling date/time information from user messages. \n"
        "Return ONLY valid JSON. \n"
        "Do not add explanation.\n"
        "Use this exact schema: \n"
        '{}'
        '"iso_datetime": "YY-MM-DDTHH:MM:SS" | null, '
        '"timezone": "IANA timezone string", '
        '"confidence": "high" | "medium" | "low"'
        '}\n'
        f"Assume the timezone is {timezone} unless the user explicity says otherwise.\n"
        f"Current local datetime is {now}.\n"
        "If not reliable datetime can be extracted, set iso_datetime to null"
    )

    llm_output = generate_agent_response(
        system_prompt=system_prompt,
        conversation_messages=[
            {
            "role": "user",
            "content": user_msg,
            }
        ],
        model_name=model_name,
    )

    parsed_json = extract_json_block(llm_output)

    if parsed_json and parsed_json.get("iso_datetime"):
        try:
            dt = datetime.fromisoformat(parsed_json["iso_datetime"])
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=ZoneInfo(timezone))
                return dt
        except (ValueError, TypeError):
            pass
    
    return parse_requested_datetime(user_msg, timezone)
