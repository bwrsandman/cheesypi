import random
from datetime import datetime

import tornado
import Adafruit_DHT
import RPi.GPIO as GPIO

from tornado.gen import coroutine
from tornado.log import app_log
from tornado_sqlalchemy import (
    SessionMixin,
)

from settings import settings
from ..models.SensorData import SensorData
from ..models.Event import Event


class DummyApplication(object):
    """Tornado_sqlalchemy needs a session factory from an Application to work
    properly. Since we want this to run separately from a web application, we
    Create a dummy application which stores and returns a session factory.
    """
    def __init__(self, session_factory):
        self.settings = {'session_factory': session_factory}


class HardwareIO(SessionMixin):
    """Base class of Harware IO interfaces running in a loop

    Takes care of initializing with Dummy application.
    The function execure should be overriden
    """
    def __init__(self, session_factory):
        self.application = DummyApplication(session_factory)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @property
    def delay(self):
        raise NotImplementedError("Using abstract base class")

    @coroutine
    def execute(self):
        raise NotImplementedError("Using abstract base class")


class HydrometerPooler(HardwareIO):
    """Pool hydrometer on a GPIO port for temperature and humidity
    Add those values and their timestamp to databse"""
    @property
    def delay(self):
        return settings['hyrdometer_refresh_delay']

    @coroutine
    def execute(self):
        time = datetime.utcnow().replace(microsecond=0)
        hum, temp = Adafruit_DHT.read_retry(
            settings["hydrometer_DHT_version"],
            settings["hydrometer_data_pin"]
        )
        app_log.debug(
            "Hydrometer measured %.2f degrees and %.2f%% humidity" %
            (temp, hum)
        )
        if (settings["humidity_acceptable_values"].low > hum or
                settings["humidity_acceptable_values"].high < hum):
            app_log.warn("Measured impossible humidity (%f), discarding" % hum)
            return
        with self.make_session() as session:
            data = SensorData(timestamp=time, temperature=temp, humidity=hum)
            yield session.add(data)
            session.commit()


class RelayController(HardwareIO):
    """Check latest database temperature compared to thresholds
    Activate or deactivate relay based on thresholds"""
    def __init__(self, *args, **kwargs):
        super(RelayController, self).__init__(*args, **kwargs)
        self.channel = settings["relay_gpio_channel"]
        self.active = False

    def __enter__(self):
        ret = super(RelayController, self).__enter__()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.channel, GPIO.OUT)
        self.mark_event("POWERON")
        return ret

    def __exit__(self, exc_type, exc_value, traceback):
        self.mark_event("POWEROFF")
        GPIO.cleanup()
        return super(RelayController, self).__exit__(exc_type, exc_value, traceback)

    @property
    def delay(self):
        return settings['relay_refresh_delay']

    def mark_event(self, type_):
        with self.make_session() as session:
            time = datetime.utcnow().replace(microsecond=0)
            event = Event(timestamp=time, type_=type_)
            session.add(event)
            session.commit()

    @coroutine
    def activate(self):
        if not self.active:
            app_log.debug("Activating switch")
            self.active = True
            GPIO.output(self.channel, self.active)
            yield self.mark_event("ACTIVATE")
        else:
            yield

    @coroutine
    def deactivate(self):
        if self.active:
            app_log.debug("Deactivating switch")
            self.active = False
            GPIO.output(self.channel, self.active)
            yield self.mark_event("DEACTIVATE")
        else:
            yield


    @coroutine
    def execute(self):
        high_threshold = settings["temperature_thresholds"].high
        low_threshold = settings["temperature_thresholds"].low
        assert(high_threshold > low_threshold)
        temp = None
        with self.make_session() as session:
            data = session.query(SensorData).order_by(SensorData.timestamp.desc()).first()
            if data is not None:
                temp = data.temperature
            yield
        if temp is not None:
            if temp < low_threshold:
                app_log.debug(
                    "Last temperature measured lower than low threshold value "
                    "(%.2f < %.2f)" % (temp, low_threshold)
                )
                yield self.deactivate()
            elif temp > high_threshold:
                app_log.debug(
                    "Last temperature measured higher than high threshold value "
                    "(%.2f < %.2f)" % (temp, high_threshold)
                )
                yield self.activate()


@coroutine
def hardware_io_loop(HardwareIoClass, session_factory):
    with HardwareIoClass(session_factory) as hw:
        delay = hw.delay
        while True:
            try:
                nxt = tornado.gen.sleep(delay.total_seconds())
                yield hw.execute()  # Run while the clock is ticking.
                yield nxt             # Wait for the timer to run out.
            except Exception as e:
                app_log.exception(e)
