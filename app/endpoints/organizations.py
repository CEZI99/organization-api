from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.repository import Repository
from app.schemas.organization import OrganizationBase, OrganizationFull, OrganizationWithActivities, BuildingInRect
from typing import List
from app.config import settings
from app.dependencies import verify_api_key


# router = APIRouter(prefix="/api/organizations", tags=["Organizations"], dependencies=[Depends(verify_api_key)])
router = APIRouter(prefix="/api/organizations", tags=["Organizations"])


@router.get("/in_building/{building_id}", response_model=List[OrganizationBase])
@cache(expire=settings.REDIS_CACHE_TTL)
async def get_orgs_in_building(
    building_id: int,
    db: AsyncSession = Depends(get_db)
    ):
    """Cписок всех организаций находящихся в конкретном здании"""
    repo = Repository(db)
    return await repo.get_organizations_in_building(building_id)

@router.get("/by_activity/{activity_id}", response_model=List[OrganizationBase])
@cache(expire=settings.REDIS_CACHE_TTL)
async def get_orgs_by_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_db)
    ):
    """Cписок всех организаций, которые относятся к указанному виду деятельности"""
    repo = Repository(db)
    return await repo.get_organizations_by_activity(activity_id)

@router.get("/in_rect", response_model=List[BuildingInRect])
@cache(expire=settings.REDIS_CACHE_TTL)
async def get_orgs_in_rect(
    lat1: float = Query(..., ge=-90, le=90),
    lon1: float = Query(..., ge=-180, le=180),
    lat2: float = Query(..., ge=-90, le=90),
    lon2: float = Query(..., ge=-180, le=180),
    db: AsyncSession = Depends(get_db)
    ):
    """Cписок организаций, которые находятся в заданном прямоугольной области 
    относительно указанной точки на карте.
    Cписок зданий"""
    repo = Repository(db)
    return await repo.get_organizations_in_rect(lat1, lon1, lat2, lon2)

@router.get("/{org_id}", response_model=OrganizationFull)
@cache(expire=settings.REDIS_CACHE_TTL)
async def get_organization(
    org_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Вывод информации об организации по её идентификатору"""
    repo = Repository(db)
    return await repo.get_organization(org_id)

@router.get("/search/by_activity_name", response_model=List[OrganizationWithActivities])
@cache(expire=settings.REDIS_CACHE_TTL)
async def search_organizations(
    activity_name: str = Query(..., min_length=2, max_length=100),
    db: AsyncSession = Depends(get_db)
):
    """Поиск по виду деятельности"""
    repo = Repository(db)
    return await repo.search_organizations_by_activity(activity_name)

@router.get("/search/by_name/{org_name}", response_model=List[OrganizationBase])
@cache(expire=settings.REDIS_CACHE_TTL)
async def search_organizations_by_name(
    org_name: str,
    db: AsyncSession = Depends(get_db)
    ):
    """Поиск организаций по названию (регистронезависимый)"""
    repo = Repository(db)
    return await repo.search_organizations_by_name(org_name)
