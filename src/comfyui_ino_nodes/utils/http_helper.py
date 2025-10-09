import httpx
import json
from httpx_retry import AsyncRetryTransport, RetryPolicy

from inopyutils import InoJsonHelper

class InoHttpCall:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "url": ("STRING", {"default": "http://127.0.0.1:3313/health"}),
                "request_type": (list(["get", "post", "put", "delete", "patch",]), {}),
                "headers": ("STRING", {"default": '{"Connection": "keep-alive"}'}),
                "json_payload": ("STRING", {"default": None})
            },
            "optional": {
                "trust_env": ("BOOLEAN", {"default": False}),
                "follow_redirects": ("BOOLEAN", {"default": False}),
                "enable_retries": ("BOOLEAN", {"default": True}),
                "max_retries": ("INT", {"default": 10, "min": 1, "max": 50}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "INT", "STRING", "STRING", )
    RETURN_NAMES = ("Success", "StatusCode", "MSG", "Response", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    async def function(self, enabled,
                       url, request_type, headers, json_payload,
                       trust_env, follow_redirects, enable_retries, max_retries
                       ):
        if not enabled:
            return (False, 0, "", "", )

        timeout = httpx.Timeout(connect=10.0, read=60, write=60, pool=10.0)
        limits = httpx.Limits(max_connections=8, max_keepalive_connections=8, keepalive_expiry=120.0)

        if enable_retries:
            exponential_retry = (
                RetryPolicy()
                .with_max_retries(max_retries)
                .with_min_delay(0.1)
                .with_multiplier(2)
                .with_retry_on(lambda status_code: status_code >= 500)
            )
        else:
            exponential_retry = None

        if InoJsonHelper.is_valid(headers):
            headers = InoJsonHelper.string_to_dict(headers)
        else:
            headers = {}

        if InoJsonHelper.is_valid(json_payload):
            json_payload = InoJsonHelper.string_to_dict(json_payload)
        else:
            json_payload = {}

        http_conn = httpx.AsyncClient(
            timeout=timeout,
            limits=limits,
            transport=AsyncRetryTransport(policy=exponential_retry),
            headers=headers,
            trust_env=trust_env,
            follow_redirects=follow_redirects
        )

        try:
            if request_type == "get":
                resp = await http_conn.get(url)
            elif request_type == "post":
                resp = await http_conn.post(url, json=json_payload)
            elif request_type == "put":
                resp = await http_conn.put(url, json=json_payload)
            elif request_type == "delete":
                resp = await http_conn.delete(url)
            elif request_type == "patch":
                resp = await http_conn.patch(url, json=json_payload)
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

LOCAL_NODE_CLASS = {
    "InoHttpCall": InoHttpCall,
}
LOCAL_NODE_NAME = {
    "InoHttpCall": "Ino Http Call",
}
