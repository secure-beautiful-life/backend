from sqlalchemy import select, func

from app.order.model import Order
from core.db import session
from core.repository import BaseRepoORM


class OrderRepo(BaseRepoORM):
    model = Order

    @classmethod
    async def count_order_with_user_id(cls, user_id: int) -> int:
        query = select(func.count(cls.model.id)).where(cls.model.user_id == user_id)
        result = await session.execute(query)
        return result.scalar()
