import os
from .s3_client import get_s3_instance

S3_INSTANCE = get_s3_instance()

class InoS3UploadFile:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "s3_key": ("STRING", {"default": ""}),
                "local_path": ("STRING", {"default": "input/example.png"}),
                "delete_local": ("BOOLEAN", {"default": True}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", )
    RETURN_NAMES = ("success", "msg", "result", )
    FUNCTION = "function"

    async def function(self, s3_key, local_path, delete_local):
        uploaded = await S3_INSTANCE.upload_file(
            s3_key=s3_key,
            local_file_path=local_path
        )
        if uploaded["success"] and delete_local:
            os.remove(local_path)
        return (uploaded["success"], uploaded["msg"], uploaded, )
