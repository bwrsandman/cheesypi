from datetime import datetime
import logging

from tornado_sqlalchemy import SessionMixin

from cheesypi.models.SensorData import SensorData
from cheesypi.models.Event import Event

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
            min_date = datetime.utcnow() - settings["hydrometer_time_window"]

            sensor_query = session.query(SensorData).filter(
                SensorData.timestamp > min_date
            )
            if last is not None:
                sensor_query = sensor_query.filter(SensorData.timestamp > last)
            sensor_query = sensor_query.order_by(SensorData.timestamp.desc())
            sensor_data = sensor_query.limit(settings['hydrometer_points']).all()[::-1]

            event_query = session.query(Event).filter(
                Event.timestamp > min_date
            )
            event_query = event_query.order_by(Event.timestamp.desc())
            event_data = event_query.limit(settings['hydrometer_points']).all()[::-1]

            table = {
                "data": {
                    'x': [
                        i.timestamp.strftime(settings['hydrometer_timeformat'])
                        for i in sensor_data
                    ],
                    'Humidity': [i.humidity for i in sensor_data],
                    'Temperature': [i.temperature for i in sensor_data],
                },
                "grid": {
                    "x": {
                        "lines": [
                            {
                                "value": i.timestamp.strftime(
                                    settings['hydrometer_timeformat']
                                ),
                                "text": i.type_,
                            }
                            for i in event_data
                        ],
                    },
                    "y": {
                        "lines": [
                            {
                                "value": settings["temperature_thresholds"].low,
                                "text": "Low threshold",
                                "axis": "y",
                                "position": "middle",
                                "color": "blue",
                            },
                            {
                                "value": settings["temperature_thresholds"].high,
                                "text": "High threshold",
                                "axis": "y",
                                "position": "middle",
                                "color": "red",
                            },
                        ],
                    },
                },
            }
            self.write(table)
