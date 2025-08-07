from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from redis import asyncio as aioredis
from app.db import database
from app.endpoints import organizations, buildings, activities
from app.dependencies import dependencies
from app.config import settings
from contextlib import asynccontextmanager
from typing import AsyncIterator
import logging

# Настройка логирования
logging.basicConfig(
    level=settings.LOG_LEVEL.upper(),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Lifespan handler для управления жизненным циклом приложения"""
    # Startup логика

    # Инициализация Redis для кеширования
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    logger.info("Redis cache initialized")
    logger.info("Starting application in %s mode", settings.APP_ENV)
    await database.init_db()

    if settings.DEBUG:
        logger.warning("Приложение запущено в DEBUG режиме!")
        logger.info("Документация API доступна по /docs и /redoc")

    yield  # Здесь приложение работает

    # Shutdown логика (при необходимости)
    logger.info("Shutting down application")

app = FastAPI(
    title="Organization Directory API",
    description="REST API для справочника организаций",
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
    dependencies=[Depends(dependencies.verify_api_key)] if not settings.DEBUG else None
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else ["https://prod.ru"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(organizations.router, prefix="/api/organizations")
app.include_router(buildings.router, prefix="/api/buildings")
app.include_router(activities.router, prefix="/api/activities")

@app.get("/health")
async def health_check():
    """Эндпоинт для проверки работоспособности"""
    return {
        "status": "ok",
        "environment": settings.APP_ENV,
        "debug": settings.DEBUG,
        "redis_status": "enabled" if settings.REDIS_HOST else "disabled"
    }
