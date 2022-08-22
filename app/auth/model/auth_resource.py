from typing import Type, List

from sqlalchemy import Column, Unicode, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, backref

from core.db import Base
from core.db.mixins import TimestampMixin


class AuthResource(Base, TimestampMixin):
    __tablename__ = "auth_resource"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    method = Column(Unicode(255), nullable=False)
    url = Column(Unicode(255), nullable=False)
    role_id = Column(BigInteger, ForeignKey("auth_role.id"), nullable=False)

    role = relationship("AuthRole", backref=backref("resource_role"), foreign_keys=[role_id], lazy="selectin")


def resource_model_to_entity(model: Type[AuthResource]) -> Type[AuthResource]:
    model.role_name = model.role.name

    return model


def resource_models_to_entities(model_list: List[Type[AuthResource]]) -> List[Type[AuthResource]]:
    return [resource_model_to_entity(model) for model in model_list]
