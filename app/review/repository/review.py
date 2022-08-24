from sqlalchemy import select, func

from app.review.model import Review
from core.db import session
from core.repository import BaseRepoORM


class ReviewRepo(BaseRepoORM):
    model = Review

    @classmethod
    async def count_review_with_product_id(cls, product_id: int) -> int:
        query = select(func.count(cls.model.id)).where(cls.model.product_id == product_id)
        result = await session.execute(query)
        return result.scalar()
