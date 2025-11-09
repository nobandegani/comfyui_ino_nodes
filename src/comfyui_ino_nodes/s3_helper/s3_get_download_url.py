from pathlib import Path
import folder_paths

from inopyutils import ino_ok, ino_err, ino_is_err

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING


class InoS3GetDownloadURL:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "s3_key": ("STRING", {"default": "input/example.png"}),
                "expires_in": ("INT", {"default": 3600, "min": 1, "max": 3600, "step": 1}),
                "as_attachment": ("BOOLEAN", {"default": False}),
                "filename": ("STRING", {"default": ""}),
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING, "tooltip": "you can leave it empty and pass it with env vars"}),
                "bucket_name": ("STRING", {"default": "default"}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("success", "msg", "result", "download_url", "filename",)
    FUNCTION = "function"

    async def function(self, enabled:bool, s3_key:str, expires_in:int = 3600, as_attachment:bool = False, filename:str = None, s3_config:str = "{}", bucket_name:str = "default"):
        if not enabled:
            return (False, "not enabled", "", "", "",)

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"], "", "", "",)

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return (False, s3_instance["msg"], "", "", "",)
        s3_instance = s3_instance["instance"]

        s3_result = await s3_instance.get_download_link(
            s3_key=s3_key,
            #bucket_name=bucket_name,
            expires_in=expires_in,
            as_attachment=as_attachment,
            filename=filename,
        )
        return (s3_result["success"], s3_result["msg"], s3_result, s3_result["url"], s3_result["filename"],)
