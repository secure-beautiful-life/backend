from sqlalchemy import Column, Unicode, BigInteger, ForeignKey

from core.db import Base
from core.db.mixins import TimestampMixin


class UserInfo(Base, TimestampMixin):
    __tablename__ = "user_info"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), unique=True, nullable=False)
    type = Column(Unicode(255), nullable=False)
    brand_name = Column(Unicode(255), unique=True)
    gender = Column(Unicode(255), nullable=False)
    email = Column(Unicode(255), unique=True, nullable=False)
    phone = Column(Unicode(255), unique=True, nullable=False)
    address = Column(Unicode(255), nullable=False)
