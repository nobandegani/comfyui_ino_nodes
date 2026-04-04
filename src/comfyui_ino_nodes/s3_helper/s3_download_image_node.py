from pathlib import Path

from inopyutils import ino_is_err, InoUtilHelper

import folder_paths

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import PARENT_FOLDER_OPTIONS, resolve_comfy_path, load_image_with_mask

class InoS3DownloadImage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "s3_key": ("STRING", {"default": "input/example.png"}),
                "parent_folder": (PARENT_FOLDER_OPTIONS, {"default": "temp"}),
                "folder": ("STRING", {"default": ""}),
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING, "tooltip": "you can leave it empty and pass it with env vars"}),
                "bucket_name": ("STRING", {"default": "default"}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "IMAGE", "MASK", )
    RETURN_NAMES = ("success", "message", "rel_path", "abs_path", "image", "mask", )
    FUNCTION = "function"

    async def function(self, enabled, s3_key, parent_folder, folder, s3_config=None, bucket_name=None):
        from nodes import EmptyImage
        empty_image = EmptyImage().generate(512, 512)[0]
        if not enabled:
            return (False, "not enabled", "", "", empty_image, None, )

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"], "", "", empty_image, None,)

        random_str = InoUtilHelper.get_date_time_utc_base64()
        file_name = f'{random_str}{Path(s3_key).suffix}'
        rel_path, abs_path = resolve_comfy_path(parent_folder, folder, file_name)

        Path(abs_path).parent.mkdir(parents=True, exist_ok=True)

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return (False, s3_instance["msg"], "", "", empty_image, None,)
        s3_instance = s3_instance["instance"]

        downloaded = await s3_instance.download_file(
            s3_key=s3_key,
            local_file_path=abs_path
        )
        if not downloaded["success"]:
            return (downloaded["success"], downloaded["msg"], rel_path, abs_path, empty_image, None, )

        output_image, output_mask = load_image_with_mask(downloaded["local_file"])

        return (downloaded["success"], downloaded["msg"], rel_path, abs_path, output_image, output_mask, )
