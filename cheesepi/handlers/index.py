# -*- coding: utf-8 -*-

from .base import BaseHandler

class MainHandler(BaseHandler):

    # @tornado.web.authenticated
    def get(self):
        self.render('index.html', power_status=False, target_temperature=22, target_humidity=90)
