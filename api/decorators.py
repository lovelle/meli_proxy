# -*- coding: utf-8 -*-
"""
    meli_proxy.api.decorators
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    decorators
"""

from functools import wraps
from flask import request, Response, jsonify, current_app as app

from dicttoxml import dicttoxml as xml

from .exceptions import MeliBadRequest, MeliNotImplemented


def dictify(fn):
    """This functions extends functionality to the format in the response"""
    def valid_format(fmt):
        return fmt in app.config.get('API_ALLOWED_FORMATS')

    def response(fmt, data):
        if fmt == "json":
            return jsonify(results=data)
        elif fmt == "xml":
            return Response(xml(data, root=True), mimetype='application/xml')
        else:
            raise MeliNotImplemented

    @wraps(fn)
    def decorated(*args, **kwargs):
        code = 200 if request.method == "GET" else 201
        fmt = kwargs.get('format', 'json')

        if not valid_format(fmt):
            raise MeliBadRequest("format %s is not supported" % fmt)

        data = fn(*args, **kwargs)
        return response(fmt, data), code

    return decorated
