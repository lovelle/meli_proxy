# -*- coding: utf-8 -*-
"""
    meli_proxy.api.routing
    ~~~~~~~~~~~~~~~~~~~~~~

    config routing
"""

from .utils import url
from .core import MeliProxy


def make_map(app):
    GET = ['GET']
    GET_POST = ['GET', 'POST']
    meli_proxy = MeliProxy.as_view('meli')

    urldispatch = [
        url(app, '/stats', 'debug.stats', methods=GET, desc="DEBUG_0[stats info]"),
        url(app, '/routes', 'debug.routes', methods=GET, desc="DEBUG_1[routes info]"),
        # url(app, '/categories/<string:query>', meli_proxy, methods=GET_POST, desc="meli_proxy")
        url(app, '/<string:init>/<string:query>', meli_proxy, methods=GET_POST, desc="meli_proxy")
    ]

    return urldispatch
