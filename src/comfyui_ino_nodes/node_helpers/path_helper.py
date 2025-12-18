import folder_paths

from pathlib import Path

class InoGetComfyPath:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder_type": (["input", "output", "temp"],),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("String",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, folder_type):
        if folder_type == "input":
            final_path = folder_paths.get_input_directory()
        elif folder_type == "output":
            final_path = folder_paths.get_output_directory()
        else:
            final_path = folder_paths.get_temp_directory()
        return (final_path,)

class InoGetLoraPathNameTriggerWord:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "lora_path": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING",)
    RETURN_NAMES = ("lora_id", "lora_name", "lora_trigger_word",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, lora_path, ):
        lora_path = Path(lora_path)
        lora_id = lora_path.parent.name
        lora_name = lora_path.stem
        trigger_word = lora_name.split('_')[0]

        return ( lora_id, lora_name, trigger_word, )

LOCAL_NODE_CLASS = {
    "InoGetComfyPath": InoGetComfyPath,
    "InoGetLoraPathNameTriggerWord": InoGetLoraPathNameTriggerWord
}
LOCAL_NODE_NAME = {
    "InoGetComfyPath": "Ino Get Comfy Path",
    "InoGetLoraPathNameTriggerWord": "Ino Get Lora Path Name Trigger Word",
}
