import os
from tools.mcp_toolsets import get_memory_toolset

DEMO_USER_ID = os.getenv("DEMO_USER_ID", "00000000")

tools = get_memory_toolset()


async def memory_agent(user_input: str):
    results = []

    notes = await tools[0](DEMO_USER_ID, user_input, 5)
    tasks = await tools[1](DEMO_USER_ID, user_input, 5)

    if notes:
        results.append("## Notes\n" + str(notes))

    if tasks:
        results.append("## Tasks\n" + str(tasks))

    if not results:
        return "No relevant results found"

    return "\n\n".join(results)