# -*- coding: utf-8 -*-
"""
    meli_proxy.api.core
    ~~~~~~~~~~~~~~~~~~~

    api core logic
"""

from flask import request, json, current_app as app
from flask.views import MethodView

from .lb.stateful import StateFul
from .http.request import HttpRequest

from .decorators import dictify
from .exceptions import (
    MeliError,
    MeliBadRequest,
    MeliNotImplemented,
    MeliServiceUnavailable
)


class MeliProxy(MethodView):

    decorators = [dictify]
    valid_methods = ("categories")

    def __init__(self):
        self.method = request.args if request.method == "GET" else request.post

    def get(self, init, query, format="json"):
        app.log.debug("received new request")

        if not query:
            raise MeliBadRequest

        lb = StateFul(request.remote_addr, query)

        if not lb.load_balance("categories", "*"):
            raise MeliServiceUnavailable("Service overloaded")

        r = HttpRequest(lb.node, init)

        # TODO: arreglar excepciones de clases

        try:
            r.send(query)
        #except MeliHttpErrorCode, e:
        #    raise e
        #except MeliHttpErrorValue, e:
        #    raise e
        #except MeliHttpErrorGeneric, e:
        #    raise e
        except MeliError, e:
            raise e

        #print lb.node
        return r.response

    def post(self):
        raise MeliNotImplemented

    def delete(self):
        raise MeliNotImplemented

    def __del__(self):
        pass
