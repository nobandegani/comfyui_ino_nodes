import os

from inopyutils import InoJsonHelper, InoOpenAIHelper
from openai import OpenAI

from custom_nodes.comfyui_ino_nodes.src.comfyui_ino_nodes.node_helper import ino_print_log

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
                    "label": "Seed (0 = random)",
                    "control_after_generate": True,
                }),
                "response_type": (["text", "image"], {}),
                "text": ("STRING", {"default": ""}),
                "image_url": ("STRING", {"default": ""}),
            },
            "optional": {
                "openai_api_key": ("STRING", {"default": ""}),
                "timeout": ("FLOAT", {"default": 300}),
                "max_retries": ("INT", {"default": 3}),
                "model": (["gpt-5", "gpt-4.1"], {}),
            }
        }

    CATEGORY = "InoOpenaiHelper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("success", "id", "status", "error", "output_text", "output",)
    FUNCTION = "function"

    async def function(self, enabled, seed, response_type, text, image_url, openai_api_key="", timeout=300, max_retries=3, model="gpt-5"):
        if not enabled:
            ino_print_log("InoOpenaiResponses","Node is disabled")
            return (False, "", "not enabled", "", "", "")

        try:
            api_key = openai_api_key if openai_api_key else os.getenv('OPENAI_TOKEN', '')
            client = OpenAI(
                api_key=api_key,
                timeout=timeout,
                max_retries=max_retries,
            )

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
            return (False, "", "Openai response failed", str(e), "", "", )


class InoOpenaiChatCompletions:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "user_prompt": ("STRING", {"default": ""}),
            },
            "optional": {
                "openai_api_key": ("STRING", {"default": ""}),
                "base_url": ("STRING", {"default": "https://api.openai.com/v1"}),
                "model": ("STRING", {"default": "gpt-5"}),
                "system_prompt": ("STRING", {"default": ""}),
                "image_url": ("STRING", {"default": ""}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.1}),
                "max_tokens": ("INT", {"default": 1024, "min": 1, "max": 128000}),
            }
        }

    CATEGORY = "InoOpenaiHelper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("success", "response", "finish_reason", "error",)
    FUNCTION = "function"

    async def function(self, enabled, user_prompt, openai_api_key="", base_url="https://api.openai.com/v1",
                       model="gpt-5", system_prompt="", image_url="", temperature=0.7, max_tokens=1024):
        if not enabled:
            ino_print_log("InoOpenaiChatCompletions", "Node is disabled")
            return (False, "", "", "not enabled")

        try:
            api_key = openai_api_key if openai_api_key else os.getenv('OPENAI_TOKEN', '')
            image = image_url if image_url else None

            result = await InoOpenAIHelper.chat_completions(
                api_key=api_key,
                base_url=base_url,
                model=model,
                user_prompt=user_prompt,
                system_prompt=system_prompt,
                image=image,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            if result.get("success"):
                return (True, result.get("response", ""), result.get("finish_reason", ""), "none")
            else:
                error_msg = result.get("message", "unknown error")
                ino_print_log("InoOpenaiChatCompletions", "", error_msg)
                return (False, "", "", error_msg)
        except Exception as e:
            ino_print_log("InoOpenaiChatCompletions", "", e)
            return (False, "", "", str(e))


LOCAL_NODE_CLASS = {
    "InoOpenaiResponses": InoOpenaiResponses,
    "InoOpenaiChatCompletions": InoOpenaiChatCompletions,
}
LOCAL_NODE_NAME = {
    "InoOpenaiResponses": "Ino Openai Responses",
    "InoOpenaiChatCompletions": "Ino Openai Chat Completions",
}
