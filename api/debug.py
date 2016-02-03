# -*- coding: utf-8 -*-
"""
    meli_proxy.api.debug
    ~~~~~~~~~~~~~~~~~~~~

    api debug info
"""

from .decorators import dictify
from .exceptions import MeliForbidden
from .utils import RedisHandler
from .lb.lb import Lb

from flask import jsonify, current_app as app


def routes():
    return jsonify(
        ((i[2], i[0]) for i in app.url_routes)
    )

@dictify
def stats():
    l = Lb()
    r = {}

    for i in l.r_m.smembers(app.redis_key_nodes):
        k = l.get_stats_key(i)
        r[k.split(":")[2]] = l.r_m.hgetall(k)

    return r
