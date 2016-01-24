# -*- coding: utf-8 -*-
"""
    meli_proxy.api.core
    ~~~~~~~~~~~~~~~~~~~

    api core logic
"""

import os

from flask import request, json, current_app as app
from flask.views import MethodView

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

    def get(self, format="json"):
        app.log.debug("received new request")
        return "WIP"

    def post(self):
        raise MeliNotImplemented

    def delete(self):
        raise MeliNotImplemented

    def __del__(self):
        pass
