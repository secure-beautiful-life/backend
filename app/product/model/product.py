from sqlalchemy import Column, BigInteger, Unicode, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from core.db import Base
from core.db.mixins import TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = 'product'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    category_id = Column(BigInteger, ForeignKey("category.id", ondelete='CASCADE'), nullable=False)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete='CASCADE'), nullable=False)
    user = relationship("User", foreign_keys=[user_id], lazy="selectin")

    name = Column(Unicode(255), nullable=False)
    price = Column(Integer, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    profile_image = relationship("ProductProfileImage", cascade="all, delete-orphan",
                                 backref=backref("product_profile_image", uselist=False), lazy="selectin")
    detail_image = relationship("ProductDetailImage", cascade="all, delete-orphan",
                                backref=backref("product_detail_image", uselist=False), lazy="selectin")
    beauty_image = relationship("ProductBeautyImage", cascade="all, delete-orphan",
                                backref=backref("product_beauty_image", uselist=False), lazy="selectin")