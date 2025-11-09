from pathlib import Path
import folder_paths

from inopyutils import ino_ok, ino_err, ino_is_err

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING

class InoS3DownloadFile:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "s3_key": ("STRING", {"default": "input/example.png"}),
                "parent_folder": (["input", "output", "temp"],),
                "save_path": ("STRING", {"default": "s3download/"}),
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING, "tooltip": "you can leave it empty and pass it with env vars"}),
                "bucket_name": ("STRING", {"default": "default"}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("success", "msg", "result", "rel_path", "abs_path", )
    FUNCTION = "function"

    async def function(self, enabled, s3_key, parent_folder, save_path, s3_config, bucket_name):
        if not enabled:
            return (False, "not enabled", "", "", "",)

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"], "", "", "",)

        if parent_folder == "input":
            parent_path = folder_paths.get_input_directory()
        elif parent_folder == "output":
            parent_path = folder_paths.get_output_directory()
        else:
            parent_path = folder_paths.get_temp_directory()

        save_path = S3Helper.get_save_path(s3_key, save_path)

        local_save_path: Path = Path(parent_path) / Path(save_path)
        abs_path = str(local_save_path.resolve())

        if not Path(local_save_path).is_dir():
            Path(local_save_path).parent.mkdir(parents=True, exist_ok=True)

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return (False, s3_instance["msg"], "", "", "",)
        s3_instance = s3_instance["instance"]

        s3_result = await s3_instance.download_file(
            s3_key=s3_key,
            local_file_path=abs_path
        )
        return (s3_result["success"], s3_result["msg"], s3_result, save_path, abs_path, )
