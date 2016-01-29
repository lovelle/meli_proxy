
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
	char 	url[strlen(BACKEND)+strlen(req->path)+1];

	if (req->hdlr_extra == NULL) {

		state = kore_malloc(sizeof(*state));
		req->hdlr_extra = state;

		kore_task_create(&state->task, send_http);
		kore_task_bind_request(&state->task, req);

		strcpy(url, BACKEND);
		strcat(url, req->path);

		/* Start the task */
		kore_task_run(&state->task);
		/* write specify path */
		kore_task_channel_write(&state->task, req->path, strlen(req->path));
		/* write complete url */
		kore_task_channel_write(&state->task, url, strlen(url));

		/* Tell Kore to retry us later */
		return (KORE_RESULT_RETRY);
	} else {
		state = req->hdlr_extra;
	}

	if (kore_task_state(&state->task) != KORE_TASK_STATE_FINISHED) {
		http_request_sleep(req);
		return (KORE_RESULT_RETRY);
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
		http_response_header(req, "Content-Type", ct);
		http_response(req, 200, result, len);
	}

	/* destroy the task */
	kore_task_destroy(&state->task);

	return (KORE_RESULT_OK);
}


int send_http(struct kore_task *t) {
	struct kore_buf	*b;
	u_int32_t		len;
	CURLcode		res;
	u_int8_t		*data;
	CURL			*curl;
	char			*ct;
	char 			path[64];
	char 			url[128];

	/* Read request path */
	kore_task_channel_read(t, path, sizeof(path));
	/* Read request url */
	kore_task_channel_read(t, url, sizeof(url));

	kore_log(LOG_NOTICE, "connecting to: %s", url);

	if ((curl = curl_easy_init()) == NULL)
		return (KORE_RESULT_ERROR);

	b = kore_buf_create(128);
	kore_log(LOG_NOTICE, "sending request: %s", path);

	curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
	curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
	curl_easy_setopt(curl, CURLOPT_URL, url);
	curl_easy_setopt(curl, CURLOPT_WRITEDATA, b);
	curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, curl_write_cb);

	res = curl_easy_perform(curl);
	if (res != CURLE_OK) {
		kore_log(LOG_ERR, "request failed: %s", curl_easy_strerror(res));
		kore_buf_free(b);
		return (KORE_RESULT_ERROR);
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

	kore_mem_free(data);

	/* always cleanup */ 
	curl_easy_cleanup(curl);

	return (KORE_RESULT_OK);
}

size_t curl_write_cb(char *ptr, size_t size, size_t nmemb, void *udata) {
	struct kore_buf		*b = udata;

	kore_buf_append(b, ptr, size * nmemb);
	return (size * nmemb);
}
