import asyncio
from mcp_server.utils.db import Database, Base

async def init_database():
    db = Database()
    await db.init()
    print("データベースが初期化されました")

if __name__ == "__main__":
    asyncio.run(init_database())