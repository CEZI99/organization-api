from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from app.models import models
from app.schemas import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
import math


async def get_activities(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Activity]:
    """Получить список всех видов деятельности с пагинацией"""
    result = await db.execute(
        select(models.Activity)
        .offset(skip)
        .limit(limit)
        .options(selectinload(models.Activity.children)))
    return result.scalars().all()

async def get_activity(db: AsyncSession, activity_id: int) -> Optional[models.Activity]:
    """Получить вид деятельности по ID с загрузкой связанных данных"""
    result = await db.execute(
        select(models.Activity)
        .where(models.Activity.id == activity_id)
        .options(
            selectinload(models.Activity.parent),
            selectinload(models.Activity.children),
            selectinload(models.Activity.organizations)
        ))
    return result.scalars().first()

async def create_activity(db: AsyncSession, activity: schemas.ActivityCreate) -> models.Activity:
    """Создать новый вид деятельности"""
    db_activity = models.Activity(
        name=activity.name,
        parent_id=activity.parent_id
    )
    db.add(db_activity)
    await db.commit()
    await db.refresh(db_activity)
    return db_activity

async def get_child_activities(db: AsyncSession, parent_id: int, max_level: int = 3) -> List[int]:
    """Рекурсивно получить все дочерние виды деятельности (до 3 уровня вложенности)"""
    async def _get_children(parent_id: int, level: int = 1) -> List[int]:
        if level > max_level:
            return []
            
        result = await db.execute(
            select(models.Activity.id)
            .where(models.Activity.parent_id == parent_id)
        )
        child_ids = result.scalars().all()
        all_ids = child_ids.copy()
        
        for child_id in child_ids:
            all_ids.extend(await _get_children(child_id, level + 1))
            
        return all_ids
    
    return await _get_children(parent_id)

# --- Organizations CRUD ---

async def get_organizations_in_building(db: AsyncSession, building_id: int):
    """Получить организации в здании (остаётся без изменений)"""
    result = await db.execute(
        select(models.Organization)
        .options(
            joinedload(models.Organization.building),
            selectinload(models.Organization.phones),
            selectinload(models.Organization.activities)
        )
        .filter(models.Organization.building_id == building_id)
    )
    return result.scalars().all()

async def get_organizations_by_activity(db: AsyncSession, activity_id: int):
    """Получить организации по виду деятельности (с учётом иерархии)"""
    activity_ids = [activity_id] + await get_child_activities(db, activity_id)
    result = await db.execute(
        select(models.Organization)
        .options(
            joinedload(models.Organization.building),
            selectinload(models.Organization.phones),
            selectinload(models.Organization.activities)
        )
        .join(models.Organization.activities)
        .filter(models.Activity.id.in_(activity_ids))
    )
    return result.scalars().unique().all()

async def get_organization(db: AsyncSession, org_id: int):
    """Получить организацию по ID (остаётся без изменений)"""
    result = await db.execute(
        select(models.Organization)
        .options(
            joinedload(models.Organization.building),
            selectinload(models.Organization.phones),
            selectinload(models.Organization.activities)
        )
        .filter(models.Organization.id == org_id)
    )
    return result.scalars().first()

async def search_organizations(db: AsyncSession, name: str):
    """Поиск организаций по названию (остаётся без изменений)"""
    result = await db.execute(
        select(models.Organization)
        .options(
            joinedload(models.Organization.building),
            selectinload(models.Organization.phones),
            selectinload(models.Organization.activities)
        )
        .filter(models.Organization.name.ilike(f"%{name}%"))
    )
    return result.scalars().all()

# --- Buildings CRUD ---

async def get_buildings(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Получить список зданий с пагинацией"""
    result = await db.execute(
        select(models.Building)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_building(db: AsyncSession, building_id: int):
    """Получить здание по ID"""
    result = await db.execute(
        select(models.Building)
        .where(models.Building.id == building_id)
    )
    return result.scalars().first()

async def get_organizations_in_radius(db: AsyncSession, lat: float, lon: float, radius: float):
    """Получить организации в радиусе (остаётся без изменений)"""
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

    buildings = (await db.execute(select(models.Building))).scalars().all()
    building_ids = [
        b.id for b in buildings 
        if haversine(lat, lon, b.latitude, b.longitude) <= radius
    ]
    
    result = await db.execute(
        select(models.Organization)
        .options(
            joinedload(models.Organization.building),
            selectinload(models.Organization.phones),
            selectinload(models.Organization.activities)
        )
        .filter(models.Organization.building_id.in_(building_ids))
    )
    return result.scalars().all()