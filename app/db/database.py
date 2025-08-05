from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import asyncio
from typing import AsyncIterator
from contextlib import asynccontextmanager

Base = declarative_base()

@asynccontextmanager
async def get_engine():
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
        pool_pre_ping=True  # Добавляем проверку соединения
    )
    try:
        yield engine
    finally:
        await engine.dispose()

async def wait_for_db():
    """Ожидание готовности БД"""
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
        pool_pre_ping=True
    )
    for _ in range(3):  # 3 попытки
        try:
            async with engine.begin() as conn:
                await conn.execute("SELECT 1")
                return True
        except Exception as e:
            print(f"DB not ready, waiting... ({e})")
            await asyncio.sleep(5)
    raise Exception("Database connection failed after 10 attempts")

async def init_db():
    """Инициализация БД с ожиданием"""
    await wait_for_db()
    async with get_engine() as engine:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

AsyncSessionLocal = sessionmaker(
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal(bind=(await anext(get_engine()))) as session:
        yield session