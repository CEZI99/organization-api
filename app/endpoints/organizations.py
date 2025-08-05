from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import schemas
from app.repository import repository
from app.db import database
from typing import List

router = APIRouter()

@router.get("/by-building/{building_id}", response_model=List[schemas.Organization])
async def orgs_by_building(building_id: int, db: AsyncSession = Depends(database.get_db)):
    return await repository.get_organizations_in_building(db, building_id)

@router.get("/by-activity/{activity_id}", response_model=List[schemas.Organization])
async def orgs_by_activity(activity_id: int, db: AsyncSession = Depends(database.get_db)):
    return await repository.get_organizations_by_activity(db, activity_id)

@router.get("/in-radius", response_model=List[schemas.Organization])
async def orgs_in_radius(
    lat: float = Query(..., description="Широта центра"),
    lon: float = Query(..., description="Долгота центра"),
    radius: float = Query(..., description="Радиус в километрах"),
    db: AsyncSession = Depends(database.get_db)
):
    return await repository.get_organizations_in_radius(db, lat, lon, radius)

@router.get("/{org_id}", response_model=schemas.Organization)
async def get_org(org_id: int, db: AsyncSession = Depends(database.get_db)):
    org = await repository.get_organization(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.get("/search/by-name", response_model=List[schemas.Organization])
async def search_orgs_by_name(
    name: str = Query(..., description="Название организации"),
    db: AsyncSession = Depends(database.get_db)
):
    return await repository.search_organizations(db, name)
