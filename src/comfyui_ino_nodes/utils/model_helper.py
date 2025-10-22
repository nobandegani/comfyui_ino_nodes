from pathlib import Path

import folder_paths
import node_helpers
from ..s3_helper.s3_helper import S3Helper

MODEL_TYPES = (
    "checkpoints", "clip", "clip_vision", "controlnet", "diffusers", "diffusion_models",
    "loras", "sams", "text_encoders", "vae"
)

class InoValidateModel:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "s3_config": ("STRING", {}),
                "model_type": (MODEL_TYPES, {}),
                "model_name": ("STRING", {"default": "flux1dev/ae.safetensors"}),
            }
        }

    CATEGORY = "InoModelHelper"
    RETURN_TYPES = ("BOOLEAN", "STRING", )
    RETURN_NAMES = ("success", "msg", )
    FUNCTION = "function"

    async def function(self, enabled, s3_config, model_type, model_name):
        if not enabled:
            return (False, "", )

        parent_path = Path(folder_paths.get_input_directory()).parent
        model_path:Path = parent_path / "models" / model_type / model_name
        print(model_path)
        need_download = not model_path.is_file()
        if not need_download:
            return (True, "model validated", )

        s3_key = f"comfyui/models/{model_type}/{model_name}"

        validate_s3_config = S3Helper.validate_s3_config(s3_config)
        if not validate_s3_config["success"]:
            return (False, validate_s3_config["msg"],)

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"],)

        model_path.parent.mkdir(parents=True, exist_ok=True)

        s3_instance = S3Helper.get_instance(s3_config)
        s3_result = await s3_instance.download_file(
            s3_key=s3_key,
            local_file_path=model_path
        )

        return (s3_result["success"], s3_result["msg"], )

LOCAL_NODE_CLASS = {
    "InoValidateModel": InoValidateModel
}
LOCAL_NODE_NAME = {
    "InoValidateModel": "Ino Validate Model"
}
