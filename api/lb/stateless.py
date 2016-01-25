# -*- coding: utf-8 -*-
"""
    meli_proxy.api.lb.stateless
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    load balancer module in stateless mode
"""

import random

from flask import request, json, current_app as app

# from .exceptions import MeliBadRequest


class StateLess(object):
    def __init__(self, remote, query):
        self.rip = remote 
        self.qry = query

    def load_balance(self, gid, resource):
        self.node = self.get_node_randomly()
        return True

    def get_node_randomly(self):
        return random.choice(app.servers)
