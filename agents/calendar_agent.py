import os
from datetime import datetime, timedelta
from tools.mcp_toolsets import get_calendar_toolset
from utils.rule_engine import extract_date, extract_title
from utils.response_formatter import format_calendar_response

DEMO_USER_ID = os.getenv("DEMO_USER_ID", "00000000")

tools = get_calendar_toolset()


async def calendar_agent(user_input: str):
    text = user_input.lower()

    date = extract_date(text)

    # ✅ CREATE MEETING
    if "meeting" in text or "schedule" in text:
        title = extract_title(user_input)

        start_time = None
        end_time = None

        if date:
            start_time = datetime.fromisoformat(date)
            end_time = start_time + timedelta(hours=1)

        result = await tools[0](
            DEMO_USER_ID,
            title,
            "",            # description
            start_time,
            end_time
        )

        return format_calendar_response(result)

    # ✅ LIST EVENTS
    if "list" in text:
        return await tools[1](DEMO_USER_ID)

    return "Calendar request not understood"