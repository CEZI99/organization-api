from sqlalchemy.future import select
from sqlalchemy import text, and_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Building, Organization, Activity, Phone
from typing import List, Optional, Sequence
import math

class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # ========== Buildings Methods ==========
    async def get_buildings(self, skip: int = 0, limit: int = 100) -> Sequence[Building]:
        """Получение списка зданий с пагинацией"""
        result = await self.session.execute(
            select(Building)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_building(self, building_id: int) -> Optional[Building]:
        """Получение здания по ID"""
        result = await self.session.execute(
            select(Building)
            .where(Building.id == building_id)
        )
        return result.scalars().first()

    async def get_buildings_by_address(self, address: str) -> Sequence[Building]:
        """Поиск зданий по адресу"""
        result = await self.session.execute(
            select(Building)
            .where(Building.address.ilike(f"%{address}%"))
        )
        return result.scalars().all()

    # ========== Activities Methods ==========
    async def get_activities(self, skip: int = 0, limit: int = 100) -> Sequence[Activity]:
        """Получение списка видов деятельности с пагинацией"""
        result = await self.session.execute(
            select(Activity)
            .offset(skip)
            .limit(limit)
            .options(selectinload(Activity.children))
        )
        return result.scalars().all()

    async def get_activity(self, activity_id: int) -> Optional[Activity]:
        """Получение вида деятельности по ID с полной иерархией"""
        result = await self.session.execute(
            select(Activity)
            .where(Activity.id == activity_id)
            .options(
                selectinload(Activity.parent),
                selectinload(Activity.children),
                selectinload(Activity.organizations)
            )
        )
        return result.scalars().first()

    async def get_activities_by_category(self, category: str) -> Sequence[Activity]:
        """Получение видов деятельности по категории"""
        result = await self.session.execute(
            select(Activity)
            .where(Activity.category.ilike(f"%{category}%"))
            .options(selectinload(Activity.children))
        )
        return result.scalars().all()

    async def get_activity_tree(self, root_id: int = None) -> Sequence[Activity]:
        """Получение дерева видов деятельности"""
        if root_id:
            result = await self.session.execute(
                select(Activity)
                .where(Activity.id == root_id)
                .options(selectinload(Activity.children))
            )
            return result.scalars().first()
        else:
            result = await self.session.execute(
                select(Activity)
                .where(Activity.parent_id == None)
                .options(selectinload(Activity.children))
            )
            return result.scalars().all()

    # ========== Organizations Methods ==========
    async def get_organizations_in_building(self, building_id: int) -> Sequence[Organization]:
        """Получение организаций в здании"""
        result = await self.session.execute(
            select(Organization)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.activities)
            )
            .where(Organization.building_id == building_id)
        )
        return result.unique().scalars().all()

    async def get_organizations_by_activity(self, activity_id: int) -> Sequence[Organization]:
        """Получение организаций по виду деятельности (с учетом иерархии)"""
        activity_ids = [activity_id] + await self._get_child_activity_ids(activity_id)
        result = await self.session.execute(
            select(Organization)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.activities)
            )
            .join(Organization.activities)
            .where(Activity.id.in_(activity_ids))
        )
        return result.unique().scalars().all()

    async def get_organization(self, org_id: int) -> Optional[Organization]:
        """Получение организации по ID"""
        result = await self.session.execute(
            select(Organization)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.activities)
            )
            .where(Organization.id == org_id)
        )
        return result.scalars().first()

    async def search_organizations(self, name: str) -> Sequence[Organization]:
        """Поиск организаций по названию"""
        result = await self.session.execute(
            select(Organization)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.activities)
            )
            .where(Organization.name.ilike(f"%{name}%"))
        )
        return result.unique().scalars().all()

    async def get_organizations_in_radius(self, lat: float, lon: float, radius: float) -> Sequence[Organization]:
        """Поиск организаций в радиусе"""
        buildings = (await self.session.execute(select(Building))).scalars().all()
        building_ids = [
            b.id for b in buildings 
            if self._haversine(lat, lon, b.latitude, b.longitude) <= radius
        ]
        
        result = await self.session.execute(
            select(Organization)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.activities)
            )
            .where(Organization.building_id.in_(building_ids))
        )
        return result.unique().scalars().all()

    async def get_organizations_in_rect(self, lat1: float, lon1: float, lat2: float, lon2: float) -> Sequence[Organization]:
        """Поиск организаций в прямоугольной области"""
        result = await self.session.execute(
            select(Organization)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.activities)
            )
            .join(Building)
            .where(and_(
                Building.latitude.between(min(lat1, lat2), max(lat1, lat2)),
                Building.longitude.between(min(lon1, lon2), max(lon1, lon2))
            ))
        )
        return result.unique().scalars().all()

    # ========== Helper Methods ==========
    async def _get_child_activity_ids(self, parent_id: int, max_level: int = 3) -> List[int]:
        """Рекурсивное получение ID дочерних активностей (до 3 уровня)"""
        async def _get_children(pid: int, level: int = 1) -> List[int]:
            if level > max_level:
                return []
                
            result = await self.session.execute(
                select(Activity.id)
                .where(Activity.parent_id == pid)
            )
            child_ids = result.scalars().all()
            all_ids = child_ids.copy()
            
            for cid in child_ids:
                all_ids.extend(await _get_children(cid, level + 1))
                
            return all_ids

        return await _get_children(parent_id)

    @staticmethod
    def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Вычисление расстояния между точками (км)"""
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
