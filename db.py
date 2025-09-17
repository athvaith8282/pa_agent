import aiosqlite
from config import DB_PATH

async def get_sqlite_conn():
    # open async connection
    conn = await aiosqlite.connect(DB_PATH)
    return conn

async def get_distinct_thread_ids(db_path: str = DB_PATH)->list[str]:
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT DISTINCT thread_id FROM checkpoints") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]