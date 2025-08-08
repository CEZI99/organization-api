from sqlalchemy.future import select
from sqlalchemy import text, and_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Building, Organization, Activity
from typing import List, Optional, Sequence
import math
import logging

logger = logging.getLogger(__name__)

class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_organizations_in_building(self, building_id: int) -> Sequence[Organization]:
        """Получение организаций в здании"""
        result = await self.session.execute(
            select(Organization)
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
                selectinload(Organization.activities).joinedload(Activity.children)
            )
            .where(Organization.id == org_id)
        )
        res = result.scalars().first()
        logger.info("REQ")
        logger.info(res)
        return res

    async def search_organizations_by_activity(self, activity_name: str):
        """Поиск организаций по виду деятельности (с учетом иерархии)"""
        # Находим корневую активность и всех её потомков
        root_activity = await self.session.execute(
            select(Activity)
            .where(Activity.name.ilike(f"%{activity_name}%"))
        )
        root_activity = root_activity.scalars().first()

        if not root_activity:
            return []

        # Получаем все ID активностей в иерархии
        activity_ids = await self._get_child_activity_ids(root_activity.id)

        # Ищем организации, связанные с этими активностями
        result = await self.session.execute(
            select(Organization)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.activities)
            )
            .join(Organization.activities)
            .where(Activity.id.in_(activity_ids))
        )

        return result.unique().scalars().all()

    async def get_organizations_in_rect(self, lat1: float, lon1: float, lat2: float, lon2: float) -> Sequence[Organization]:
        """Поиск организаций в прямоугольной области"""
        min_lat, max_lat = sorted([lat1, lat2])
        min_lon, max_lon = sorted([lon1, lon2])        
        result = await self.session.execute(
            select(Building)
            .options(
                joinedload(Building.organizations)
                .selectinload(Organization.phones),
                joinedload(Building.organizations)
                .selectinload(Organization.activities)
            )
            .where(and_(
                Building.latitude.between(min_lat, max_lat),
                Building.longitude.between(min_lon, max_lon)
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

    async def search_organizations_by_name(self, name: str) -> Sequence[Organization]:
        """Поиск организаций по частичному совпадению названия"""
        result = await self.session.execute(
            select(Organization)
            .options(
                joinedload(Organization.building)
            )
            .where(Organization.name.ilike(f"%{name}%"))
        )
        return result.unique().scalars().all()
