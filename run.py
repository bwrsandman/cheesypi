#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Basic run script"""

import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
from tornado.options import options
from tornado_sqlalchemy import make_session_factory

from settings import settings
from cheesypi.urls import url_patterns
from cheesypi.handlers.hardware_io import (
    hardware_io_loop,
    HydrometerPooler,
    RelayController,
)
from cheesypi.models.base import Base


class TornadoApplication(tornado.web.Application):

    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)


def main(argv):
    tornado.options.parse_command_line(args=argv)
    session_factory = make_session_factory(options.dbname)
    Base.metadata.create_all(session_factory._engine)
    for HardwareIoClass in (HydrometerPooler, RelayController):
        tornado.ioloop.IOLoop.current().spawn_callback(hardware_io_loop, HardwareIoClass, session_factory)
    settings['session_factory'] = session_factory
    app = TornadoApplication()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main(sys.argv)
