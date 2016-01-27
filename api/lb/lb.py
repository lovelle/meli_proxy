# -*- coding: utf-8 -*-
"""
    meli_proxy.api.lb.lb
    ~~~~~~~~~~~~~~~~~~~~

    load balancer basic module
"""

from flask import current_app as app

from ..utils import RedisHandler
from ..exceptions import MeliServiceUnavailable
from ..stats.statistics import Stats


class Lb(Stats):
    def __init__(self):
        super(Lb, self).__init__()
        self.r_m = self.redis_connect("master")

    def redis_connect(self, environ="slave"):
        with RedisHandler(app.config, environ=environ) as obj:
            if isinstance(obj, basestring):
                raise MeliServiceUnavailable(obj)
            else:
                return obj
