import os
from pathlib import Path

import folder_paths

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import any_type

class InoS3UploadFile:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "execute": (any_type,),
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "s3_key": ("STRING", {"default": ""}),
                "parent_folder": (["input", "output", "temp"],),
                "local_path": ("STRING", {"default": "input/example.png"}),
                "delete_local": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING , "tooltip": "you can leave it empty and pass it with env vars"}),
                "bucket_name": ("STRING", {"default": "default"}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", )
    RETURN_NAMES = ("success", "msg", "result", )
    FUNCTION = "function"

    async def function(self, execute, enabled:bool, s3_key:str, parent_folder:str, local_path:str, delete_local:bool, s3_config:str, bucket_name:str):
        if not enabled:
            return (False, "not enabled", "",)

        if not execute:
            return (False, "execute empty", "", )

        validate_s3_config = S3Helper.validate_s3_config(s3_config)
        if not validate_s3_config["success"]:
            return (False, validate_s3_config["msg"], "", )
        s3_config = validate_s3_config["config"]

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"], "", )

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
            return (False, validate_local_path["msg"], "", )

        s3_instance = S3Helper.get_instance(s3_config)
        s3_result = await s3_instance.upload_file(
            s3_key=s3_key,
            local_file_path=abs_path,
            # bucket_name=bucket_name,
        )
        if s3_result["success"] and delete_local:
            os.remove(abs_path)

        return (s3_result["success"], s3_result["msg"], s3_result, )
