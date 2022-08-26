import os
from typing import Optional, Type, List

from sqlalchemy import delete, exists, select

from app.product.model import ProductWish
from core.config import config
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


def wish_models_to_entities(model_list: List[Type[ProductWish]]) -> List[Type[ProductWish]]:
    return [wish_model_to_detail_entity(model) for model in model_list]


def wish_model_to_detail_entity(model: Type[ProductWish], user_id: Optional[int] = None) -> Type[ProductWish]:
    model.product.product_id = model.product.id
    model.product.profile_image_name = model.product.profile_image[0].uploaded_name
    model.product.profile_image_url = model.product.profile_image[0].saved_name
    model.product.brand_name = model.product.user.info[0].brand_name

    return model
