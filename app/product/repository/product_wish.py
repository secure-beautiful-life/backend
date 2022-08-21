from sqlalchemy import delete, select

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
