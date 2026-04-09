import os
from tools.mcp_toolsets import get_memory_toolset
from utils.response_formatter import format_memory_response

DEMO_USER_ID = os.getenv("DEMO_USER_ID", "00000000")

tools = get_memory_toolset()


def memory_agent(user_input: str):
    notes = tools[0](user_input, DEMO_USER_ID)
    tasks = tools[1](user_input, DEMO_USER_ID)

    if not notes and not tasks:
        return "No results found"

    return format_memory_response(f"{notes}\n{tasks}")