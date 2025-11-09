import os
import shutil
from pathlib import Path

import folder_paths

from inopyutils import ino_ok, ino_err, ino_is_err

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import any_type

class InoS3UploadFolder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "execute": (any_type,),
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "s3_key": ("STRING", {"default": ""}),
                "parent_folder": (["input", "output", "temp"], ),
                "local_path": ("STRING", {"default": "input/example.png"}),
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
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "INT", "INT", "INT", "STRING", )
    RETURN_NAMES = ("success", "msg", "result", "total_files", "uploaded_successfully", "failed_uploads", "errors", )
    FUNCTION = "function"

    async def function(self, execute, enabled, s3_key, parent_folder, local_path, delete_local, s3_config, bucket_name, max_concurrent, verify_with_s3):
        if not enabled:
            return (False, "", "", 0, 0, 0, "", )

        if not execute:
            return (False, "", "", 0, 0, 0, "", )

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"], "", 0, 0, 0, "", )

        if parent_folder == "input":
            parent_path = folder_paths.get_input_directory()
        elif parent_folder == "output":
            parent_path = folder_paths.get_output_directory()
        else:
            parent_path = folder_paths.get_temp_directory()

        local_upload_path: Path = Path(parent_path) / Path(local_path)
        abs_path = str(local_upload_path.resolve())

        validate_local_path = S3Helper.validate_local_path(local_upload_path)
        if not validate_local_path["success"]:
            return (False, validate_local_path["msg"], "", 0, 0, 0, "", )

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return (False, s3_instance["msg"], "", 0, 0, 0, "", )
        s3_instance = s3_instance["instance"]

        s3_result = await s3_instance.upload_folder(
            s3_folder_key=s3_key,
            local_folder_path=abs_path,
            #bucket_name=bucket_name,
            max_concurrent=max_concurrent,
            verify=verify_with_s3
        )
        if s3_result["success"] and delete_local:
            shutil.rmtree(local_upload_path)

        return (s3_result["success"], s3_result["msg"], s3_result, s3_result["total_files"], s3_result["uploaded_successfully"], s3_result["failed_uploads"], s3_result["errors"], )
