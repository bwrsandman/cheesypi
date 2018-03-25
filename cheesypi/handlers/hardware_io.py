import random
from datetime import datetime

import tornado
import Adafruit_DHT

from tornado.gen import coroutine
from tornado.log import app_log
from tornado_sqlalchemy import (
    SessionMixin,
)

from settings import settings
from ..models.SensorData import SensorData


class DummyApplication(object):
    """Tornado_sqlalchemy needs a session factory from an Application to work
    properly. Since we want this to run separately from a web application, we
    Create a dummy application which stores and returns a session factory.
    """
    def __init__(self, session_factory):
        self.settings = {'session_factory': session_factory}


class HydrometerPooler(SessionMixin):
    def __init__(self, session_factory):
        self.application = DummyApplication(session_factory)

    @tornado.gen.coroutine
    def pool_hydrometer(self):
        time = datetime.utcnow().replace(microsecond=0)
        hum, temp = Adafruit_DHT.read_retry(
            settings["hydrometer_DHT_version"],
            settings["hydrometer_data_pin"]
        )
        with self.make_session() as session:
            data = SensorData(timestamp=time, temperature=temp, humidity=hum)
            yield session.add(data)
            session.commit()


@coroutine
def hydrometer_pooling_timer(session_factory):
    pooler = HydrometerPooler(session_factory)
    while True:
        try:
            nxt = tornado.gen.sleep(settings['hyrdometer_refresh_delay'].total_seconds())
            yield pooler.pool_hydrometer()  # Run while the clock is ticking.
            yield nxt             # Wait for the timer to run out.
        except Exception as e:
            app_log.exception(e)
