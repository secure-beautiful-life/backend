from sqlalchemy import Column, Unicode, BigInteger

from core.db import Base
from core.db.mixins import TimestampMixin


class AuthRole(Base, TimestampMixin):
    __tablename__ = "auth_role"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    description = Column(Unicode(255))
