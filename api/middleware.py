# -*- coding: utf-8 -*-
"""
    meli_proxy.api.middleware
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    middleware initialization
"""

from .environment import load_app
from .routing import make_map
from .helpers import JSONEncoder, HandleRequest, HandleErrors
from .exceptions import (
    MeliError,
    MeliForbidden,
    MeliBadRequest,
    MeliDataNotFound,
    MeliUnauthorized,
    MeliNotImplemented,
    MeliServiceUnavailable,
)


def make_app(settings_override=None, register_security_blueprint=False):
    app = load_app(__name__, 'path', settings_override,
                   register_security_blueprint=register_security_blueprint)

    r = HandleRequest()
    e = HandleErrors()

    # Set the default JSON encoder
    app.json_encoder = JSONEncoder

    # Register custom error handlers
    app.errorhandler(400)(e.on_meli_proxy_bad_request)
    app.errorhandler(401)(e.on_meli_proxy_unauthorized)
    app.errorhandler(403)(e.on_forbidden)
    app.errorhandler(404)(e.on_not_found)
    app.errorhandler(405)(e.on_method_not_allowed)
    app.errorhandler(408)(e.on_request_timeout)
    app.errorhandler(415)(e.on_unsupported_media_type)
    app.errorhandler(500)(e.on_internal_error)
    app.errorhandler(501)(e.on_not_implemented)
    app.errorhandler(502)(e.on_bad_gateway)
    app.errorhandler(503)(e.on_service_unavailable)
    app.errorhandler(MeliForbidden)(e.on_forbidden)
    app.errorhandler(MeliError)(e.on_meli_proxy_generic_error)
    app.errorhandler(MeliDataNotFound)(e.on_data_not_found)
    app.errorhandler(MeliBadRequest)(e.on_meli_proxy_bad_request)
    app.errorhandler(MeliNotImplemented)(e.on_not_implemented)
    app.errorhandler(MeliUnauthorized)(e.on_meli_proxy_unauthorized)
    app.errorhandler(MeliServiceUnavailable)(e.on_service_unavailable)

    # Register special featueres over initial and finished request
    app.after_request_funcs.setdefault(None, [r.set_headers, r.run_after])
    app.before_request_funcs.setdefault(None, [r.run_before])

    # Url mapping
    # create list of available routes
    # also availabe in url_map as class instance of werkzeug.routing.Map
    app.url_routes = make_map(app)

    return app
