from sqlalchemy import delete, func, select

from app.cart.model import Cart
from core.db import session
from core.repository import BaseRepoORM, SynchronizeSessionEnum


class CartRepo(BaseRepoORM):
    model = Cart

    @classmethod
    async def truncate_cart_by_user_id(cls, user_id: int, synchronize_session: SynchronizeSessionEnum = False) -> None:
        query = (
            delete(cls.model)
            .where(cls.model.user_id == user_id)
            .execution_options(synchronize_session=synchronize_session)
        )
        await cls.safe_commit(query)
        return

    @classmethod
    async def cart_count_with_user_id(cls, user_id: int) -> int:
        query = select(func.count(cls.model.id)).where(cls.model.user_id == user_id)
        result = await session.execute(query)
        return result.scalar()
