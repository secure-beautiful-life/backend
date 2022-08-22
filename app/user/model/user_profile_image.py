from sqlalchemy import Column, Unicode, BigInteger, ForeignKey

from core.db import Base
from core.db.mixins import TimestampMixin


class UserProfileImage(Base, TimestampMixin):
    __tablename__ = "user_profile_image"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id"), unique=True, nullable=False)
    uploaded_name = Column(Unicode(255), nullable=False)
    saved_name = Column(Unicode(255), unique=True, nullable=False)
    size = Column(BigInteger, nullable=False)
    type = Column(Unicode(255), nullable=False)
