from sqlalchemy import Column, BigInteger, ForeignKey

from core.db import Base
from core.db.mixins import TimestampMixin


class AuthRoleHierarchy(Base, TimestampMixin):
    __tablename__ = "auth_role_hierarchy"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    parent_role_id = Column(BigInteger, ForeignKey("auth_role.id"), nullable=False)
    child_role_id = Column(BigInteger, ForeignKey("auth_role.id"))
