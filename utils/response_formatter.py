def format_task_response(result):
    return f"""
✅ Task Created
{result}
""".strip()


def format_calendar_response(result):
    return f"""
📅 Calendar Update
{result}
""".strip()


def format_memory_response(result):
    return f"""
🔎 Search Results
{result}
""".strip()


def format_section(title, content):
    return f"\n## {title}\n{content}\n"