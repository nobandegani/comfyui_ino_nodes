from pathlib import Path

from .s3_helper import get_s3_instance, get_save_path

class InoS3DownloadFolder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "s3_config": ("STRING", {"default": ""}),
                "s3_key": ("STRING", {"default": "input/example.png"}),
                "save_path": ("STRING", {"default": "input/"}),
            },
            "optional": {
                "bucket_name": ("STRING", {"default": "default"}),
                "max_concurrent": ("INT", {"default": 5, "min": 1, "max": 10}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("success", "msg", "result", "rel_path", "abs_path", )
    FUNCTION = "function"

    async def function(self, s3_key, save_path, s3_config, bucket_name, max_concurrent):
        rel_path = save_path
        abs_path = rel_path.resolve()

        s3_instance = get_s3_instance(s3_config)
        s3_result = await s3_instance.download_folder(
            s3_key=s3_key,
            local_file_path=str(rel_path),
            #bucket_name=bucket_name,
            max_concurrent=max_concurrent
        )
        return (s3_result["success"], s3_result["msg"], s3_result, str(rel_path), str(abs_path), )
