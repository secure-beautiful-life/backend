import os
from typing import Type, List

from sqlalchemy import Column, BigInteger, ForeignKey, Unicode, Integer
from sqlalchemy.orm import relationship, backref

from core.config import config
from core.db import Base
from core.db.mixins import TimestampMixin


class Review(Base, TimestampMixin):
    __tablename__ = "review"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(BigInteger, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    content = Column(Unicode(255), nullable=False)
    rate = Column(Integer, nullable=False)

    user = relationship("User", backref=backref("review_user"), foreign_keys=[user_id], lazy="selectin")
    images = relationship("ReviewImage", cascade="all, delete-orphan", backref=backref("review_image"), lazy="selectin")


def review_model_to_entity(model: Type[Review]) -> Type[Review]:
    model.reviewer_name = model.user.info[0].name
    model.images_ = []

    for image in model.images:
        image.image_name = image.uploaded_name
        image.image_url = os.path.join(config.REVIEW_REVEAL_IMAGE_DIR, image.saved_name)
        model.images_.append(image)

    model.images = model.images_

    return model


def review_models_to_entities(model_list: List[Type[Review]]) -> List[Type[Review]]:
    return [review_model_to_entity(model) for model in model_list]
