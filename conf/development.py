# -*- coding: utf-8 -*-
"""
    meli_proxy.conf.development.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    meli_proxy conf module
"""

#SERVER_NAME = 'https://api.mercadolibre.com'

SERVER = 'MeliProxy-007'
DEBUG = True
SECRET_KEY = 'super-secret-key'

# JSON_SORT_KEYS = False
API_ALLOWED_FORMATS = ('json', 'xml')

LOGGER_LEVEL = 'DEBUG'
LOGGER_NAME = 'meli_proxy'
LOGGER_FORMAT = "[%(asctime)s,%(msecs)03d] [%(levelname)s:%(name)s]: %(message)s"
LOGGER_DATE = "%d-%m-%Y %H:%M:%S"


LB_SERVERS = [
	#{"uid": 0, "gid": 1, "enabled": True, "uri": "https://127.0.0.1:9000", "resources": "*=100;", "load": 0},
	#{"uid": 1, "gid": 1, "enabled": True, "uri": "https://127.0.0.1:9001", "resources": "*=100;", "load": 0},
	#{"uid": 2, "gid": 1, "enabled": True, "uri": "https://127.0.0.1:9002", "resources": "*=100;", "load": 0},
	{"uid": 0, "gid": 1, "enabled": True, "uri": "https://api.mercadolibre.com", "resources": "*=100;", "load": 0}
]

# ip de origen o token para la restriccion por origen?