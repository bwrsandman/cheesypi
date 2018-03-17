from datetime import datetime
import logging

from tornado_sqlalchemy import SessionMixin

from cheesepi.models.SensorData import SensorData
from .base import BaseHandler
from settings import settings

class HydrometerHandler(BaseHandler, SessionMixin):
    def get(self):
        """
        Get last few to update page measurements
        """
        last = self.get_argument("last", None)
        if last is not None:
            try:
                last = datetime.strptime(last, settings['hydrometer_timeformat'])
            except ValueError as e:
                logging.exception(e)
                last = None
        with self.make_session() as session:
            query = session.query(SensorData)
            if last is not None:
                query = query.filter(SensorData.timestamp > last)
            data = query.order_by(SensorData.timestamp.desc()).limit(settings['hydrometer_points']).all()[::-1]
            table = {
                'x': [i.timestamp.strftime(settings['hydrometer_timeformat']) for i in data],
                'Humidity': [i.humidity for i in data],
                'Temperature': [i.temperature for i in data],
            }
            self.write(table)
