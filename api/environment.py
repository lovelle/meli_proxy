# -*- coding: utf-8 -*-
"""
    meli_proxy.api.environment
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    load environment config data
"""

import os
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from .utils import write_stderr, setup_log_handlers


def load_app(app_name, app_path, settings_override, register_security_blueprint):
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

    app.wsgi_app = ProxyFix(app.wsgi_app)

    return app
