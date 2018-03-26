# -*- coding: utf-8 -*-

"""Global settings for the project"""

import os.path
import datetime
import collections
import logging

from tornado.options import define
from cheesypi.handlers.page_not_found import PageNotFoundHandler
from Adafruit_DHT import DHT11

TempThreshold = collections.namedtuple('TempThreshold', ['low', 'high'])

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
settings['temperature_thresholds'] = TempThreshold(low=6, high=8)
settings['relay_refresh_delay'] = datetime.timedelta(seconds=15)
settings['relay_gpio_channel'] = 11  # pin 17
settings['hyrdometer_refresh_delay'] = datetime.timedelta(minutes=1)
settings['hydrometer_points'] = 50
settings['hydrometer_DHT_version'] = DHT11
settings['hydrometer_data_pin'] = 22
settings['hydrometer_timeformat'] = "%Y-%m-%d %H:%M:%S"
settings['dbname'] = 'sqlite:///default.sqlite'
