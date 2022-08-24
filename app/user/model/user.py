import os
from typing import Type, List

from sqlalchemy import Column, Unicode, BigInteger, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from core.config import config
from core.db import Base
from core.db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), unique=True, nullable=False)
    role_id = Column(BigInteger, ForeignKey("auth_role.id"), nullable=False)
    login_failed_count = Column(Integer, default=0)
    login_forbidden_time = Column(DateTime(timezone=True), default=None)

    role = relationship("AuthRole", backref=backref("user_role"), foreign_keys=[role_id], lazy="selectin")
    info = relationship("UserInfo", cascade="all, delete-orphan",
                        backref=backref("user_info", uselist=False), lazy="selectin")
    profile_image = relationship("UserProfileImage", cascade="all, delete-orphan",
                                 backref=backref("user_profile_image", uselist=False), lazy="selectin")


def user_model_to_entity(model: Type[User]) -> Type[User]:
    info = model.info[0]
    model.role_name = model.role.name
    model.name = info.name
    model.type = info.type
    model.gender = info.gender
    model.email = info.email
    model.phone = info.phone
    model.address = info.address
    if model.type == "brand":
        model.brand_name = info.brand_name
    if model.profile_image:
        profile_image = model.profile_image[0]
        model.profile_image_url = os.path.join(config.USER_PROFILE_REVEAL_IMAGE_DIR, profile_image.saved_name)
        model.profile_image_name = profile_image.uploaded_name

    return model


def user_models_to_entities(model_list: List[Type[User]]) -> List[Type[User]]:
    return [user_model_to_entity(model) for model in model_list]
