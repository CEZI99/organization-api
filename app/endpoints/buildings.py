from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import schemas
from app.repository import repository
from app.db import database
from typing import List

router = APIRouter()

@router.get("/", response_model=List[schemas.Building])
async def list_buildings(db: AsyncSession = Depends(database.get_db)):
    return await repository.get_buildings(db)

@router.get("/{building_id}", response_model=schemas.Building)
async def get_building(building_id: int, db: AsyncSession = Depends(database.get_db)):
    building = await repository.get_building(db, building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building
