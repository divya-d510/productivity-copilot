import os
from tools.mcp_toolsets import get_task_notes_toolset
from utils.rule_engine import extract_priority, extract_date, extract_title
from utils.response_formatter import format_task_response

DEMO_USER_ID = os.getenv("DEMO_USER_ID", "00000000")

tools = get_task_notes_toolset()


async def task_notes_agent(user_input: str):
    text = user_input.lower()

    priority = extract_priority(text)   # ✅ lowercase
    date = extract_date(text)

    # ✅ CREATE TASK
    if "task" in text or "todo" in text:
        title = extract_title(user_input)

        result = await tools[0](
            DEMO_USER_ID,
            title,
            "",          # description
            priority,
            date
        )

        return format_task_response(result)

    # ✅ CREATE NOTE
    if "note" in text:
        return await tools[4](DEMO_USER_ID, extract_title(user_input))

    # ✅ LIST TASKS
    if "list" in text:
        return await tools[1](DEMO_USER_ID)

    return "Task/Note request not understood"