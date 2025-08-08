from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.repository import Repository
from app.schemas.building import Building
from app.config import settings
from app.dependencies import verify_api_key

# router = APIRouter(tags=["Buildings"], dependencies=[Depends(verify_api_key)])
router = APIRouter(tags=["Buildings"])

@router.get("/", response_model=List[Building])
@cache(expire=settings.REDIS_CACHE_TTL)
async def get_buildings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db)
):
    repo = Repository(db)
    return await repo.get_buildings(skip, limit)


@router.get("/{building_id}", response_model=Building)
@cache(expire=settings.REDIS_CACHE_TTL)
async def get_building(
    building_id: int,
    db: AsyncSession = Depends(get_db)
):
    repo = Repository(db)
    building = await repo.get_building(building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


@router.get("/by-address/search", response_model=List[Building])
@cache(expire=settings.REDIS_CACHE_TTL)
async def search_buildings_by_address(
    address: str = Query(..., min_length=2),
    db: AsyncSession = Depends(get_db)
):
    repo = Repository(db)
    return await repo.get_buildings_by_address(address)
