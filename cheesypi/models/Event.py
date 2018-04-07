from sqlalchemy import (
    Column,
    DateTime,
    String,
)

from settings import settings

from .base import Base


class Event(Base):
    __tablename__ = 'event'

    timestamp = Column(DateTime, primary_key=True)
    type_ = Column(String)

    def __repr__(self):
        return "<Event (datetime=%s, type=%s>" % (
            self.timestamp.strftime(settings['hydrometer_timeformat']),
            self.type_
        )
