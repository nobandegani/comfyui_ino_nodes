import os
from pathlib import Path

from inopyutils import ino_ok, ino_err, ino_is_err

import folder_paths

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import any_type, PARENT_FOLDER_OPTIONS, resolve_comfy_path

class InoS3UploadFile:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "execute": (any_type,),
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "s3_key": ("STRING", {"default": ""}),
                "parent_folder": (PARENT_FOLDER_OPTIONS,),
                "folder": ("STRING", {"default": ""}),
                "filename": ("STRING", {"default": ""}),
                "delete_local": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING , "tooltip": "you can leave it empty and pass it with env vars"}),
                "bucket_name": ("STRING", {"default": "default"}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("success", "message", "rel_path", "abs_path", )
    FUNCTION = "function"
    OUTPUT_NODE = True

    async def function(self, execute, enabled:bool, s3_key:str, parent_folder:str, folder:str, filename:str, delete_local:bool, s3_config:str=None, bucket_name:str=None):
        if not enabled:
            return (False, "not enabled", "", "",)

        if not execute:
            return (False, "execute empty", "", "", )

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"], "", "", )

        rel_path, abs_path = resolve_comfy_path(parent_folder, folder, filename)

        local_upload_path = Path(abs_path)
        validate_local_path = S3Helper.validate_local_path(local_upload_path)
        if not validate_local_path["success"]:
            return (False, validate_local_path["msg"], rel_path, abs_path, )

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return (False, s3_instance["msg"], rel_path, abs_path, )
        s3_instance = s3_instance["instance"]

        s3_result = await s3_instance.upload_file(
            s3_key=s3_key,
            local_file_path=abs_path,
        )
        if s3_result["success"] and delete_local:
            os.remove(abs_path)

        return (s3_result["success"], s3_result["msg"], rel_path, abs_path, )
