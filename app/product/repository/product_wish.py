from typing import Optional

from sqlalchemy import delete, exists, select

from app.product.model import ProductWish
from core.db import session
from core.repository import BaseRepoORM
from core.repository.enum import SynchronizeSessionEnum


class ProductWishRepo(BaseRepoORM):
    model = ProductWish

    @classmethod
    async def exists_wish(cls, user_id: int, product_id: int):
        query = select(cls.model)
        query = query.where((cls.model.user_id == user_id) & (cls.model.product_id == product_id))

        result = await session.execute(query)

        return result.scalar()

    @classmethod
    async def delete_wish(cls, user_id: int, product_id: int, synchronize_session: SynchronizeSessionEnum = False):
        query = (
            delete(cls.model)
            .where((cls.model.user_id == user_id) & (cls.model.product_id == product_id))
            .execution_options(synchronize_session=synchronize_session)
        )
        await cls.safe_commit(query)

        return {}

    @classmethod
    async def filter_by_list_desc(cls, params: dict, limit: int = 10, offset: Optional[int] = None):
        query = select(cls.model).filter_by(**params)

        if offset:
            query = query.offset(offset * limit)

        if limit > 100:
            limit = 100

        query = query.limit(limit)
        query = query.order_by(cls.model.id.desc())

        result = await session.execute(query)

        return result.scalars().all()