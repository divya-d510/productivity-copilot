# tools/task_tools.py
from typing import Optional
from tools.database import execute_query, execute_single
from utils.rule_engine import extract_title

async def create_task(
    user_id: str,
    title: str,
    description: str = "",
    priority: str = "medium",
    due_date: str = ""
) -> dict:
    """Create a new task for the user"""
    query = """
        INSERT INTO tasks (user_id, title, description, priority, due_date)
        VALUES ($1::uuid, $2, $3, $4, NULLIF($5, '')::timestamptz)
        RETURNING id, title, status, priority, due_date, created_at
    """
    result = await execute_single(query, user_id, title, description, priority, due_date)
    return dict(result)

async def list_tasks(user_id: str, status_filter: str = "all") -> list[dict]:
    """List all tasks for a user, optionally filtered by status"""
    query = """
        SELECT id, title, description, status, priority, due_date, created_at
        FROM tasks
        WHERE user_id = $1::uuid
          AND ($2 = 'all' OR status = $2)
        ORDER BY
          CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
          due_date NULLS LAST
        LIMIT 20
    """
    results = await execute_query(query, user_id, status_filter)
    return [dict(r) for r in results]

async def update_task_status(task_id: str, new_status: str) -> dict:
    """Update the status of a task"""
    query = """
        UPDATE tasks SET status = $2, updated_at = NOW()
        WHERE id = $1::uuid
        RETURNING id, title, status, updated_at
    """
    result = await execute_single(query, task_id, new_status)
    return dict(result)

async def get_task(task_id: str) -> dict:
    """Get a single task by ID"""
    query = """
        SELECT id, title, description, status, priority, due_date, created_at
        FROM tasks WHERE id = $1::uuid
    """
    result = await execute_single(query, task_id)
    return dict(result) if result else {}
