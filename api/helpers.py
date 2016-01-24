# -*- coding: utf-8 -*-
"""
    meli_proxy.api.helpers
    ~~~~~~~~~~~~~~~~~~~~~~

    helpers module
"""

import time

from flask import jsonify, request, current_app as app
from flask.json import JSONEncoder as BaseJSONEncoder
from werkzeug import import_string, cached_property


class JSONEncoder(BaseJSONEncoder):
    """Custom :class:`JSONEncoder` which respects objects that include the
    :class:`JsonSerializer` mixin.
    """
    def default(self, obj):
        #if isinstance(obj, JsonSerializer):
        #    return obj.to_json()
        return super(JSONEncoder, self).default(obj)

"""
class JsonSerializer(object):
    A mixin that can be used to mark a SQLAlchemy model class which
    implements a :func:`to_json` method. The :func:`to_json` method is used
    in conjuction with the custom :class:`JSONEncoder` class. By default this
    mixin will assume all properties of the SQLAlchemy model are to be visible
    in the JSON output. Extend this class to customize which properties are
    public, hidden or modified before being being passed to the JSON serializer.


    __json_public__ = None
    __json_hidden__ = None
    __json_modifiers__ = None

    def get_field_names(self):
        for p in self.__mapper__.iterate_properties:
            yield p.key

    def to_json(self):
        field_names = self.get_field_names()

        public = self.__json_public__ or field_names
        hidden = self.__json_hidden__ or []
        modifiers = self.__json_modifiers__ or dict()

        rv = dict()
        for key in public:
            rv[key] = getattr(self, key)
        for key, modifier in modifiers.items():
            value = getattr(self, key)
            rv[key] = modifier(value, self)
        for key in hidden:
            rv.pop(key, None)
        return rv
"""


class LazyView(object):
    """This method is from flask documentation, 
    with a little touch by myself"""

    def __init__(self, import_name):
        print import_name
        self.__module__, self.__name__ = import_name.rsplit('.', 1)
        self.import_name = import_name

    @cached_property
    def view(self):
        return import_string(self.import_name)

    def __call__(self, *args, **kwargs):
        return self.view(*args, **kwargs)


class HandleRequest(object):

    def __init__(self):
        super(HandleRequest, self).__init__()
        self.st_timer = None
        self.end_timer = None

    def set_headers(self, response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['X-Server'] = 'MeliProxy'
        response.headers['X-Response-Time'] = '%.3f' % self.end_timer
        return response

    def run_after(self, response):
        self.end_timer = time.time() - self.st_timer

        if self.end_timer > 10:
            app.log.warn("Api requests at '%s' was served too slowly!" % request.path)

        app.log.info("'%s' render time %.3f seconds" % (request.path, self.end_timer))
        return response

    def run_before(self):
        self.st_timer = time.time()


class HandleErrors(object):

    def __init__(self):
        super(HandleErrors, self).__init__()

    def on_meli_proxy_bad_request(self, e):
        return self.common(400, e)

    def on_meli_proxy_generic_error(self, e):
        return self.critic(400, e)

    def on_meli_proxy_unauthorized(self, e):
        return self.common(401, e)

    def on_forbidden(self, e):
        return self.common(403, e)

    def on_data_not_found(self, e):
        return self.common(404, e)

    def on_not_found(self, e):
        return self.common(404, "Sorry, request not found")

    def on_method_not_allowed(self, e):
        return self.common(405, "Sorry, method not allowed")

    def on_request_timeout(self, e):
        return self.critic(408, "Sorry, your request timed out")

    def on_unsupported_media_type(self, e):
        return self.common(415, "Sorry, the only supported media type is application/json")

    def on_internal_error(self, e):
        return self.critic(500, "Sorry, internal server error")

    def on_not_implemented(self, e):
        return self.common(501, "Sorry, the method you requested is not allready implemented")

    def on_bad_gateway(self, e):
        return self.critic(502, e)

    def on_service_unavailable(self, e):
        return self.critic(503, "Sorry, the service is not available")

    def common(self, code, e):
        return jsonify(message=self._parse(e)), code

    def critic(self, code, e):
        app.log.error("Api return response '%s'" % code)
        return jsonify(message=self._parse(e)), code

    def _parse(self, e):
        if isinstance(e, str):
            return e
        elif hasattr(e, '__class__'):
            return str(e)
