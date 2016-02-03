# -*- coding: utf-8 -*-
"""
    meli_proxy.api.utils
    ~~~~~~~~~~~~~~~~~~~~

    utilities for meli proxy api
"""

import sys
import redis
import logging

from .helpers import LazyView
from urlparse import urlparse


def setup_log_handlers(
        level='INFO', name='app', datefmt='%d-%m-%Y %H:%M:%S',
        chandle={'args': '(sys.stdout,)', 'class': 'StreamHandler'},
        formfmt='[%(asctime)s] [%(levelname)s:%(name)s]: %(message)s'):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        formatter = logging.Formatter(fmt=formfmt, datefmt=datefmt)
        handle = "logging." + chandle.get('class') + chandle.get('args')
        handler = eval(handle)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return (logger)


def url(app, url_rule, import_name, methods, desc):
    if hasattr(import_name, '__call__'):
        view = import_name
    else:
        view = LazyView("%s.%s" % ("api", import_name))

    app.add_url_rule(url_rule, view_func=view, methods=methods)
    app.add_url_rule(url_rule + ".<string(minlength=3, maxlength=4):format>",
                     view_func=view, methods=methods)
    return url_rule, methods, desc


def write_stderr(s, log=None):
    if not log:
        sys.stderr.write("[ERROR] %s" % s)
        sys.stderr.write("\n")
        sys.stderr.flush()
    else:
        log.error(s)
    sys.exit(1)


class RedisHandler(object):
    instances = {
        "master": {"host": "localhost", "port": 6379, "tout": 2},
        "slave": {"host": "localhost", "port": 6379, "tout": 2}
    }

    def __init__(self, myredis, environ=False):
        r = urlparse(myredis)
        self.password = r.password
        self.instances["master"]["host"] = r.hostname
        self.instances["master"]["port"] = int(r.port)
        self.instances["master"]["tout"] = 5
        self.instances["slave"]["host"] = r.hostname
        self.instances["slave"]["port"] = int(r.port)
        self.instances["slave"]["tout"] = 5
        self.environ = environ

    def __enter__(self):
        return self.std_connection() if self.environ is False else self.pool_connection()

    def std_connection(self):
        return (self.__connect(k) for k in self.instances.iterkeys())

    def pool_connection(self):
        return self.__connect(self.environ)

    def __connect(self, env):
        try:
            self.instances[env]["handler"] = redis.ConnectionPool(
                host=self.instances[env]["host"],
                port=self.instances[env]["port"],
                password=self.password,
                socket_timeout=self.instances[env]["tout"],
                db=0
            )
            r = redis.Redis(connection_pool=self.instances[env]["handler"])
            r.ping()
        except Exception, e:
            return str(e)
        else:
            return r

    def __exit__(self, *kwargs):
        [i["handler"].disconnect() for i in self.instances.values()
            if "handler" in i] if self.environ is False else None
