import httpx
from httpx_retry import AsyncRetryTransport, RetryPolicy

class InoHttpCall:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "url": ("STRING", {"default": "http://127.0.0.1:3314/health"}),
                "request_type": (list(["get", "post", "put", "delete", "patch",]), {}),
                "headers": ("STRING", {"default": '{"Connection": "keep-alive"}'}),
                "json": ("STRING", {"default": None})
            }
        }

    RETURN_TYPES = ("BOOLEAN", "INT", "STRING", "STRING", )
    RETURN_NAMES = ("Success", "StatusCode", "MSG", "Response", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    async def function(self, enabled, url, request_type, headers, json):
        if not enabled:
            return (False, 0, "", "", )

        timeout = httpx.Timeout(connect=10.0, read=60, write=60, pool=10.0)
        limits = httpx.Limits(max_connections=8, max_keepalive_connections=8, keepalive_expiry=120.0)

        exponential_retry = (
            RetryPolicy()
            .with_max_retries(10)
            .with_min_delay(0.1)
            .with_multiplier(2)
            .with_retry_on(lambda status_code: status_code >= 500)
        )

        headers = headers
        http_conn = httpx.AsyncClient(
            timeout=timeout,
            limits=limits,
            #transport=AsyncRetryTransport(policy=exponential_retry),
            headers=headers,
            #trust_env=False,
            #follow_redirects=False
        )

        try:
            if request_type == "get":
                resp = await http_conn.get(url)
            elif request_type == "post":
                resp = await http_conn.post(url, json=json)
            elif request_type == "put":
                resp = await http_conn.put(url, json=json)
            elif request_type == "delete":
                resp = await http_conn.delete(url)
            elif request_type == "patch":
                resp = await http_conn.patch(url, json=json)
            else:
                resp = await http_conn.get(url)

            resp.raise_for_status()
        except httpx.RequestError as exc:
            return (False, 0, f"Request error: {exc}", "", )
        except httpx.HTTPStatusError as exc:
            return (False, exc.response.status_code, f"HTTP error: {exc.response}", "", )

        try:
            response = resp.json()
        except ValueError:
            response = resp.text

        return (True, resp.status_code, f"Http call successfull", response, )
