import os
from typing import Type, List, Optional

from sqlalchemy import select, func

from app.product.model import Product
from core.config import config
from core.db import session
from core.repository import BaseRepoORM


class ProductRepo(BaseRepoORM):
    model = Product

    @classmethod
    async def get_product_list_search_autocomplete(cls, limit: int = 10, offset: Optional[int] = None,
                                                   name: str = "") -> List[Product]:
        query = select(cls.model)

        if name:
            query = query.filter(cls.model.name.contains(name))

        if offset:
            query = query.offset(offset * limit)

        if limit > 100:
            limit = 100

        query = query.limit(limit)
        result = await session.execute(query)

        return result.scalars().all()

    @classmethod
    async def get_product_list_search_count(cls, name: str = "") -> int:
        query = select(func.count(cls.model.id)) \
            .filter(cls.model.name.contains(name))

        result = await session.execute(query)

        return result.scalar()

    @classmethod
    async def get_product_list_by_filter(cls, limit: int = 10, offset: Optional[int] = None,
                                         category_id: Optional[int] = None) -> Optional[Product]:
        query = select(cls.model)

        if category_id:
            query = query.filter_by(category_id=category_id)

        if offset:
            query = query.offset(offset * limit)

        if limit > 100:
            limit = 100

        query = query.limit(limit)
        result = await session.execute(query)

        return result.scalars().all()

    @classmethod
    async def get_product_filter_count(cls, category_id: Optional[int] = None) -> int:
        query = select(func.count(cls.model.id))

        if category_id:
            query = query.filter_by(category_id=category_id)

        result = await session.execute(query)

        return result.scalar()


def product_model_to_entity(model: Type[Product]) -> Type[Product]:
    model.product_id = model.id

    if model.profile_image:
        profile_image = model.profile_image[0]
        model.profile_image_url = os.path.join(config.PRODUCT_REVEAL_IMAGE_DIR, profile_image.saved_name)
        model.profile_image_name = profile_image.uploaded_name

    model.brand_name = model.user.info[0].brand_name

    return model


def product_models_to_entities(model_list: List[Type[Product]]) -> List[Type[Product]]:
    return [product_model_to_entity(model) for model in model_list]


def product_model_to_detail_entity(model: Type[Product], user_id: Optional[int] = None) -> Type[Product]:
    model.product_id = model.id

    if model.profile_image:
        profile_image = model.profile_image[0]
        model.profile_image_url = os.path.join(config.PRODUCT_REVEAL_IMAGE_DIR, profile_image.saved_name)
        model.profile_image_name = profile_image.uploaded_name

    model.brand_name = model.user.info[0].brand_name
    model.detail_images = []

    for detail_image in model.detail_image:
        model.detail_images.append(
            {
                'image_url': os.path.join(config.PRODUCT_REVEAL_IMAGE_DIR, detail_image.saved_name),
                'image_name': detail_image.uploaded_name
            }
        )

    return model
