from pathlib import Path

from inopyutils import ino_is_err

import folder_paths

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import any_type

class InoS3VerifyFile:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "execute": (any_type,),
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "s3_key": ("STRING", {"default": ""}),
                "parent_folder": (["input", "output", "temp"],),
                "local_path": ("STRING", {"default": "input/example.png"}),
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING, "tooltip": "you can leave it empty and pass it with env vars"}),
                "use_md5": ("BOOLEAN", {"default": False}),
                "use_sha256": ("BOOLEAN", {"default": False}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "BOOLEAN", "BOOLEAN",)
    RETURN_NAMES = ("success", "msg", "result", "exists_remote", "sizes_match",)
    FUNCTION = "function"

    async def function(self, execute, enabled, s3_key, parent_folder, local_path, s3_config, use_md5, use_sha256):
        if not enabled:
            return (False, "not enabled", "", False, False,)

        if not execute:
            return (False, "execute empty", "", False, False,)

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"], "", False, False,)

        if parent_folder == "input":
            parent_path = folder_paths.get_input_directory()
        elif parent_folder == "output":
            parent_path = folder_paths.get_output_directory()
        else:
            parent_path = folder_paths.get_temp_directory()

        local_file_path: Path = Path(parent_path) / Path(local_path)
        abs_path = str(local_file_path.resolve())

        validate_local_path = S3Helper.validate_local_path(local_file_path)
        if not validate_local_path["success"]:
            return (False, validate_local_path["msg"], "", False, False,)

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return (False, s3_instance["msg"], "", False, False,)
        s3_instance = s3_instance["instance"]

        s3_result = await s3_instance.verify_file(
            local_file_path=abs_path,
            s3_key=s3_key,
            use_md5=use_md5,
            use_sha256=use_sha256,
        )

        return (
            s3_result["success"],
            s3_result["msg"],
            str(s3_result),
            s3_result.get("exists_remote", False),
            s3_result.get("sizes_match", False),
        )
