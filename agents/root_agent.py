from agents.calendar_agent import calendar_agent
from agents.task_notes_agent import task_notes_agent
from agents.memory_agent import memory_agent


async def root_agent(user_input: str):
    text = user_input.lower()

    # 🔍 MEMORY FIRST
    if "find" in text or "search" in text:
        return await memory_agent(user_input)

    # 📅 CALENDAR
    if "meeting" in text or "schedule" in text:
        return await calendar_agent(user_input)

    # 📝 TASK / NOTES
    if "task" in text or "todo" in text or "note" in text or "list" in text:
        return await task_notes_agent(user_input)

    return "Request not understood"