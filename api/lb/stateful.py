# -*- coding: utf-8 -*-
"""
    meli_proxy.api.lb.stateful
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    load balancer module in stateful mode
"""

import random

from flask import current_app as app

from .lb import Lb


class StateFul(Lb):
    def __init__(self, remote, query):
        super(StateFul, self).__init__()
        self.rip = remote 
        self.qry = query
        self.r_s = self.redis_connect()

    def load_balance(self, gid, resource):
        # self.node = self.get_node_randomly()
        self.node = self.get_node_least_loaded(gid)

        if self.node:
            self.set_incr_node(+1)
            return True

    def set_incr_node(self, by):
        self.r_m.hincrby(self.node["server"], "load", by)
        self.set_stats_global(self.node["server"], self.r_m, by)

    def get_server_nodes(self):
        # return app.servers
        return [dict(self.r_s.hgetall(i), **{"server": i}) for i in self.r_s.smembers(app.redis_key_nodes)]

    def get_node_randomly(self):
        return random.choice(self.get_server_nodes())

    def get_node_least_loaded(self, gid):
        """ Get the node who has less processing requests """
        return min(self.filer_enabled(gid), key=lambda x: x['load'])

    def filer_enabled(self, gid):
        """ Filter those nodes who are enabled and has proper gid """
        return [i for i in self.get_server_nodes() if bool(i.get('enabled')) is True and i.get('gid') == gid]

    def __del__(self):
        return self.set_incr_node(-1) if self.node else None
