from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.repository import Repository
from app.schemas.activity import Activity
from typing import List
from app.config import settings
from app.dependencies import verify_api_key

# router = APIRouter(tags=["Activities"], dependencies=[Depends(verify_api_key)])
router = APIRouter(tags=["Activities"])


@router.get("/", response_model=List[Activity])
@cache(expire=settings.REDIS_CACHE_TTL)
async def get_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db)
):
    repo = Repository(db)
    return await repo.get_activities(skip, limit)

@router.get("/{activity_id}", response_model=Activity)
@cache(expire=settings.REDIS_CACHE_TTL)
async def get_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_db)
):
    repo = Repository(db)
    activity = await repo.get_activity(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.get("/tree/{root_id}", response_model=Activity)
@cache(expire=settings.REDIS_CACHE_TTL)
async def get_activity_tree(
    root_id: int,
    db: AsyncSession = Depends(get_db)
):
    repo = Repository(db)
    activity = await repo.get_activity_tree(root_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.get("/by-category/search", response_model=List[Activity])
@cache(expire=settings.REDIS_CACHE_TTL)
async def get_activities_by_category(
    category: str = Query(..., min_length=2),
    db: AsyncSession = Depends(get_db)
):
    repo = Repository(db)
    return await repo.get_activities_by_category(category)
