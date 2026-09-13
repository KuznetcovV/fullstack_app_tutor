import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect(
        host="127.0.0.1",
        port=5433,
        user="postgres",
        password="postgres",
        database="fastapi_test_db",
    )
    result = await conn.fetchval("SELECT 1")
    print("УСПЕХ:", result)
    await conn.close()

asyncio.run(main())