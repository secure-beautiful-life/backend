from sqlalchemy import Column, BigInteger, ForeignKey

from core.db import Base
from core.db.mixins import TimestampMixin


class ProductWish(Base, TimestampMixin):
    __tablename__ = 'product_wish'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey("product.id", ondelete='CASCADE'), nullable=False)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete='CASCADE'), nullable=False)
