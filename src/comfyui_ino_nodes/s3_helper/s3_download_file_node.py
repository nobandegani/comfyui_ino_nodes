from pathlib import Path

from .s3_client import get_s3_instance, get_save_path
S3_INSTANCE = get_s3_instance()

class InoS3DownloadFile:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "s3_key": ("STRING", {"default": "input/example.png"}),
                "save_path": ("STRING", {"default": "input/"}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("success", "msg", "result", "rel_path", "abs_path", )
    FUNCTION = "function"

    async def function(self, s3_key, save_path):
        rel_path = get_save_path(s3_key, save_path)
        abs_path = rel_path.resolve()

        downloaded = await S3_INSTANCE.download_file(
            s3_key=s3_key,
            local_file_path=str(rel_path)
        )
        return (downloaded["success"], downloaded["msg"], downloaded, str(rel_path), str(abs_path), )
