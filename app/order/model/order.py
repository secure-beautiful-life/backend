import os
from typing import Type, List

from sqlalchemy import Column, BigInteger, ForeignKey, Unicode
from sqlalchemy.orm import relationship, backref

from app.product.model import Product
from core.config import config
from core.db import Base
from core.db.mixins import TimestampMixin


class Order(Base, TimestampMixin):
    __tablename__ = "order"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    status = Column(Unicode(255), nullable=False)
    address = Column(Unicode(255), nullable=False)

    details = relationship("OrderDetail", cascade="all, delete-orphan", backref=backref("order_detail"),
                           lazy="selectin")


def product_model_to_entity(model: Type[Product], price: int, amount: int) -> Type[Product]:
    model.profile_image_name = model.profile_image[0].uploaded_name
    model.profile_image_url = os.path.join(config.PRODUCT_REVEAL_IMAGE_DIR, model.profile_image[0].saved_name)
    model.price = price
    model.amount = amount

    return model


def order_model_to_entity(model: Type[Order]) -> Type[Order]:
    model.ordered_products = [product_model_to_entity(
        detail.product, price=detail.price, amount=detail.amount) for detail in model.details]
    model.total_price = sum(product.price * product.amount for product in model.ordered_products)
    model.ordered_date = model.created_at

    return model


def order_models_to_entities(model_list: List[Type[Order]]) -> List[Type[Order]]:
    return [order_model_to_entity(model) for model in model_list]
