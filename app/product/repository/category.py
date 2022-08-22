from typing import Optional, Type, List

from sqlalchemy import select
from sqlalchemy.orm import subqueryload

from app.product.model import Category, Product
from core.db.session import session
from core.repository import BaseRepoORM


class CategoryRepo(BaseRepoORM):
    model = Category

    @classmethod
    async def get_category_list_with_children(cls) \
            -> Optional[Type[List[Category]]]:
        query = select(cls.model) \
            .distinct() \
            .options(subqueryload(cls.model.children)) \
            .where(cls.model.parent_id.is_(None))

        result = await session.execute(query)

        return result.scalars().all()