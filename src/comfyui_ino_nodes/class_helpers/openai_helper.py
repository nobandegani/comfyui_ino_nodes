import hashlib
import random
import os

from inopyutils import InoJsonHelper
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
        openai_api_key = os.getenv('OPENAI_TOKEN', openai_api_key)
        config = {
            "api_key": openai_api_key,
            "timeout": timeout,
            "max_retries": max_retries,
        }
        return (True, config)

class InoOpenaiResponses:
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
                "response_type": (["text", "image"], {}),
                "text": ("STRING", {"default": ""}),
                "image_url": ("STRING", {"default": ""}),
            },
            "optional": {
                "config": ("STRING", {"default": ""}),
                "model": (["gpt-5", "gpt-4.1"], {}),
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

    async def function(self, enabled, seed, response_type, text, image_url, config, model):
        if not enabled:
            ino_print_log("InoOpenaiTextGeneration","Node is disabled")
            return (False, -1, "not enabled", "", "", "", )

        try:
            client = get_openai_client(config)

            response_input = text
            if response_type == "text":
                pass
            elif response_type == "image":
                response_input=[
                    {
                        "role": "user",
                        "content": [
                            { "type": "input_text", "text": text },
                            {
                                "type": "input_image",
                                "image_url": image_url
                            }
                        ]
                    }
                ]
            response = client.responses.create(
                model=model,
                input=response_input
            )

            if response.error:
                error_message = response.error.message
            else:
                error_message = "none"

            if response.output:
                response_output = InoJsonHelper.dict_to_string(response.output)["data"]
            else:
                response_output = "empty"

            if response.output_text:
                response_text = response.output_text
            else:
                response_text = "empty"

            return (True, response.id, response.status, error_message, response_text, response_output, )
        except Exception as e:
            ino_print_log("InoOpenaiResponses","",e)
            return (False, -1, "Openai response failed", str(e), "", "", )


LOCAL_NODE_CLASS = {
    "InoOpenaiConfig": InoOpenaiConfig,
    "InoOpenaiTextGeneration": InoOpenaiResponses,
}
LOCAL_NODE_NAME = {
    "InoOpenaiConfig": "Ino Openai Config",
    "InoOpenaiTextGeneration": "Ino Openai Text Generation",
}
