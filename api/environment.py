# -*- coding: utf-8 -*-
"""
    meli_proxy.api.environment
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    load environment config data
"""

import os
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from .utils import write_stderr, setup_log_handlers, RedisHandler


def load_app(app_name, settings_override):
    conf_file = os.environ.get('CONFIG_FILE')

    app = Flask(app_name, instance_relative_config=True)

    app.config.from_envvar('CONFIG_FILE') if conf_file \
        else write_stderr("CONFIG_FILE environ varibale is not set")

    app.config.from_object(settings_override)
    app.log = setup_log_handlers(
        level=app.config.get("LOGGER_LEVEL"),
        name=app.config.get("LOGGER_NAME"),
        datefmt=app.config.get("LOGGER_DATE"),
        formfmt=app.config.get("LOGGER_FORMAT")
    )

    # Check if all redis instances configured are running
    with RedisHandler(app.config) as obj:
        [write_stderr(i, app.log) for i in obj if isinstance(i, basestring)]

    """
    app.statics = {}
    basic_stats = {
        'request_slower': 0.0,
        'request_faster': 0.0,
        'requests_failed': 0,
        'requests_successful': 0,
        'requests_total_processed': 0,
        'requests_total_received': 0,
    }
    """

    app.servers = app.config.get('LB_SERVERS')
    app.redis_key_nodes = app.config.get('REDIS_KEY_SERVERS')

    """
    for i in app.servers:
        server = "%s|%s" % (app.config.get('SERVER'), i.get('uid'))
        app.statics[server] = basic_stats
    """

    app.wsgi_app = ProxyFix(app.wsgi_app)

    return app
