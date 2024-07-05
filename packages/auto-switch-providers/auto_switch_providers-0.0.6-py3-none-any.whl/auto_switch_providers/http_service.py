from json import dumps, loads
from urllib.parse import urlencode
import requests

from .cache_service import CacheService
from .utils.helpers import base64encode


class HttpService(object):
    def __init__(
        self,
        config=None,
        cache_config=None,
        base_url: str = None,
        default_headers=None,
        endpoints=None,
    ) -> None:
        self.config = config
        self.base_url = base_url if base_url is not None else ""
        self.default_headers = default_headers if default_headers is not None else {}
        self.endpoints = endpoints if endpoints is not None else {}
        self.cache_service = None

        if cache_config is not None:
            self.cache_service = CacheService(cache_config)

    def _request(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict = None,
        body: dict = None,
        headers: dict = None,
        timeout=10,
        url_params_format=None,
    ):
        endpoint = self.endpoints.get(endpoint) or endpoint
        if url_params_format:
            endpoint = endpoint.format(**url_params_format)
        headers = (
            {**self.default_headers, **headers} if headers else self.default_headers
        )
        url = self.base_url + (endpoint or "/")
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=body,
            timeout=timeout,
        )
        return response

    def request(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict = None,
        body: dict = None,
        headers: dict = None,
        timeout=10,
        status_force_list=None,
        total=3,
        url_params_format=None,
    ):
        if status_force_list is None:
            status_force_list = []

        endpoint = self.endpoints.get(endpoint) or endpoint
        if url_params_format:
            endpoint = endpoint.format(**url_params_format)

        params_str = " - " + dumps(params) if params else ""
        cache_url_query = urlencode(params or {})
        if cache_url_query != "":
            cache_url_query = f"?{cache_url_query}"

        for _ in range(total):
            try:
                log_endpoint = self.base_url + (endpoint or "/")

                # Check exists in cache
                if self.cache_service is not None:
                    cache_params = {}

                    if params:
                        cache_params = {**cache_params, **params}
                    if body:
                        cache_params = {**cache_params, **body}
                    if headers:
                        cache_params = {**cache_params, **headers}

                    if "api_key" in cache_params:
                        cache_params.pop("api_key")
                    if "auth_key" in cache_params:
                        cache_params.pop("auth_key")

                    cache_path = base64encode(cache_params)
                    found = self.cache_service.exists([log_endpoint, cache_path])
                    if found:
                        cached_response_text = self.cache_service.hget(
                            [log_endpoint, cache_path],
                            "text",
                        )
                        cached_response_status_code = self.cache_service.hget(
                            [log_endpoint, cache_path],
                            "status_code",
                        )
                        if (
                            cached_response_status_code
                            and int(cached_response_status_code) == 200
                        ):
                            print(
                                f"✅ [memory] {method}: {log_endpoint}{cache_url_query} (memory cache)"
                            )
                            return {
                                "text": loads(cached_response_text),
                                "status_code": cached_response_status_code,
                            }

                response = self._request(
                    endpoint,
                    method=method,
                    params=params,
                    body=body,
                    headers=headers,
                    timeout=timeout,
                )

                if response.status_code in status_force_list:
                    print(
                        f"✅ [{response.elapsed.total_seconds() if response else None}s] {method}: {log_endpoint}{cache_url_query} - retrying... ({_+1}) (code: wrong status_code)"
                    )
                    continue

                if response.status_code == 200:
                    if self.cache_service is not None:
                        self.cache_service.hset(
                            [log_endpoint, cache_path],
                            "text",
                            response.text,
                        )

                        self.cache_service.hset(
                            [log_endpoint, cache_path],
                            "status_code",
                            response.status_code,
                        )

                if response.status_code == 400:
                    print(
                        f"🚸 [{timeout if timeout else None}s] {method}: {log_endpoint}{cache_url_query} - stopped ({_+1}) (code: HTTPError) {params_str}"
                    )
                else:
                    print(
                        f"✅ [{response.elapsed.total_seconds() if response else None}s] {method}: {log_endpoint}{cache_url_query}"
                    )

                return response
            except requests.exceptions.Timeout:
                print(
                    f"⛔️ [{timeout if timeout else None}] {method}: {log_endpoint}{cache_url_query} - retrying... ({_+1}) (code: Timeout){params_str}"
                )
                continue
            except requests.exceptions.ConnectionError:
                print(
                    f"⛔️ [{timeout if timeout else None}] {method}: {log_endpoint}{cache_url_query} - stopped ({_+1}) (code: ConnectionError) {params_str}"
                )
                pass

        return None
