from pathlib import Path

from inopyutils import ino_is_err

import folder_paths

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import any_type, PARENT_FOLDER_OPTIONS, resolve_comfy_path

class InoS3VerifyFile:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "execute": (any_type,),
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "s3_key": ("STRING", {"default": ""}),
                "parent_folder": (PARENT_FOLDER_OPTIONS,),
                "folder": ("STRING", {"default": ""}),
                "filename": ("STRING", {"default": ""}),
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING, "tooltip": "you can leave it empty and pass it with env vars"}),
                "use_md5": ("BOOLEAN", {"default": False}),
                "use_sha256": ("BOOLEAN", {"default": False}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "BOOLEAN", "BOOLEAN",)
    RETURN_NAMES = ("success", "message", "rel_path", "abs_path", "exists_remote", "sizes_match",)
    FUNCTION = "function"

    async def function(self, execute, enabled, s3_key, parent_folder, folder, filename, s3_config=None, use_md5=False, use_sha256=False):
        if not enabled:
            return (False, "not enabled", "", "", False, False,)

        if not execute:
            return (False, "execute empty", "", "", False, False,)

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"], "", "", False, False,)

        rel_path, abs_path = resolve_comfy_path(parent_folder, folder, filename)

        local_file_path = Path(abs_path)
        validate_local_path = S3Helper.validate_local_path(local_file_path)
        if not validate_local_path["success"]:
            return (False, validate_local_path["msg"], rel_path, abs_path, False, False,)

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return (False, s3_instance["msg"], rel_path, abs_path, False, False,)
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
            rel_path,
            abs_path,
            s3_result.get("exists_remote", False),
            s3_result.get("sizes_match", False),
        )
