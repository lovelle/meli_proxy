meli_proxy
===
Meli Proxy - incoming data handler

Python implementation
---

Features
----
        * Load balance against multiple nodes in stateful mode
        * Xml returning format (could be specified in the request, deafult format is json)

        WIP:
        * Stats
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
