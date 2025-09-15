import aiosqlite
from config import DB_PATH

async def get_sqlite_conn():
    # open async connection
    conn = await aiosqlite.connect(DB_PATH)
    return conn