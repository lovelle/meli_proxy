#include <curl/curl.h>
#include <kore/kore.h>
#include <kore/http.h>
#include <kore/tasks.h>

// const char *BACKEND = "http://127.0.0.1:8000/asdasd";
//const char *BACKEND = "https://api.mercadolibre.com";
const char *BACKEND = "https://api.mercadolibre.com/categories/MLA97994";

int	send_http(struct kore_task *);
int	meli_proxy(struct http_request *);
int	meli_welcome(struct http_request *);
int	meli_not_found(struct http_request *);
size_t	curl_write_cb(char *, size_t, size_t, void *);

struct rstate {
	struct kore_task	task;
};
