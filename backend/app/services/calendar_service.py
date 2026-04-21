from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

#Minimum scope to create and edit events

SCOPES = ["https://www.googleapis.com/auth/calendar"]

BASE_DIR = Path(__file__).resolve().parents[2]
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"

def get_calendar_service():
    """
    Authenticate the local user and return a Google Calendar service client.
    -First run opens a browser OAuth flow.
    - Then runs rueuse token.json
    """

    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE),
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    
    return build("calendar", "v3", credentials=creds)

def create_demo_event(
    summary: str,
    description: str,
    start_date: datetime,
    duration_minutes: int=30,
    timezone: str = "America/Toronto"
):
    """
    Create a real Google Calendar event in the authenticated users primary calendar.
    """

    service = get_calendar_service()

    end_date = start_date + timedelta(minutes=duration_minutes)

    event_body = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_date.isoformat(),
            "timeZone": timezone,
        },
        "end": {
            "dateTime": end_date.isoformat(),
            "timeZone": timezone,
        },
    }

    event = (
        service.events()
        .insert(calendarId="primary", body=event_body)
        .execute()
    )

    return{
        "event_id": event["id"],
        "html_link": event.get("htmlLink"),
        "status": event.get("status"),
    }