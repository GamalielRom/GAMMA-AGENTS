from datetime import datetime, timedelta
from app.services.calendar_service import create_demo_event

start_date = datetime.now().replace(second=0, microsecond=0) + timedelta(days=1)
start_date = start_date.replace(hour=14, minute=0)

result = create_demo_event(
    summary="EMPY Test Demo",
    description="Testing Google Calendar integration from EMPY backend",
    start_date=start_date,
    duration_minutes=30,
    timezone="America/Toronto",
)

print(result)