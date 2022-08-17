from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Column, DateTime

from core.config import config


class TimestampMixin:
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.now(tz=ZoneInfo(config.APP_TIMEZONE)),
        nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(tz=ZoneInfo(config.APP_TIMEZONE)),
        onupdate=datetime.now(tz=ZoneInfo(config.APP_TIMEZONE)),
        nullable=False,
    )
