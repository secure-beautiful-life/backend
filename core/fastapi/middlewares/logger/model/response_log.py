from sqlalchemy import Column, BigInteger, Integer, Unicode

from core.db import Base
from core.db.mixins import TimestampMixin


class ResponseLog(Base, TimestampMixin):
    __tablename__ = "response_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(Unicode(255), nullable=False)
    status_code = Column(Integer, nullable=False)
