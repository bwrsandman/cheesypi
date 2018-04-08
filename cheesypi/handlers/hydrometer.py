from datetime import datetime
import logging

from tornado.options import options
from tornado_sqlalchemy import SessionMixin

from cheesypi.models.SensorData import SensorData
from cheesypi.models.Event import Event

from .base import BaseHandler
from settings import settings

button_classes = {"ACTIVATE": "power-on"}
button_labels = {"ACTIVATE": "ON"}


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
            min_date = datetime.utcnow() - options.hydrometer_time_window

            sensor_query = session.query(SensorData).filter(
                SensorData.timestamp > min_date
            ).filter(
                SensorData.sensor_id == options.hydrometer_master
            )
            if last is not None:
                sensor_query = sensor_query.filter(SensorData.timestamp > last)
            sensor_query = sensor_query.order_by(SensorData.timestamp.desc())
            sensor_data = sensor_query.limit(options.hydrometer_points).all()[::-1]

            event_query = session.query(Event).filter(
                Event.timestamp > min_date
            )
            event_query = event_query.order_by(Event.timestamp.desc())
            event_data = event_query.limit(options.hydrometer_points).all()[::-1]

            button_label = "OFF"
            button_class = "power-off"
            if event_data:
                button_label = button_labels.get(event_data[-1].type_, "OFF")
                button_class = button_classes.get(event_data[-1].type_, "power-off")
            else:
                last_event_type = session.query(Event.type_).order_by(SensorData.timestamp.desc()).first()
                if last_event_type:
                    button_label = button_labels.get(last_event_type, "OFF")
                    button_class = button_classes.get(last_event_type, "power-off")

            tempLabel = None
            humLabel = None
            if sensor_data:
                tempLabel = sensor_data[-1].temperature
                humLabel = sensor_data[-1].humidity

            table = {
                "graph": {
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
                                    "value": options.temperature_threshold_low,
                                    "text": "Low threshold",
                                    "axis": "y",
                                    "position": "middle",
                                    "color": "blue",
                                },
                                {
                                    "value": options.temperature_threshold_high,
                                    "text": "High threshold",
                                    "axis": "y",
                                    "position": "middle",
                                    "color": "red",
                                },
                            ],
                        },
                    },
                },
                "status": {
                    "button": {
                        "textContent": button_label,
                        "className": button_class,
                    },
                    "tempLabel": "%.2f°C" % tempLabel if tempLabel is not None else "??°C",
                    "humLabel": "%.2f%%" % humLabel if humLabel is not None else "??%",
                }
            }
            self.write(table)
