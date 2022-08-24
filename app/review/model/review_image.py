from sqlalchemy import Column, Unicode, BigInteger, ForeignKey

from core.db import Base
from core.db.mixins import TimestampMixin


class ReviewImage(Base, TimestampMixin):
    __tablename__ = 'review_image'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    review_id = Column(BigInteger, ForeignKey("review.id", ondelete='CASCADE'), nullable=False)
    uploaded_name = Column(Unicode(255), nullable=False)
    saved_name = Column(Unicode(255), unique=True, nullable=False)
    size = Column(BigInteger, nullable=False)
    type = Column(Unicode(255), nullable=False)
