import hashlib
import random

from openai import OpenAI

from custom_nodes.comfyui_ino_nodes.src.comfyui_ino_nodes.node_helper import ino_print_log

openai_client = None

def get_openai_client(config):
    global openai_client
    if openai_client is None:
        openai_client = OpenAI(
            api_key=config["api_key"],
            timeout=config["timeout"],
            max_retries=config["max_retries"],
        )
    return openai_client


class InoOpenaiConfig:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "openai_api_key": ("STRING", {"default": "sk-proj-xxxxxxx"}),
                "timeout": ("FLOAT", {"default": 300}),
                "max_retries": ("INT", {"default": 3}),
            }
        }

    CATEGORY = "InoOpenaiHelper"
    RETURN_TYPES = ("BOOLEAN", "STRING",)
    RETURN_NAMES = ("success", "config",)
    FUNCTION = "function"

    async def function(self, openai_api_key, timeout, max_retries):
        config = {
            "api_key": openai_api_key,
            "timeout": timeout,
            "max_retries": max_retries,
        }
        return (True, config)

class InoOpenaiTextGeneration:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "step": 1,
                    "label": "Seed (0 = random)"
                }),
                "config": ("STRING", {"default": ""}),
                "prompt": ("STRING", {"default": ""}),
                "model": ("STRING", {"default": "gpt-5"}),
            }
        }

    CATEGORY = "InoOpenaiHelper"
    RETURN_TYPES = ("BOOLEAN", "INT", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("success", "id", "status", "error", "output_text", "output",)
    FUNCTION = "function"

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        m = hashlib.sha256()
        m.update(seed)
        return m.digest().hex()

    async def function(self, enabled, seed, config, prompt, model):
        if not enabled:
            ino_print_log("InoOpenaiTextGeneration","Node is disabled")
            return (False, )

        try:
            client = get_openai_client(config)

            response = client.responses.create(
                model=model,
                input=prompt
            )

            if response.error:
                error_message = response.error.message
            else:
                error_message = "none"

            return (True, response.id, response.status, error_message, response.output_text, "", )
        except Exception as e:
            ino_print_log("InoOpenaiTextGeneration","",e)
            return (False, -1, "", "", "", "", )


LOCAL_NODE_CLASS = {
    "InoOpenaiConfig": InoOpenaiConfig,
    "InoOpenaiTextGeneration": InoOpenaiTextGeneration,
}
LOCAL_NODE_NAME = {
    "InoOpenaiConfig": "Ino Openai Config",
    "InoOpenaiTextGeneration": "Ino Openai Text Generation",
}
