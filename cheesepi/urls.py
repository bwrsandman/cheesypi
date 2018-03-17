# -*- coding: utf-8 -*-

from .handlers import (
    index,
    hydrometer,
)


url_patterns = [
    (r"/", index.MainHandler),
    (r"/hydrometer_chart", hydrometer.HydrometerHandler),
]
