from sqlalchemy import Column, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref

from core.db import Base
from core.db.mixins import TimestampMixin


class OrderDetail(Base, TimestampMixin):
    __tablename__ = "order_detail"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey("order.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(BigInteger, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    price = Column(BigInteger, nullable=False)
    amount = Column(Integer, nullable=False)

    product = relationship("Product", backref=backref("order_detail_product"), foreign_keys=[product_id],
                           lazy="selectin")
