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

    def __repr__(self):
        return "<Sensor (id: %d, name: %s)>" % (self.id, self.name)
