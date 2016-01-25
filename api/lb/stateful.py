# -*- coding: utf-8 -*-
"""
    meli_proxy.api.lb.stateless
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    load balancer module in stateless mode
"""

import random

from flask import request, json, current_app as app

from ..exceptions import MeliBadRequest, MeliServiceUnavailable


class Lb(object):
    def __init__(self):
        self.r = self.__redis_connect()

    def __redis_connect(self):
        environ = "slave"# "master"

        with RedisHandler(app.config, environ=environ) as obj:
            if isinstance(obj, basestring):
                raise MeliServiceUnavailable(obj)
            else:
                return obj


class StateFul(Lb):
    def __init__(self, remote, query):
        self.rip = remote 
        self.qry = query

    def load_balance(self, gid, resource):
        #self.node = self.get_node_randomly()
        self.node = self.get_node_least_loaded(gid)
        return True

    def get_node_randomly(self):
        return random.choice(app.servers)

    def get_node_least_loaded(self, gid):
        """ Get the node who has less processing requests """
        return min(self.filer_enabled(gid), key=lambda x: x['load'])

    def filer_enabled(self, gid):
        """ Filter those nodes who are enabled and has proper gid """
        return [i for i in app.servers if bool(i.get('enabled')) is True and i.get('gid') == gid]
