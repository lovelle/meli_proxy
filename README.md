meli_proxy
===
Meli Proxy - incoming data handler

Python implementation
---

Features
----
        * 1 [Load balance](#1-load-balance) against multiple nodes in stateful mode.
        * 2 [Xml](#2-handling-returning-format) returning format.
        * 3 [Stats](#3-statistics).

        WIP:
        * Max requests per ip origin

Installation (in dev environment)
----
        # Dependences for python debian/ubuntu support
        $ aptitude install python-pip python-virtualenv python-dev
        # Build lib dependences
        $ make

Configuration
----

        # Set custom params
        $ editor conf/development.py
        # set config var with path of environment
        $ export CONFIG_FILE=/usr/src/meli_proxy/conf/development.py

Run
----
        # Run server (use this command just for dev environ)
        $ venv/bin/python -u wsgi.py
        # Deploy with uwsgi
        $ venv/bin/uwsgi -w wsgi --ini conf/uwsgi.ini
        # Deploy with gunicorn
        $ venv/bin/gunicorn wsgi -c conf/gunicorn.py

Doc
----

1. Load balance
-------

The idea si to send requests across multiple nodes.

Abilities:
----------

        * Grouping nodes by `group id`.
        * Disable or enable nodes by parameter: `enabled = False|True`.
        * Tracking load of each node in order to do load balance.
        * Centralized data in redis db.

Example of servers data struct:

```
[
        {"uid": 0, "gid": "categories", "enabled": True, "uri": "https://api.mercadolibre.com", "load": 0},
        {"uid": 1, "gid": "categories", "enabled": True, "uri": "https://api.mercadolibre.com", "load": 0},
]
```

2. Handling returning format
-------

You can specify any format you want, or `xml` or `json`.
By default, if you don't specify any returning type, the default will be `json`.

Example for xml: `$ curl http://127.0.0.1:8000/categories/MLA97994.xml`.
Example for json: `$ curl http://127.0.0.1:8000/categories/MLA97994`.
Other json example: `$ curl http://127.0.0.1:8000/categories/MLA97994.json`.


3. Statistics
-------
