from pathlib import Path

from .s3_helper import S3Helper

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
        validate_s3_config = S3Helper.validate_s3_config(s3_config)
        if not validate_s3_config["success"]:
            return (False, validate_s3_config["msg"], None,)

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"], None,)

        if Path(save_path).is_file():
            return (False, "Save path is a file", None,)

        if not Path(save_path).is_dir():
            Path(save_path).mkdir(parents=True, exist_ok=True)

        rel_path = save_path
        abs_path = Path(rel_path).resolve()

        s3_instance = S3Helper.get_instance(s3_config)
        s3_result = await s3_instance.download_folder(
            s3_folder_key=s3_key,
            local_folder_path=str(rel_path),
            #bucket_name=bucket_name,
            max_concurrent=max_concurrent
        )
        return (s3_result["success"], s3_result["msg"], s3_result, str(rel_path), str(abs_path), )
