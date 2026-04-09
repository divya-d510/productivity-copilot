# tools/notes_tools.py
from tools.database import execute_query, execute_single

async def create_note(
    user_id: str,
    title: str,
    content: str,
    tags: str = ""
) -> dict:
    """Save a new note"""
    query = """
        INSERT INTO notes (user_id, title, content, tags)
        VALUES ($1::uuid, $2, $3, string_to_array($4, ','))
        RETURNING id, title, created_at
    """
    result = await execute_single(query, user_id, title, content, tags)
    return dict(result)

async def list_notes(user_id: str) -> list[dict]:
    """List recent notes"""
    query = """
        SELECT id, title, LEFT(content, 200) AS preview, tags, created_at
        FROM notes
        WHERE user_id = $1::uuid
        ORDER BY created_at DESC
        LIMIT 10
    """
    results = await execute_query(query, user_id)
    return [dict(r) for r in results]
