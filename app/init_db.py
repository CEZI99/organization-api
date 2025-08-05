from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
import os

async def init_test_data():
    engine = create_async_engine(os.getenv("DATABASE_URL"))
    
    with open("tests/test_data.sql", "r") as f:
        sql_script = f.read()
    
    async with engine.begin() as conn:
        await conn.execute(sql_script)

if __name__ == "__main__":
    asyncio.run(init_test_data())