import os
from .s3_helper import get_s3_instance, get_save_path

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
        s3_instance = get_s3_instance(s3_config)
        s3_result = await s3_instance.upload_file(
            s3_key=s3_key,
            local_file_path=local_path,
            #bucket_name=bucket_name,
            max_concurrent=max_concurrent
        )
        if s3_result["success"] and delete_local:
            os.remove(local_path)

        return (s3_result["success"], s3_result["msg"], s3_result, )
