from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.activity import ActivityBase
from app.repository import Repository  # Изменённый импорт
from app.db.database import get_db
from app.config import settings
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ActivityBase])
@cache(expire=settings.REDIS_CACHE_TTL, namespace="activity")
async def list_activities(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)):
    repo = Repository(db)
    return await repo.get_activities(skip, limit)

@router.get("/{activity_id}", response_model=ActivityBase)
@cache(expire=settings.REDIS_CACHE_TTL, namespace="activity_details")
async def get_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_db)):
    repo = Repository(db)
    activity = await repo.get_activity(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity
