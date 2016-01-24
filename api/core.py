# -*- coding: utf-8 -*-
"""
    meli_proxy.api.core
    ~~~~~~~~~~~~~~~~~~~

    api core logic
"""

from flask import request, json, current_app as app
from flask.views import MethodView

from .lb.stateless import StateLess

from .decorators import dictify
from .exceptions import (
    MeliBadRequest,
    MeliNotImplemented,
    MeliServiceUnavailable
)


class MeliProxy(MethodView):

    decorators = [dictify]

    def __init__(self):
        self.method = request.args if request.method == "GET" else request.post

    def get(self, query, format="json"):
        app.log.debug("received new request")

        if not query:
            raise MeliBadRequest

        lb = StateLess(request.remote_addr, query)

        if not lb.load_balance("1", "*"):
            raise MeliServiceUnavailable("Service overloaded")

        print lb.node

        return "WIP"

    def post(self):
        raise MeliNotImplemented

    def delete(self):
        raise MeliNotImplemented

    def __del__(self):
        pass
