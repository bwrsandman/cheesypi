# -*- coding: utf-8 -*-

"""Global settings for the project"""

import os.path
import datetime
import collections
import logging

from tornado.options import define
from cheesypi.handlers.page_not_found import PageNotFoundHandler
from Adafruit_DHT import DHT22

Threshold = collections.namedtuple('Threshold', ['low', 'high'])
SensorConfig = collections.namedtuple('SensorConfig', ['name', 'DHT_version', 'data_pin'])

logging.basicConfig(level=logging.DEBUG)

define("port", default=8000, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=True, help="debug mode")

__BASE_PACKAGE__ = "cheesypi"

settings = {}

settings["debug"] = True
settings["cookie_secret"] = "kZBjaVLpfX2sFj83swSRB7OF0"
settings["login_url"] = "/login"
settings["static_path"] = os.path.join(os.path.dirname(__file__), __BASE_PACKAGE__, "static")
settings["template_path"] = os.path.join(os.path.dirname(__file__), __BASE_PACKAGE__, "templates")
settings["xsrf_cookies"] = False
settings['default_handler_class'] = PageNotFoundHandler
settings['default_handler_args'] = dict(status_code=404)
settings['temperature_thresholds'] = Threshold(low=7, high=8)
settings['relay_refresh_delay'] = datetime.timedelta(seconds=15)
settings['relay_gpio_channel'] = 11  # pin 17
settings['hyrdometer_refresh_delay'] = datetime.timedelta(minutes=1)
settings['hydrometer_points'] = 50
settings['hydrometer_time_window'] = datetime.timedelta(hours=6)
settings['hydrometer_sensors'] = [
    SensorConfig(name="Hydrometer0", DHT_version=DHT22, data_pin=22),
]
settings['hydrometer_master'] = 0
settings['hydrometer_timeformat'] = "%Y-%m-%d %H:%M:%S"
settings['humidity_acceptable_values'] = Threshold(low=0, high=300)
settings['dbname'] = 'sqlite:///default.sqlite'
