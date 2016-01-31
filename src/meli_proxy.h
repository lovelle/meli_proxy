#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <curl/curl.h>
#include <kore/kore.h>
#include <kore/http.h>
#include <kore/tasks.h>
#include <hiredis/hiredis.h>

#define MELI_REDIS_ERROR	-1
#define MELI_LIMITS_IP_REACHED	-2

const char *SERVER = "MeliProxy1";
const char *BACKEND = "https://api.mercadolibre.com";

const long MAX_ACCESS_PER_IP = 100;

const int REDIS_PORT = 6379;
const char *REDIS_HOST = "127.0.0.1";
const struct timeval REDIS_TIMEOUT = { 1, 500000 }; // 1.5 seconds

const char *KEY_STATS = "meli:stats:MeliProxy1";
const char *KEY_ALLOW = "meli:allow";

int	send_http(struct kore_task *);
int	meli_proxy(struct http_request *);
int	meli_welcome(struct http_request *);
int	meli_not_found(struct http_request *);
size_t curl_write_cb(char *, size_t, size_t, void *);
void meli_proxy_stats(redisContext *, char *);
char *meli_fetch_addr(char *buf, size_t size, struct http_request *req);
long meli_fetch_addr_limits(redisContext *c, char *addr);

struct rstate {
	struct kore_task	task;
};
