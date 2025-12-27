import os
import base64
from aiohttp import web

class InoBasicAuthClass:
    def __init__(self):
        self.username = os.getenv('COMFYUI_USERNAME', '')
        self.password = os.getenv('COMFYUI_PASSWORD', '')
        self.enabled = bool(self.username and self.password)

    @web.middleware
    async def handle(self, request, handler):
        if not self.enabled:
            return await handler(request)

        # Get Authorization header
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return web.Response(
                status=401,
                headers={'WWW-Authenticate': 'Basic realm="ComfyUI Server"'}
            )

        try:
            auth_type, auth_string = auth_header.split(' ', 1)
            if auth_type.lower() != 'basic':
                raise ValueError('Invalid auth type')

            decoded = base64.b64decode(auth_string).decode('utf-8')
            provided_username, provided_password = decoded.split(':', 1)

            if provided_username == self.username and provided_password == self.password:
                return await handler(request)

        except Exception:
            pass

        return web.Response(
            status=401,
            headers={'WWW-Authenticate': 'Basic realm="ComfyUI Server"'}
        )

class InoBasicAuthNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("BASIC_AUTH",)
    FUNCTION = "setup_auth"
    CATEGORY = "InoBasicAuth"
    OUTPUT_NODE = True

    def setup_auth(self, enabled):
        return ({"enabled": enabled},)

LOCAL_NODE_CLASS = {
    "InoBasicAuthNode": InoBasicAuthNode
}

LOCAL_NODE_NAME = {
    "InoBasicAuthNode": "Ino Basic Auth Node"
}
