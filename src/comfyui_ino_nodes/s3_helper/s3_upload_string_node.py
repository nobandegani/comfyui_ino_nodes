import os
from pathlib import Path
from datetime import datetime

from PIL import Image, ImageOps, ImageSequence
from PIL.PngImagePlugin import PngInfo
import numpy as np
from inopyutils import InoJsonHelper, InoFileHelper, ino_ok, ino_err, ino_is_err, InoUtilHelper

import folder_paths
from comfy.cli_args import args

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import any_type, PARENT_FOLDER_OPTIONS, resolve_comfy_path

class InoS3UploadString:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "execute": (any_type,),
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "string": ("STRING",),
                "save_as": (["txt", "json", "ini"], ),
                "s3_key": ("STRING", {"default": ""}),
                "parent_folder": (PARENT_FOLDER_OPTIONS, {"default": "temp"}),
                "folder": ("STRING", {"default": ""}),
                "filename": ("STRING", {"default": ""})
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING, "tooltip": "you can leave it empty and pass it with env vars"}),
                "date_time_as_name": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING", "BOOLEAN", "STRING", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("STRING", "success", "message", "rel_path", "abs_path", "file_name", "s3_string_path",)
    FUNCTION = "function"
    OUTPUT_NODE = True
    CATEGORY = "InoS3Helper"

    async def function(self, execute, enabled, string, save_as, s3_key, parent_folder, folder, filename, s3_config=None, date_time_as_name=False):
        if not enabled:
            return (string, False, "", "", "", "", "",)

        if not execute:
            return (string, False, "", "", "", "", "",)

        if isinstance(filename, list):
            if len(filename) == 1:
                filename = str(filename[0])
            else:
                return (string, False, "file name is list", "", "", "", "",)
        elif isinstance(filename, str):
            pass
        else:
            return (string, False, "file name not string", "", "", "", "",)

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (string, False, validate_s3_key["msg"], "", "", "", "",)

        if date_time_as_name:
            filename = InoUtilHelper.get_date_time_utc_base64()

        rel_path, abs_path = resolve_comfy_path(parent_folder, folder)

        full_output_folder, file_prefix, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename, abs_path, 0, 0)

        filename_with_batch_num = file_prefix.replace("%batch_num%", "0")
        file = f"{filename_with_batch_num}_{counter:05}"
        file_w_ext= f"{file}.{save_as}"
        full_path = os.path.join(full_output_folder, file_w_ext)

        if save_as == "json":
            save_file = await InoJsonHelper.save_string_as_json_async(string, full_path)
        else:
            save_file = await InoFileHelper.save_string_as_file(string, full_path)

        if not save_file["success"]:
            return (string, False, save_file["msg"], rel_path, abs_path, "", "", )

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return (string, False, s3_instance["msg"], rel_path, abs_path, "", "", )
        s3_instance = s3_instance["instance"]

        s3_full_key = f"{s3_key.rstrip('/')}/{filename}.{save_as}"
        s3_result = await s3_instance.upload_file(
            s3_key=s3_full_key,
            local_file_path=full_path,
        )
        if not s3_result["success"]:
            return (string, False, s3_result["msg"], rel_path, abs_path, "", "",)

        return (string, True, "Success", rel_path, abs_path, file_w_ext, s3_full_key, )
