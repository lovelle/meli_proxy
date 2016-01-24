# -*- coding: utf-8 -*-
"""
    meli_proxy.api.stats
    ~~~~~~~~~~~~~~~~~~~~

    api stats info
"""

from .decorators import dictify
from .exceptions import MeliForbidden
from flask import (
    request,
    jsonify,
    current_app as app
)


def routes():
    return jsonify(
        ((i[2], i[0]) for i in app.url_routes)
    )

@dictify
def info():
    return app.statics
