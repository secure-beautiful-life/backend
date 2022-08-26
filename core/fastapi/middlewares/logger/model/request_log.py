from sqlalchemy import Column, Unicode, BigInteger, Integer

from core.db import Base
from core.db.mixins import TimestampMixin


class RequestLog(Base, TimestampMixin):
    __tablename__ = "request_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(Unicode(255), nullable=False)
    method = Column(Unicode(255), nullable=False)
    url = Column(Unicode(255), nullable=False)
    host = Column(Unicode(255), nullable=False)
    port = Column(Integer, nullable=False)
    user_agent = Column(Unicode(255))
    content_type = Column(Unicode(255))
    origin = Column(Unicode(255))
    referer = Column(Unicode(255))
    user_id = Column(Integer)
    user_token = Column(Unicode(255))
