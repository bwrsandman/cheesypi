# -*- coding: utf-8 -*-

import traceback
import tornado.web

import pygments
from pygments.lexers.python import Python3TracebackLexer
from pygments.formatters import HtmlFormatter


class BaseHandler(tornado.web.RequestHandler):
    """
    Base handler gonna to be used instead of RequestHandler
    """
    def render_error(self, exc_info="", *args, **kwargs):
        self.render(
            "%d.html" % self._status_code,
            error_code=self._status_code,
            error_message=self._reason,
            exc_info=pygments.highlight(exc_info, Python3TracebackLexer(), HtmlFormatter()),
            *args,
            **kwargs
        )

    def write_error(self, status_code, **kwargs):
        """Overridden to implement custom error pages.

            ``write_error`` may call `write`, `render`, `set_header`, etc
            to produce output as usual.

            If this error was caused by an uncaught exception (including
            HTTPError), an ``exc_info`` triple will be available as
            ``kwargs["exc_info"]``.  Note that this exception may not be
            the "current" exception for purposes of methods like
            ``sys.exc_info()`` or ``traceback.format_exc``.
        """
        if status_code in [404, 500]:
            self.render_error(
                exc_info="".join(traceback.format_exception(*kwargs["exc_info"]))
                if self.settings.get("serve_traceback")
                else ""
            )
        else:
            self.finish("<html><title>%(code)d: %(message)s</title>"
                        "<body>%(code)d: %(message)s</body></html>" % {
                            "code": status_code,
                            "message": self._reason,
                        })
