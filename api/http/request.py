# -*- coding: utf-8 -*-
"""
    meli_proxy.api.http.request
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    http client lib
"""

import requests

from flask import json, current_app as app

from ..exceptions import MeliError
from ..lb.stateful import Lb


class HttpRequest(Lb):

    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }

    def __init__(self, node, branch):
        super(HttpRequest, self).__init__()
        self.uri = node["uri"]
        self.tout = node.get("tout", 10)
        self.node = node
        self.server = node["server"]
        self.branch = branch

    def __backend(self, query):
        return "%s/%s/%s" % (self.uri, self.branch, query)

    def send(self, query):
        return self.__connect(query)

    def __connect(self, query):
        app.log.debug("sending request: %s to: %s", query, self.server)

        try:
            r = requests.get(self.__backend(query), verify=False,
                headers=self.headers, timeout=float(self.tout))
        except Exception, e:
            self.set_stats_generic_err(self.server, self.r_m)
            raise MeliHttpErrorGeneric(e)
        else:
            return self.__response(r)

    def __response(self, r):
        if r.status_code != 200:
            self.set_stats_http_errcode(self.server, self.r_m, r.status_code)
            raise MeliError("backend response is invalid code '%s'" % r.status_code)

        try:
            self.response = r.json()
        except ValueError, e:
            self.set_stats_value_err(self.server, self.r_m)
            raise MeliHttpErrorValue(e)

        # app.log.debug("request recv: %s", self.response)

        self.set_stats_successful(self.server, self.r_m)
        return self.response
