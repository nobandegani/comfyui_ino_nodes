import os
import shutil
from pathlib import Path

import folder_paths

from inopyutils import ino_ok, ino_err, ino_is_err

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import any_type, PARENT_FOLDER_OPTIONS, resolve_comfy_path

class InoS3UploadFolder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "execute": (any_type,),
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "s3_key": ("STRING", {"default": ""}),
                "parent_folder": (PARENT_FOLDER_OPTIONS, ),
                "folder": ("STRING", {"default": ""}),
                "delete_local": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING, "tooltip": "you can leave it empty and pass it with env vars"}),
                "bucket_name": ("STRING", {"default": "default"}),
                "max_concurrent": ("INT", {"default": 5, "min": 1, "max": 10}),
                "verify_with_s3": ("BOOLEAN", {"default": False}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "INT", "INT", "INT", "STRING", )
    RETURN_NAMES = ("success", "message", "rel_path", "abs_path", "total_files", "uploaded_successfully", "failed_uploads", "errors", )
    FUNCTION = "function"
    OUTPUT_NODE = True

    async def function(self, execute, enabled, s3_key, parent_folder, folder, delete_local, s3_config=None, bucket_name=None, max_concurrent=5, verify_with_s3=False):
        if not enabled:
            return (False, "", "", "", 0, 0, 0, "", )

        if not execute:
            return (False, "", "", "", 0, 0, 0, "", )

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"], "", "", 0, 0, 0, "", )

        rel_path, abs_path = resolve_comfy_path(parent_folder, folder)

        local_upload_path = Path(abs_path)
        validate_local_path = S3Helper.validate_local_path(local_upload_path)
        if not validate_local_path["success"]:
            return (False, validate_local_path["msg"], rel_path, abs_path, 0, 0, 0, "", )

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return (False, s3_instance["msg"], rel_path, abs_path, 0, 0, 0, "", )
        s3_instance = s3_instance["instance"]

        s3_result = await s3_instance.upload_folder(
            s3_folder_key=s3_key,
            local_folder_path=abs_path,
            max_concurrent=max_concurrent,
            verify=verify_with_s3
        )
        if s3_result["success"] and delete_local:
            shutil.rmtree(local_upload_path)

        return (s3_result["success"], s3_result["msg"], rel_path, abs_path, s3_result["total_files"], s3_result["uploaded_successfully"], s3_result["failed_uploads"], str(s3_result["errors"]), )
