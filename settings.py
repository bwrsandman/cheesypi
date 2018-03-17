# -*- coding: utf-8 -*-

"""Global settings for the project"""

import os.path

from tornado.options import define
from cheesepi.handlers.page_not_found import PageNotFoundHandler


define("port", default=8000, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=True, help="debug mode")

__BASE_PACKAGE__ = "cheesepi"

settings = {}

settings["debug"] = True
settings["cookie_secret"] = "kZBjaVLpfX2sFj83swSRB7OF0"
settings["login_url"] = "/login"
settings["static_path"] = os.path.join(os.path.dirname(__file__), __BASE_PACKAGE__, "static")
settings["template_path"] = os.path.join(os.path.dirname(__file__), __BASE_PACKAGE__, "templates")
settings["xsrf_cookies"] = False
settings['default_handler_class'] = PageNotFoundHandler
settings['default_handler_args'] = dict(status_code=404)
settings['hyrdometer_refresh_delay'] = 5
settings['hydrometer_points'] = 50
settings['hydrometer_timeformat'] = "%Y-%m-%d %H:%M:%S"
settings['dbname'] = 'sqlite:///default.sqlite'
