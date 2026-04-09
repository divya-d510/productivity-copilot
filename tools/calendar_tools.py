# tools/calendar_tools.py
from tools.database import execute_query, execute_single

async def create_event(
    user_id: str,
    title: str,
    description: str,
    start_time: str,
    end_time: str,
    location: str = ""
) -> dict:
    """Create a new calendar event"""
    query = """
        INSERT INTO calendar_events
          (user_id, title, description, start_time, end_time, location)
        VALUES ($1::uuid, $2, $3, $4::timestamptz, $5::timestamptz, $6)
        RETURNING id, title, start_time, end_time, location
    """
    result = await execute_single(query, user_id, title, description, start_time, end_time, location)
    return dict(result)

async def list_events(user_id: str, days_ahead: int = 7) -> list[dict]:
    """List upcoming calendar events"""
    query = """
        SELECT id, title, description, start_time, end_time, location
        FROM calendar_events
        WHERE user_id = $1::uuid
          AND start_time BETWEEN NOW() AND NOW() + ($2 || ' days')::interval
        ORDER BY start_time
        LIMIT 20
    """
    results = await execute_query(query, user_id, days_ahead)
    return [dict(r) for r in results]

async def check_availability(user_id: str, start_time: str, end_time: str) -> dict:
    """Check if a user has any events during a time slot"""
    query = """
        SELECT
          COUNT(*) AS conflict_count,
          ARRAY_AGG(title) AS conflicting_events
        FROM calendar_events
        WHERE user_id = $1::uuid
          AND tstzrange(start_time, end_time) &&
              tstzrange($2::timestamptz, $3::timestamptz)
    """
    result = await execute_single(query, user_id, start_time, end_time)
    return dict(result)
