from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.repository import Repository
from app.schemas.organization import Organization
from typing import List
from app.config import settings
from app.dependencies import verify_api_key


router = APIRouter(tags=["Organizations"], dependencies=[Depends(verify_api_key)])

@router.get("/by-building/{building_id}", response_model=List[Organization])
@cache(expire=settings.REDIS_CACHE_TTL)
async def get_orgs_by_building(
    building_id: int,
    db: AsyncSession = Depends(get_db)
):
    repo = Repository(db)
    return await repo.get_organizations_in_building(building_id)

@router.get("/by-activity/{activity_id}", response_model=List[Organization])
@cache(expire=settings.REDIS_CACHE_TTL)
async def get_orgs_by_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_db)
):
    repo = Repository(db)
    return await repo.get_organizations_by_activity(activity_id)

@router.get("/in-radius", response_model=List[Organization])
@cache(expire=settings.REDIS_CACHE_TTL)
async def get_orgs_in_radius(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    radius: float = Query(..., gt=0, le=100),  # до 100 км
    db: AsyncSession = Depends(get_db)
):
    repo = Repository(db)
    return await repo.get_organizations_in_radius(lat, lon, radius)

@router.get("/in-rect", response_model=List[Organization])
@cache(expire=settings.REDIS_CACHE_TTL)
async def get_orgs_in_rect(
    lat1: float = Query(..., ge=-90, le=90),
    lon1: float = Query(..., ge=-180, le=180),
    lat2: float = Query(..., ge=-90, le=90),
    lon2: float = Query(..., ge=-180, le=180),
    db: AsyncSession = Depends(get_db)
):
    repo = Repository(db)
    return await repo.get_organizations_in_rect(lat1, lon1, lat2, lon2)

@router.get("/{org_id}", response_model=Organization)
@cache(expire=settings.REDIS_CACHE_TTL)
async def get_organization(
    org_id: int,
    db: AsyncSession = Depends(get_db)
):
    repo = Repository(db)
    org = await repo.get_organization(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.get("/search/by-name", response_model=List[Organization])
@cache(expire=settings.REDIS_CACHE_TTL)
async def search_organizations(
    name: str = Query(..., min_length=2, max_length=100),
    db: AsyncSession = Depends(get_db)
):
    repo = Repository(db)
    return await repo.search_organizations(name)
