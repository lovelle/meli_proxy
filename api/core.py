# -*- coding: utf-8 -*-
"""
    meli_proxy.api.core
    ~~~~~~~~~~~~~~~~~~~

    api core logic
"""

import requests

from flask import request, json, current_app as app
from flask.views import MethodView

from .lb.stateful import StateFul

from .decorators import dictify
from .exceptions import (
    MeliError,
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

        lb = StateFul(request.remote_addr, query)

        if not lb.load_balance("1", "*"):
            raise MeliServiceUnavailable("Service overloaded")

        r = SendRequest(lb.node)

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


class SendRequest(object):

    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }

    def __init__(self, node):
        self.uri = node["uri"]
        self.tout = node.get("tout", 10)

    def backend(self, query):
        return "%s/categories/%s" % (self.uri, query)

    def send(self, query):
        return self.__connect(query)

    def __connect(self, query):
        app.log.debug("request send: %s", query)

        try:
            r = requests.get(self.backend(query), verify=False,
                headers=self.headers, timeout=float(self.tout))
        except Exception, e:
            raise MeliError(e)
        else:
            return self.__response(r)

    def __response(self, r):
        if r.status_code != 200:
            raise MeliError("backend response is invalid code '%s'" % r.status_code)

        try:
            self.response = r.json()
        except ValueError, e:
            raise MeliError(e)

        # app.log.debug("request recv: %s", self.response)

        return self.response
