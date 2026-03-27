import os

from inopyutils import InoRunpodHelper, ino_is_err

from custom_nodes.comfyui_ino_nodes.src.comfyui_ino_nodes.node_helper import ino_print_log


class InoVllmRunSync:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "url": ("STRING", {"default": ""}),
                "api_key": ("STRING", {"default": ""}),
                "model": ("STRING", {"default": ""}),
                "user_prompt": ("STRING", {"default": ""}),
            },
            "optional": {
                "system_prompt": ("STRING", {"default": ""}),
                "image_url": ("STRING", {"default": ""}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.1}),
                "max_tokens": ("INT", {"default": 1024, "min": 1, "max": 128000}),
            }
        }

    CATEGORY = "InoRunpodHelper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "INT", "INT", "STRING",)
    RETURN_NAMES = ("success", "id", "status", "delay_time", "execution_time", "response",)
    FUNCTION = "function"

    async def function(self, enabled, url, api_key, model, user_prompt,
                       system_prompt="", image_url="", temperature=0.7, max_tokens=1024):
        if not enabled:
            ino_print_log("InoVllmRunSync", "Node is disabled")
            return (False, "", "not enabled", 0, 0, "")

        try:
            api_key = api_key if api_key else os.getenv('RUNPOD_API_KEY', '')
            image = image_url if image_url else None

            response = await InoRunpodHelper.serverless_vllm_runsync(
                url=url,
                api_key=api_key,
                model=model,
                user_prompt=user_prompt,
                system_prompt=system_prompt,
                image=image,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            if ino_is_err(response):
                return (False, "", response.get("msg", "unknown error"), 0, 0, "")

            return (
                True,
                response.get("id", ""),
                response.get("status", ""),
                response.get("delay_time", 0),
                response.get("execution_time", 0),
                response.get("response", ""),
            )
        except Exception as e:
            ino_print_log("InoVllmRunSync", "", e)
            return (False, "", f"response failed: {e}", 0, 0, "")


LOCAL_NODE_CLASS = {
    "InoVllmRunSync": InoVllmRunSync,
}
LOCAL_NODE_NAME = {
    "InoVllmRunSync": "Ino Vllm Run Sync",
}
