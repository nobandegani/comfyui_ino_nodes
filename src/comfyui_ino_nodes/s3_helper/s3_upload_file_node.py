import os
from .s3_helper import get_s3_instance, get_save_path

class InoS3UploadFile:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "s3_config": ("STRING", {"default": ""}),
                "s3_key": ("STRING", {"default": ""}),
                "local_path": ("STRING", {"default": "input/example.png"}),
                "delete_local": ("BOOLEAN", {"default": True}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", )
    RETURN_NAMES = ("success", "msg", "result", )
    FUNCTION = "function"

    async def function(self, s3_key, local_path, delete_local, s3_config):
        s3_instance = get_s3_instance(s3_config)
        uploaded = await s3_instance.upload_file(
            s3_key=s3_key,
            local_file_path=local_path
        )
        if uploaded["success"] and delete_local:
            os.remove(local_path)
        return (uploaded["success"], uploaded["msg"], uploaded, )
