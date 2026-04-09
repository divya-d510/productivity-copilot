# tools/database.py
import os
import asyncpg
from typing import Optional

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "productivity_db"),
    "user": os.getenv("DB_USER", "productivity_user"),
    "password": os.getenv("DB_PASSWORD", "AppPassword456!"),
}

_pool: Optional[asyncpg.Pool] = None

async def get_db_pool() -> asyncpg.Pool:
    """Get or create database connection pool"""
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(**DB_CONFIG, min_size=2, max_size=10)
    return _pool

async def execute_query(query: str, *args):
    """Execute a query and return results"""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        return await conn.fetch(query, *args)

async def execute_single(query: str, *args):
    """Execute a query and return single result"""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, *args)
