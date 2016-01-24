# -*- coding: utf-8 -*-
"""
    meli_proxy.api.stats
    ~~~~~~~~~~~~~~~~~~~~

    api stats info
"""

from flask import (
    request,
    jsonify,
    render_template,
    current_app as app
)


def routes():
    return jsonify(
        ((i[2], i[0]) for i in app.url_routes)
    )

def info():
    return "info"
