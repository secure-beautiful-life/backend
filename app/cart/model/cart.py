from sqlalchemy import Column, BigInteger, Integer, ForeignKey

from core.db import Base
from core.db.mixins import TimestampMixin


class Cart(Base, TimestampMixin):
    __tablename__ = "cart"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(BigInteger, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Integer, nullable=False)
