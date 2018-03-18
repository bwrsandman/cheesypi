#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Basic run script"""

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
from tornado.options import options
from tornado_sqlalchemy import make_session_factory

from settings import settings
from cheesypi.urls import url_patterns
from cheesypi.handlers import hardware_io
from cheesypi.models.base import Base


class TornadoApplication(tornado.web.Application):

    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)


def main():
    session_factory = make_session_factory(settings['dbname'])
    Base.metadata.create_all(session_factory._engine)
    tornado.ioloop.IOLoop.current().spawn_callback(hardware_io.hydrometer_pooling_timer, session_factory)
    settings['session_factory'] = session_factory
    app = TornadoApplication()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
