from sqlalchemy import Column, Unicode, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from core.db import Base
from core.db.mixins import TimestampMixin


class Category(Base, TimestampMixin):
    __tablename__ = 'category'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    depth = Column(Integer, default=0)

    parent_id = Column(BigInteger, ForeignKey("category.id", ondelete='CASCADE'))

    children = relationship("Category", backref=backref('parent', remote_side=[id]))
