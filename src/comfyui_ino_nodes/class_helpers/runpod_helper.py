import hashlib
import random
import os

from inopyutils import InoJsonHelper, InoHttpHelper, InoRunpodHelper

from custom_nodes.comfyui_ino_nodes.src.comfyui_ino_nodes.node_helper import ino_print_log

class InoVllmRunSyncText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "url": ("STRING", {"default": ""}),
                "api_key": ("STRING", {"default": ""}),
                "system_prompt": ("STRING", {"default": ""}),
                "user_prompt": ("STRING", {"default": ""}),
            },
            "optional": {
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0}),
                "max_tokens": ("INT", {"default": 1024, "min": 32, "max": 4096}),
            }
        }

    CATEGORY = "InoRunpodHelper"
    RETURN_TYPES = ("BOOLEAN", "INT", "STRING", "INT", "INT", "STRING",)
    RETURN_NAMES = ("success", "id", "status", "delay_time", "execution_time", "response", )
    FUNCTION = "function"

    async def function(self, enabled, url, api_key, system_prompt, user_prompt, temperature, max_tokens):
        if not enabled:
            return (False, -1, "not enabled", "", "", "", )

        try:

            response = InoRunpodHelper.serverless_vllm_runsync(
                url=url,
                api_key=api_key,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            return (response["success"], response["id"], response["status"], response["delay_time"], response["execution_time"], response["response"], )
        except Exception as e:
            ino_print_log("InoOpenaiResponses","",e)
            return (False, -1, "Openai response failed", str(e), "", "", )


LOCAL_NODE_CLASS = {
    "InoVllmRunSyncText": InoVllmRunSyncText,
}
LOCAL_NODE_NAME = {
    "InoVllmRunSyncText": "Ino Vllm Run Sync Text",
}
