
/*
 * An easy to use, scalable and secure web 
 * application framework for writing web APIs in C
 * 
 * https://kore.io
 * https://github.com/jorisvink/kore
 */

#include <meli_proxy.h>


int meli_not_found(struct http_request *req) {
	char *err = "Not found";
	http_response(req, 404, err, strlen(err));
	return (KORE_RESULT_OK);
}


int meli_welcome(struct http_request *req) {
	char *hello = "Bienvenido a meli proxy ;)";
	http_response(req, 200, hello, strlen(hello));
	return (KORE_RESULT_OK);
}


int meli_proxy(struct http_request *req) {
	u_int32_t	len;
	struct rstate	*state;
	char	ct[64], result[2048];
	char	url[strlen(BACKEND)+strlen(req->path)+1];
	char	addr[INET6_ADDRSTRLEN], time_taken[8];
	u_int16_t	time_req = req->total;

	if (req->hdlr_extra == NULL) {

		state = kore_malloc(sizeof(*state));
		req->hdlr_extra = state;

		kore_task_create(&state->task, send_http);
		kore_task_bind_request(&state->task, req);

		strcpy(url, BACKEND);
		strcat(url, req->path);

		meli_fetch_addr(addr, sizeof(addr), req);

		/* Start the task */
		kore_task_run(&state->task);
		/* write specify path */
		kore_task_channel_write(&state->task, req->path, strlen(req->path));
		/* write complete url */
		kore_task_channel_write(&state->task, url, strlen(url));
		/* write request ip */
		kore_task_channel_write(&state->task, addr, strlen(addr));

		/* Tell Kore to retry us later */
		return (KORE_RESULT_RETRY);
	} else {
		state = req->hdlr_extra;
	}

	if (kore_task_state(&state->task) != KORE_TASK_STATE_FINISHED) {
		http_request_sleep(req);
		return (KORE_RESULT_RETRY);
	}

	if (kore_task_result(&state->task) == MELI_REDIS_ERROR) {
		kore_task_destroy(&state->task);
		http_response(req, 500, "Connection error to redis", 25);
		return (KORE_RESULT_OK);
	}

	/* Task is finished, check the result */
	if (kore_task_result(&state->task) != KORE_RESULT_OK) {
		kore_task_destroy(&state->task);
		http_response(req, 500, "could not send request", 22);
		return (KORE_RESULT_OK);
	}

	len = kore_task_channel_read(&state->task, result, sizeof(result));
	kore_task_channel_read(&state->task, ct, sizeof(ct));
	
	if (len > sizeof(result)) {
		http_response(req, 500, "response length mismatch", 24);
	} else {
		snprintf(time_taken, sizeof(time_taken), "%dms", time_req);
		http_response_header(req, "Content-Type", ct);
		http_response_header(req, "X-Server", SERVER);
		http_response_header(req, "X-Response-Time", time_taken);
		http_response(req, 200, result, len);
	}

	/* destroy the task */
	kore_task_destroy(&state->task);

	return (KORE_RESULT_OK);
}


int send_http(struct kore_task *t) {
	redisContext	*c;
	struct kore_buf	*b;
	u_int32_t		len;
	CURLcode		res;
	u_int8_t		*data;
	CURL			*curl;
	char			*ct, path[64], url[128], addr[INET6_ADDRSTRLEN], http_key_code[32];
	long			http_code = 0;

	c = redisConnectWithTimeout(REDIS_HOST, REDIS_PORT, REDIS_TIMEOUT);

	/* Read request path */
	kore_task_channel_read(t, path, sizeof(path));
	/* Read request url */
	kore_task_channel_read(t, url, sizeof(url));
	/* Read request addr */
	kore_task_channel_read(t, addr, sizeof(addr));

	if (c == NULL || c->err) {
		if (c) {
			kore_log(LOG_ERR, "Connection error: %s", c->errstr);
			redisFree(c);
		} else {
			kore_log(LOG_ERR, "Connection error: can't allocate redis context");
		}
		return (MELI_REDIS_ERROR);
	}

	meli_proxy_stats(c, "requests_total_received");

	kore_log(LOG_NOTICE, "connecting to: %s", url);

	if ((curl = curl_easy_init()) == NULL) {
		meli_proxy_stats(c, "requests_failed");
		return (KORE_RESULT_ERROR);
	}

	b = kore_buf_create(128);
	kore_log(LOG_NOTICE, "sending request: %s", path);

	curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
	curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
	curl_easy_setopt(curl, CURLOPT_URL, url);
	curl_easy_setopt(curl, CURLOPT_WRITEDATA, b);
	curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, curl_write_cb);

	meli_proxy_stats(c, "requests_total_processed");

	res = curl_easy_perform(curl);
	if (res != CURLE_OK) {
		kore_log(LOG_ERR, "request failed: %s", curl_easy_strerror(res));
		meli_proxy_stats(c, "requests_failed");
		kore_buf_free(b);
		return (KORE_RESULT_ERROR);
	} else {
		curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &http_code);
	}

	if (http_code != 200) {
		snprintf(http_key_code, sizeof(http_key_code), "requests_failed_http_%lu", http_code);
		meli_proxy_stats(c, http_key_code);
	}

	kore_log(LOG_NOTICE, "recevied request");

	/* Save received Content Type to bypass it */
	res = curl_easy_getinfo(curl, CURLINFO_CONTENT_TYPE, &ct);

	/*
	 * Grab the response from the CURL request and write the
	 * result back to the task channel.
	 */
	data = kore_buf_release(b, &len);

	/* Grab data */
	kore_task_channel_write(t, data, len);

	/* Grab content type */
	kore_task_channel_write(t, ct, strlen(ct));

	/* Free data */
	kore_mem_free(data);

	/* always cleanup */
	curl_easy_cleanup(curl);

	meli_proxy_stats(c, "requests_successful");

	/* Disconnects and frees the context */
	redisFree(c);

	return (KORE_RESULT_OK);
}

size_t curl_write_cb(char *ptr, size_t size, size_t nmemb, void *udata) {
	struct kore_buf		*b = udata;

	kore_buf_append(b, ptr, size * nmemb);
	return (size * nmemb);
}

void meli_proxy_stats(redisContext *c, char *type) {
	redisReply *reply;
	reply = redisCommand(c,"HINCRBY %s %s 1", KEY_STATS, type);
	freeReplyObject(reply);
}

char *meli_fetch_addr(char *buf, size_t size, struct http_request *req) {
	char addr[size];

	/* Set type of address */
	if (req->owner->addrtype == AF_INET) {
		memcpy(addr, &(req->owner->addr.ipv4.sin_addr),
			sizeof(req->owner->addr.ipv4.sin_addr));
	} else {
		memcpy(addr, &(req->owner->addr.ipv6.sin6_addr),
			sizeof(req->owner->addr.ipv6.sin6_addr));
	}

	if (inet_ntop(req->owner->addrtype, &(addr), buf, size) == NULL)
			kore_strlcpy(buf, "unknown", size);

	return buf;
}