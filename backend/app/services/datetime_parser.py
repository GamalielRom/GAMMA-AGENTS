from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from dateparser.search import search_dates
import dateparser


DEFAULT_TIMEZONE = "America/Toronto"


def fallback_demo_datetime(timezone: str = DEFAULT_TIMEZONE) -> datetime:
    """
    Fallback datetime just when we can't confidently parse the users request.
    Default: tomorrow at 2:00 PM local time.
    """
    now = datetime.now(ZoneInfo(timezone))
    fallback = now + timedelta(days=1)
    return fallback.replace(hour=14, minute=0, second=0, microsecond=0)


def parse_requested_datetime(
    user_message: str,
    timezone: str = DEFAULT_TIMEZONE,
) -> datetime:
    """
    Try to parse a scheduling datetime from natural language.
    Falls back to tomorrow at 2 PM if fails again.
    """
    now = datetime.now(ZoneInfo(timezone))
    cleaned_message = user_message.replace("?", "").strip()
    results = search_dates(
        cleaned_message,
        settings={
            "TIMEZONE": timezone,
            "TO_TIMEZONE": timezone,
            "RETURN_AS_TIMEZONE_AWARE": True,
            "PREFER_DATES_FROM": "future",
            "RELATIVE_BASE": now,
        },
    )

    if not results:
        return fallback_demo_datetime(timezone)

    #take the first date that was detected 
    _, parsed = results[0]
    # If the user didn't specify a time, set a friendly default
    if parsed.hour == 0 and parsed.minute == 0:
        parsed = parsed.replace(hour=14, minute=0, second=0, microsecond=0)

    return parsed