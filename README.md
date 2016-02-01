meli_proxy
===
Meli Proxy - incoming data handler

C implementation
---

Using [Kore](https://github.com/jorisvink/kore)

Compiled with NOTLS=1 and TASKS=1


Installation
----

1. Install Linux deps (curl dev files and redis dev files)

	$ aptitude install libcurl-dev libhiredis-dev libevent-pthreads-2.0-5

2. Install [Kore](https://github.com/jorisvink/kore#building-kore) with proper env variables

	$ git clone https://github.com/jorisvink/kore
	$ cd kore
	$ export NOTLS=1 TASKS=1
	$ make; make install

3. Install meli_proxy

	$ git clone https://github.com/lovelle/meli_proxy.git
	$ cd meli_proxy
	$ git checkout c
	$ kore build

Configure and start the server
----
    $ cd meli_proxy
    # Adjust listen address
    $ editor conf/meli_proxy.conf
    # Run!
    $ kore run

Doc
----

1. Stats

For stats data is stored into redis database with Hash set for data structure.

Example for stats:

```
127.0.0.1:6379> hgetall meli:stats:MeliProxy1
1) "requests_total_received"
2) "5"
3) "requests_total_processed"
4) "5"
5) "requests_failed_http_404"
6) "2"
7) "requests_successful"
8) "5"
```


2. Allow module

Allow module also uses hash set for data struct.

But the key, is created for ip received.

Example:

```
127.0.0.1:6379> hgetall meli:allow:192.168.0.30
1) "requests"
2) "15"
3) "/categories/MLA97994"
4) "14"
5) "/categories/MLA97993"
6) "1"

```

The general rules defining the behaviour of the allow module,
uses constant variables in file `src/meli_proxy.h`

Example:
```c
const long MAX_ACCESS_PER_IP = 100;
const long MAX_ACCESS_PER_PATH = 5;
```
