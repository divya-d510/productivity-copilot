import os
from tools.mcp_toolsets import get_calendar_toolset
from utils.rule_engine import extract_date, extract_time
from utils.response_formatter import format_calendar_response

DEMO_USER_ID = os.getenv("DEMO_USER_ID", "00000000")

tools = get_calendar_toolset()


def calendar_agent(user_input: str):
    text = user_input.lower()

    date = extract_date(text)
    time = extract_time(text)

    if "meeting" in text or "schedule" in text:
        result = tools[0](user_input, DEMO_USER_ID, date, time)
        return format_calendar_response(result)

    if "list" in text:
        return tools[1](DEMO_USER_ID)

    return "Calendar request not understood"