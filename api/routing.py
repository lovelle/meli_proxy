# -*- coding: utf-8 -*-
"""
    meli_proxy.api.routing
    ~~~~~~~~~~~~~~~~~~~~~~

    config routing
"""

from .utils import url
from .core import MeliProxy


def make_map(app):
    GET_POST = ['GET', 'POST']
    meli_proxy = MeliProxy.as_view('meli')

    urldispatch = [
        url(app, '/', meli_proxy, methods=GET_POST, desc="meli_proxy")
    ]

    #if app.config['DEBUG']:
    urldispatch.append(url(app, '/info', 'api.stats.info', methods=GET_POST, desc="DEBUG_1[stats info]"))

    return urldispatch
