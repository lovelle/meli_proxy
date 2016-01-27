# -*- coding: utf-8 -*-
"""
    meli_proxy.api.stats.statistics
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    basic struct for stats
"""

from flask import current_app as app


class Stats(object):

    def get_stats_key(self, node):
        return "meli:stats:%s_%s" % (app.server_name, node)

    def get_stats_global(self, by):
        return "requests_total_received" if by > 0 else "requests_total_processed"

    def get_stats_successful(self):
        return "requests_successful"

    def get_stats_requests_failed(self):
        return "requests_failed"

    def get_stats_http_errcode(self, code):
        return "requests_failed_http_%s" % (code)

    def get_stats_value_err(self):
        return "requests_failed_recv"

    def get_stats_generic_err(self):
        return "requests_failed_generic"

    def set_stats_global(self, node, r, by):
        r.hincrby(self.get_stats_key(node), self.get_stats_global(by), +1)

    def set_stats_successful(self, node, r):
        r.hincrby(self.get_stats_key(node), self.get_stats_successful(), +1)

    def set_stats_http_errcode(self, node, r, code):
        r.hincrby(self.get_stats_key(node), self.get_stats_requests_failed(), +1)
        r.hincrby(self.get_stats_key(node), self.get_stats_http_errcode(code), +1)

    def set_stats_value_err(self, node, r):
        r.hincrby(self.get_stats_key(node), self.get_stats_requests_failed(), +1)
        r.hincrby(self.get_stats_key(node), self.get_stats_value_err(), +1)

    def set_stats_generic_err(self, node, r):
        r.hincrby(self.get_stats_key(node), self.get_stats_requests_failed(), +1)
        r.hincrby(self.get_stats_key(node), self.get_stats_generic_err(), +1)
