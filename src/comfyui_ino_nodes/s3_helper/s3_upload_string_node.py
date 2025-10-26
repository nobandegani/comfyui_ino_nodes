import os
from pathlib import Path
from datetime import datetime

from PIL import Image, ImageOps, ImageSequence
from PIL.PngImagePlugin import PngInfo
import numpy as np
from inopyutils import InoJsonHelper, InoFileHelper

import folder_paths
from comfy.cli_args import args

from .s3_helper import S3Helper
from ..node_helper import any_type

class InoS3UploadString:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "execute": (any_type,),
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "string": ("STRING",),
                "save_as": (["txt", "json", "ini"], ),
                "s3_config": ("STRING", {"default": ""}),
                "s3_key": ("STRING", {"default": ""}),
                "file_name": ("STRING", {"default": ""})
            },
            "optional": {
                "date_time_as_name": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING", "BOOLEAN", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("STRING", "success", "msg", "result", "file_name", "s3_image_path",)
    FUNCTION = "function"
    CATEGORY = "InoS3Helper"

    async def function(self, execute, enabled, string, save_as, s3_config, s3_key, file_name, date_time_as_name):
        if not enabled:
            return (string, False, "", "", "", "",)

        if not execute:
            return (string, False, "", "", "", "",)

        if isinstance(file_name, list):
            if len(file_name) == 1:
                file_name = str(file_name[0])
            else:
                return (string, False, "", "", "", "",)
        elif isinstance(file_name, str):
            pass
        else:
            return (string, False, "", "", "", "",)

        validate_s3_config = S3Helper.validate_s3_config(s3_config)
        if not validate_s3_config["success"]:
            return (string,False, "", "", "", "",)

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (string,False, "", "", "", "",)

        if date_time_as_name:
            file_name = datetime.now().strftime("%Y%m%d%H%M%S")

        parent_path = folder_paths.get_temp_directory()

        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(file_name, parent_path, 0, 0)

        filename_with_batch_num = filename.replace("%batch_num%", "0")
        file = f"{filename_with_batch_num}_{counter:05}_.{save_as}"
        full_path = os.path.join(full_output_folder, file)

        if save_as == "json":
            save_file = await InoJsonHelper.save_string_as_json_async(string, full_path)
        else:
            save_file = await InoFileHelper.save_string_as_file(string, full_path)

        if not save_file["success"]:
            return (string, False, save_file["msg"], "", "", "", )

        s3_instance = S3Helper.get_instance(s3_config)

        s3_full_key = s3_key + "/" + file
        s3_result = await s3_instance.upload_file(
            s3_key=s3_full_key,
            local_file_path=full_path,
            # bucket_name=bucket_name,
        )
        if not s3_result["success"]:
            return (string, False, s3_result["msg"], "", "", "",)

        os.remove(full_path)

        return (string, True, "Success", s3_result, file, s3_full_key, )
