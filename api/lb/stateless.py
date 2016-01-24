# -*- coding: utf-8 -*-
"""
    meli_proxy.api.lb.stateless
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    load balancer module in stateless mode
"""

from flask import request, json, current_app as app

# from .logic.stateless import StateLess
# from .exceptions import MeliBadRequest


class StateLess(object):
    def __init__(self, remote, query):
        self.rip = remote 
        self.qry = query

    def load_balance(self, gid, resource):
        self.node = 2
        return True
