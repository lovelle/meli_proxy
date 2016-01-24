# -*- coding: utf-8 -*-
"""
    meli_proxy.exceptions
    ~~~~~~~~~~~~~~~~~~~~~

    exceptions module
"""

from flask import current_app as app


class ExceptionError(Exception):
    def __init__(self, e):
        app.log.error(e)


class MeliNotImplemented(Exception):
    def __init__(self):
        pass


class MeliUnauthorized(Exception):
    def __init__(self, msg="Sorry, you are not authorized"):
        super(MeliUnauthorized, self).__init__(msg)
        self.msg = msg


class MeliForbidden(Exception):
    def __init__(self, msg="Sorry, forbidden to see this"):
        super(MeliForbidden, self).__init__(msg)
        self.msg = msg


class MeliBadRequest(Exception):
    def __init__(self, msg="MeliBadRequest exception raised"):
        super(MeliBadRequest, self).__init__(msg)
        self.msg = msg


class MeliError(ExceptionError):
    def __init__(self, msg="MeliError exception raised"):
        super(MeliError, self).__init__(msg)
        self.msg = msg


class MeliServiceUnavailable(ExceptionError):
    def __init__(self, msg="MeliServiceUnavailable exception raised"):
        super(MeliServiceUnavailable, self).__init__(msg)
        self.msg = msg


class MeliDataNotFound(Exception):
    def __init__(self, msg="MeliDataNotFound exception raised"):
        super(MeliDataNotFound, self).__init__(msg)
        self.msg = msg
