import random
from datetime import datetime

import tornado
from tornado.gen import coroutine

from settings import settings
from tornado_sqlalchemy import (
    SessionMixin,
)

from ..models.SensorData import SensorData


class DummyApplication(object):
    def __init__(self, session_factory):
        self.settings = {'session_factory': session_factory}


class HydrometerPooler(SessionMixin):
    def __init__(self, session_factory):
        self.application = DummyApplication(session_factory)

    @tornado.gen.coroutine
    def do_something(self):
        time = datetime.utcnow().replace(microsecond=0)
        hum = random.uniform(0.0, 100.0)
        temp = random.uniform(-40.0, 40.0)
        with self.make_session() as session:
            data = SensorData(timestamp=time, temperature=temp, humidity=hum)
            yield session.add(data)
            session.commit()


@coroutine
def hydrometer_pooling_timer(session_factory):
    pooler = HydrometerPooler(session_factory)
    while True:
        nxt = tornado.gen.sleep(settings['hyrdometer_refresh_delay'])   # Start the clock.
        yield pooler.do_something()  # Run while the clock is ticking.
        yield nxt             # Wait for the timer to run out.
