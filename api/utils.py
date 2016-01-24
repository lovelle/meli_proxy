# -*- coding: utf-8 -*-
"""
    meli_proxy.api.utils
    ~~~~~~~~~~~~~~~~~~~~

    utilities for meli proxy api
"""

import sys
import logging

from .helpers import LazyView


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