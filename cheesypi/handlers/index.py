# -*- coding: utf-8 -*-

from tornado_sqlalchemy import SessionMixin

from cheesypi.models.SensorData import SensorData
from cheesypi.models.Event import Event

from .base import BaseHandler
from .hydrometer import button_classes, button_labels

class MainHandler(BaseHandler, SessionMixin):

    # @tornado.web.authenticated
    def get(self):
        with self.make_session() as session:
            event = session.query(Event).order_by(Event.timestamp.desc()).first()
            sensor = session.query(SensorData).order_by(SensorData.timestamp.desc()).first()
            button_label = "OFF"
            button_class = "power-off"
            if event:
                button_label = button_labels.get(event.type_, "OFF")
                button_class = button_classes.get(event.type_, "power-off")
            last_temperature = "??"
            last_humidity = "??"
            if sensor:
                last_temperature = "%.2f" % sensor.temperature
                last_humidity = "%.2f" % sensor.humidity
            self.render(
                'index.html',
                button_label=button_label,
                button_class=button_class,
                last_temperature=last_temperature,
                last_humidity=last_humidity,
            )
