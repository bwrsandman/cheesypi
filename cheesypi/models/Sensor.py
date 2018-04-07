from sqlalchemy import (
    Column,
    Integer,
    String,
)

from .base import Base


class Sensor(Base):
    __tablename__ = 'sensor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    pin = Column(Integer)
    version = Column(Integer)

    def __repr__(self):
        return "<Sensor (id: %d, name: %s, pin: %d, version: %d)>" % (
            self.id,
            self.name,
            self.pin,
            self.version,
        )
