import os
import shutil
from .s3_helper import S3Helper

class InoS3UploadFolder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "s3_config": ("STRING", {"default": ""}),
                "s3_key": ("STRING", {"default": ""}),
                "local_path": ("STRING", {"default": "input/example.png"}),
                "delete_local": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "bucket_name": ("STRING", {"default": "default"}),
                "max_concurrent": ("INT", {"default": 5, "min": 1, "max": 10}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", )
    RETURN_NAMES = ("success", "msg", "result", )
    FUNCTION = "function"

    async def function(self, s3_key, local_path, delete_local, s3_config, bucket_name, max_concurrent):
        validate_s3_config = S3Helper.validate_s3_config(s3_config)
        if not validate_s3_config["success"]:
            return (False, validate_s3_config["msg"], None, )

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"], None,)

        validate_local_path = S3Helper.validate_local_path(local_path)
        if not validate_local_path["success"]:
            return (False, validate_local_path["msg"], None,)

        s3_instance = S3Helper.get_instance(s3_config)
        s3_result = await s3_instance.upload_folder(
            s3_folder_key=s3_key,
            local_folder_path=local_path,
            #bucket_name=bucket_name,
            max_concurrent=max_concurrent
        )
        if s3_result["success"] and delete_local:
            shutil.rmtree(local_path)

        return (s3_result["success"], s3_result["msg"], s3_result, )
