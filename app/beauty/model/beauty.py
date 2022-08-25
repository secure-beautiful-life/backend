from sqlalchemy import Column, BigInteger, ForeignKey, Unicode

from core.db import Base
from core.db.mixins import TimestampMixin


class Beauty(Base, TimestampMixin):
    __tablename__ = "beauty"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(BigInteger, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    saved_name = Column(Unicode(255), unique=True, nullable=False)