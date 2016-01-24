# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~

    meli_proxy wsgi initialization
"""

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from gevent.wsgi import WSGIServer

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from api import middleware as meli_proxy

HOST = "0.0.0.0"
PORT = 8000

application = DispatcherMiddleware(meli_proxy.make_app())


def run_tornado():
    http_server = HTTPServer(WSGIContainer(application))
    http_server.listen(PORT)
    IOLoop.instance().start()


def run_gevent():
    http_server = WSGIServer((HOST, PORT), application)
    http_server.serve_forever()


def run_werkzeug():
	run_simple(HOST, PORT, application, use_reloader=True, use_debugger=True)


if __name__ == "__main__":
    run_werkzeug()


# venv/bin/gunicorn wsgi -c conf/gunicorn.py
# venv/bin/uwsgi --http-socket 0.0.0.0:8000 -w wsgi # --ini conf/uwsgi.ini
