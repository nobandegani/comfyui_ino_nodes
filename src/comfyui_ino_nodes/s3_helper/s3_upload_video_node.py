import os
from pathlib import Path
from datetime import datetime

from PIL import Image, ImageOps, ImageSequence
from PIL.PngImagePlugin import PngInfo
import numpy as np
from inopyutils import InoJsonHelper, ino_ok, ino_err, ino_is_err, InoUtilHelper

import folder_paths
from comfy.cli_args import args
from comfy_api.latest import ComfyExtension, io, ui, Input, InputImpl, Types

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import any_type

class InoS3UploadVideo:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "execute": (any_type,),
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "video": ("VIDEO",),
                "s3_key": ("STRING", {"default": ""}),
                "file_name": ("STRING", {"default": ""})
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING, "tooltip": "you can leave it empty and pass it with env vars"}),
                "date_time_as_name": ("BOOLEAN", {"default": False}),
                "video_format": (("mp4", "auto"), {}),
                "video_codec": (("h264", "auto"), {}),
            },
        }

    RETURN_TYPES = ("Video", "BOOLEAN", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("video", "success", "msg", "result", "file_name", "s3_video_path",)
    FUNCTION = "function"
    OUTPUT_NODE = True
    CATEGORY = "InoS3Helper"

    async def function(self, execute, enabled, video: Input.Video, s3_key, file_name, s3_config, date_time_as_name, video_format, video_codec):
        if not enabled:
            return (video, False, "", "", "", "",)

        if not execute:
            return (video, False, "", "", "", "",)

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (video, False, validate_s3_key["msg"], "", "", "")

        if date_time_as_name:
            file_name = InoUtilHelper.get_date_time_utc_base64()

        parent_path = folder_paths.get_temp_directory()

        width, height = video.get_dimensions()

        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
            file_name,
            parent_path,
            width,
            height
        )

        saved_metadata = None

        filename_w_ext = f"{filename}.{Types.VideoContainer.get_extension(video_format)}"
        file_path = os.path.join(full_output_folder, filename_w_ext)

        video.save_to(
            file_path,
            format=Types.VideoContainer(video_format),
            codec=video_codec,
            metadata=saved_metadata
        )

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return (video, False, s3_instance["msg"], str(s3_instance), "", "")
        s3_instance = s3_instance["instance"]

        s3_full_key = s3_key + "/" + filename_w_ext
        s3_result = await s3_instance.upload_file(
            s3_key=s3_full_key,
            local_file_path=file_path,
            # bucket_name=bucket_name,
        )
        if not s3_result["success"]:
            #os.remove(results[index]["full_path"])
            return (video, s3_result["success"], s3_result["msg"], str(s3_result), file_name, s3_full_key,)

        return (video, s3_result["success"], s3_result["msg"], str(s3_result), file_name, s3_full_key,)
