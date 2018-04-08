# -*- coding: utf-8 -*-

"""Global settings for the project"""

import os.path
import datetime

from tornado.options import define, parse_config_file
from cheesypi.sensor_config import SensorConfig
from cheesypi.handlers.page_not_found import PageNotFoundHandler
from Adafruit_DHT import DHT22


define("port", default=8000, help="run on the given port", type=int)
define("config", default=None, help="tornado config file", callback=lambda path: parse_config_file(path, final=False))
define("debug", default=True, help="debug mode")
define("dbname", default='sqlite:///:memory:', help="uri of database")
# define("dbname", default='sqlite:///default.sqlite', help="uri of database")

# Hardware io
define("hydrometer_master", default=0, group="hardware io", help="hydrometer io to use by default")
define("hydrometer_time_window", default=datetime.timedelta(hours=6), group="hardware io", help="maximum time window of points to display")
define("hydrometer_points", default=200, group="hardware io", help="maximum time entries to display on dashboard graph")
define("hydrometer_refresh_delay", default=datetime.timedelta(seconds=30), group="hardware io", help="time taken between every nrew sample of the hydrometer")
define("relay_gpio_channel", default=11, group="hardware io", help="GPIO pin in which relay data channel is connected")  # pin 17
define("relay_refresh_delay", default=datetime.timedelta(seconds=15), group="hardware io", help="time taken between every hardware check of sensor status")
define("temperature_threshold_low", default=8.5, group="hardware io", help="threshold for which the relay will deactivate if the temperature falls below")
define("temperature_threshold_high", default=9.0, group="hardware io", help="threshold for which the relay will activate if the temperature goes above")
define("humidity_acceptable_values_low", default=0.0, group="hardware io", help="threshold for which humidity values below will be discarded and assumed to be a bad reading")
define("humidity_acceptable_values_high", default=100.0, group="hardware io", help="threshold for which humidity values above will be discarded and assumed to be a bad reading")
default_hydrometer_sensors = [
    SensorConfig(name="Hydrometer0", data_pin=22, DHT_version=DHT22),
]
define("hydrometer_sensors", default=default_hydrometer_sensors, type=SensorConfig, multiple=True, group="hardware io", metavar="NAME:PIN:DHT_VERSION,...")

__BASE_PACKAGE__ = "cheesypi"

settings = {}

settings["cookie_secret"] = "kZBjaVLpfX2sFj83swSRB7OF0"
settings["login_url"] = "/login"
settings["static_path"] = os.path.join(os.path.dirname(__file__), __BASE_PACKAGE__, "static")
settings["template_path"] = os.path.join(os.path.dirname(__file__), __BASE_PACKAGE__, "templates")
settings["xsrf_cookies"] = False
settings['default_handler_class'] = PageNotFoundHandler
settings['default_handler_args'] = dict(status_code=404)
settings['hydrometer_timeformat'] = "%Y-%m-%d %H:%M:%S"
