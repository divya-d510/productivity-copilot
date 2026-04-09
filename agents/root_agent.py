from agents.calendar_agent import calendar_agent
from agents.task_notes_agent import task_notes_agent
from agents.memory_agent import memory_agent
from utils.rule_engine import detect_intents
from utils.response_formatter import format_section


async def root_agent(user_input: str):
    intents = detect_intents(user_input)
    sections = []

    if "memory" in intents:
        res = memory_agent(user_input)
        sections.append(format_section("Memory", res))

    if "calendar" in intents:
        res = calendar_agent(user_input)
        sections.append(format_section("Calendar", res))

    if "task" in intents or "note" in intents:
        res = await task_notes_agent(user_input)
        sections.append(format_section("Tasks", res))

    if not sections:
        return "Sorry, I couldn't understand your request."

    return "".join(sections).strip()