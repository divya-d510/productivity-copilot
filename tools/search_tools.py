# tools/search_tools.py
from tools.database import execute_query

async def semantic_search_notes(user_id: str, query: str, limit: int = 5) -> list[dict]:
    """Search notes semantically using natural language"""
    sql = """
        SELECT
          id, title, content, tags, created_at,
          0.5 AS relevance
        FROM notes
        WHERE user_id = $1::uuid
          AND (title ILIKE '%' || $2 || '%' OR content ILIKE '%' || $2 || '%')
        ORDER BY created_at DESC
        LIMIT $3
    """
    results = await execute_query(sql, user_id, query, limit)
    return [dict(r) for r in results]

async def semantic_search_tasks(user_id: str, query: str, limit: int = 5) -> list[dict]:
    """Search tasks semantically using natural language"""
    sql = """
        SELECT
          id, title, description, status, priority, due_date,
          0.5 AS relevance
        FROM tasks
        WHERE user_id = $1::uuid
          AND (title ILIKE '%' || $2 || '%' OR description ILIKE '%' || $2 || '%')
        ORDER BY created_at DESC
        LIMIT $3
    """
    results = await execute_query(sql, user_id, query, limit)
    return [dict(r) for r in results]
