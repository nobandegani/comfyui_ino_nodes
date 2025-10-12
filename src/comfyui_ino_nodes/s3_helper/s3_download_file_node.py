from pathlib import Path
import folder_paths
from .s3_helper import S3Helper

class InoS3DownloadFile:
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
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("success", "msg", "result", "rel_path", "abs_path", )
    FUNCTION = "function"

    async def function(self, s3_key, save_path, s3_config, bucket_name):
        validate_s3_config = S3Helper.validate_s3_config(s3_config)
        if not validate_s3_config["success"]:
            return (False, validate_s3_config["msg"], "", 0, 0, 0, "",)

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"], "", 0, 0, 0, "",)

        output_path = folder_paths.get_output_directory()
        local_save_path: Path = Path(output_path) / Path(save_path)
        abs_path = str(local_save_path.resolve())

        if not Path(local_save_path).is_dir():
            Path(local_save_path).parent.mkdir(parents=True, exist_ok=True)

        s3_instance = S3Helper.get_instance(s3_config)
        s3_result = await s3_instance.download_file(
            s3_key=s3_key,
            local_file_path=abs_path
        )
        return (s3_result["success"], s3_result["msg"], s3_result, save_path, abs_path, )
