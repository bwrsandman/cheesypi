# -*- coding: utf-8 -*-

import tornado.web

from . import base


class PageNotFoundHandler(tornado.web.ErrorHandler, base.BaseHandler):

    def prepare(self):
        self.set_status(404)
        self.render_error()
