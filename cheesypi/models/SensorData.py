from sqlalchemy import (
    Column,
    DateTime,
    Float,
)

from settings import settings

from .base import Base
# from .Sensor import Sensor


class SensorData(Base):
    __tablename__ = 'sensor_data'

    # sensor_id = Column(Sensor, primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    temperature = Column(Float)
    humidity = Column(Float)

    def __repr__(self):
        return (
            "<Sensor"
            # "%03d "
            "Data(datetime=%s, temperature: %2.2f, humidity: %2.2f)>" % (
            # self.sensor_id.id,
            self.timestamp.strftime(settings['hydrometer_timeformat']),
            self.temperature,
            self.humidity,
        ))
