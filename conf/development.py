# -*- coding: utf-8 -*-
"""
    meli_proxy.conf.development.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    meli_proxy conf module
"""

#SERVER_NAME = 'https://api.mercadolibre.com'

DEBUG = True
SECRET_KEY = 'super-secret-key'

# JSON_SORT_KEYS = False
API_ALLOWED_FORMATS = ('json', 'xml')

LOGGER_LEVEL = 'DEBUG'
LOGGER_NAME = 'meli_proxy'
LOGGER_FORMAT = "[%(asctime)s,%(msecs)03d] [%(levelname)s:%(name)s]: %(message)s"
LOGGER_DATE = "%d-%m-%Y %H:%M:%S"


# ip de origen o token para la restriccion por origen?