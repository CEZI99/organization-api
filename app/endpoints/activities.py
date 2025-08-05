from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import schemas
from app.repository import repository
from app.db import database
from typing import List

router = APIRouter()

@router.get("/", response_model=List[schemas.Activity])
async def list_activities(db: AsyncSession = Depends(database.get_db)):
    return await repository.get_activities(db)

@router.get("/{activity_id}", response_model=schemas.Activity)
async def get_activity(activity_id: int, db: AsyncSession = Depends(database.get_db)):
    activity = await repository.get_activity(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity