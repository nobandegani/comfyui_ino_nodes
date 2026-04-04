from pathlib import Path

import folder_paths

from inopyutils import ino_ok, ino_err, ino_is_err

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import PARENT_FOLDER_OPTIONS, resolve_comfy_path

class InoS3DownloadFolder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "s3_key": ("STRING", {"default": "input/example.png"}),
                "parent_folder": (PARENT_FOLDER_OPTIONS,),
                "folder": ("STRING", {"default": "input/"}),
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING, "tooltip": "you can leave it empty and pass it with env vars"}),
                "bucket_name": ("STRING", {"default": "default"}),
                "max_concurrent": ("INT", {"default": 5, "min": 1, "max": 10}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("success", "message", "rel_path", "abs_path", )
    FUNCTION = "function"

    async def function(self, enabled, s3_key, parent_folder, folder, s3_config=None, bucket_name=None, max_concurrent=5):
        if not enabled:
            return (False, "not enabled", "", "", )

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"], "", "",)

        rel_path, abs_path = resolve_comfy_path(parent_folder, folder)

        if Path(abs_path).is_file():
            return (False, "Save path is a file", "", "",)

        if not Path(abs_path).is_dir():
            Path(abs_path).mkdir(parents=True, exist_ok=True)

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return (False, s3_instance["msg"], "", "",)
        s3_instance = s3_instance["instance"]

        s3_result = await s3_instance.download_folder(
            s3_folder_key=s3_key,
            local_folder_path=abs_path,
            max_concurrent=max_concurrent
        )

        return (s3_result["success"], s3_result["msg"], rel_path, abs_path, )
