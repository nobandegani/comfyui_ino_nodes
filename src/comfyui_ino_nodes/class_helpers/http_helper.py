from inopyutils import InoJsonHelper, InoHttpHelper

from custom_nodes.comfyui_ino_nodes.src.comfyui_ino_nodes.node_helper import ino_print_log


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
                "allow_redirects": ("BOOLEAN", {"default": False}),
                "max_retries": ("INT", {"default": 10, "min": 1, "max": 50}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "INT", "STRING", "STRING", )
    RETURN_NAMES = ("Success", "StatusCode", "MSG", "Response", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    async def function(self, enabled,
                       url, request_type, headers, json_payload,
                       trust_env, allow_redirects, max_retries
                       ):
        if not enabled:
            ino_print_log("InoHttpCall", "Attempt to run but disabled")
            return (False, 0, "Attempt to run but disabled", "", )

        http_client = None
        try:
            http_client = InoHttpHelper(
                retries=max_retries,
                trust_env=trust_env
            )

            if InoJsonHelper.is_valid(headers):
                headers = InoJsonHelper.string_to_dict(headers)["data"]
            else:
                headers = {}

            if InoJsonHelper.is_valid(json_payload):
                json_payload = InoJsonHelper.string_to_dict(json_payload)["data"]
            else:
                json_payload = {}

            if request_type == "get":
                resp = await http_client.get(url=url, headers=headers, allow_redirects=allow_redirects)
            elif request_type == "post":
                resp = await http_client.post(url=url, headers=headers, json=json_payload, allow_redirects=allow_redirects)
            elif request_type == "put":
                resp = await http_client.put(url, json=json_payload, allow_redirects=allow_redirects)
            elif request_type == "delete":
                resp = await http_client.delete(url, allow_redirects=allow_redirects)
            elif request_type == "patch":
                resp = await http_client.patch(url, json=json_payload, allow_redirects=allow_redirects)
            else:
                await http_client.close()
                ino_print_log("InoHttpCall", "Invalid request type", request_type)
                return (False, 0, "Invalid request type", "",)

            await http_client.close()
            if not resp["success"]:
                ino_print_log("InoHttpCall", resp["msg"], resp)
                return (False, 0, resp["msg"], resp,)

            ino_print_log("InoHttpCall", "Success")
            return (True, resp["status_code"], resp["msg"], resp["data"], )
        except Exception as e:
            if http_client:
                await http_client.close()
            ino_print_log("InoHttpCall", "", e)
            return (False, 0, str(e), "",)

LOCAL_NODE_CLASS = {
    "InoHttpCall": InoHttpCall,
}
LOCAL_NODE_NAME = {
    "InoHttpCall": "Ino Http Call",
}
