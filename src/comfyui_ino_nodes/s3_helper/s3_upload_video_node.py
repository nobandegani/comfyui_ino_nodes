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
from ..node_helper import any_type, PARENT_FOLDER_OPTIONS, resolve_comfy_path

class InoS3UploadVideo:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "execute": (any_type,),
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "video": ("VIDEO",),
                "s3_key": ("STRING", {"default": ""}),
                "parent_folder": (PARENT_FOLDER_OPTIONS, {"default": "temp"}),
                "folder": ("STRING", {"default": ""}),
                "filename": ("STRING", {"default": ""})
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING, "tooltip": "you can leave it empty and pass it with env vars"}),
                "date_time_as_name": ("BOOLEAN", {"default": False}),
                "video_format": (("mp4", "auto"), {}),
                "video_codec": (("h264", "auto"), {}),
            },
        }

    RETURN_TYPES = ("Video", "BOOLEAN", "STRING", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("video", "success", "message", "rel_path", "abs_path", "file_name", "s3_video_path",)
    FUNCTION = "function"
    OUTPUT_NODE = True
    CATEGORY = "InoS3Helper"

    async def function(self, execute, enabled, video: Input.Video, s3_key, parent_folder, folder, filename, s3_config=None, date_time_as_name=False, video_format="mp4", video_codec="h264"):
        if not enabled:
            return (video, False, "", "", "", "", "",)

        if not execute:
            return (video, False, "", "", "", "", "",)

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (video, False, validate_s3_key["msg"], "", "", "", "")

        if date_time_as_name:
            filename = InoUtilHelper.get_date_time_utc_base64()

        rel_path, abs_path = resolve_comfy_path(parent_folder, folder)

        _, parent_abs = resolve_comfy_path(parent_folder, folder)
        width, height = video.get_dimensions()

        full_output_folder, file_prefix, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
            filename,
            parent_abs,
            width,
            height
        )

        saved_metadata = None

        filename_w_ext = f"{file_prefix}.{Types.VideoContainer.get_extension(video_format)}"
        file_path = os.path.join(full_output_folder, filename_w_ext)

        video.save_to(
            file_path,
            format=Types.VideoContainer(video_format),
            codec=video_codec,
            metadata=saved_metadata
        )

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return (video, False, s3_instance["msg"], rel_path, abs_path, "", "")
        s3_instance = s3_instance["instance"]

        s3_full_key = s3_key + "/" + filename_w_ext
        s3_result = await s3_instance.upload_file(
            s3_key=s3_full_key,
            local_file_path=file_path,
        )
        if not s3_result["success"]:
            return (video, s3_result["success"], s3_result["msg"], rel_path, abs_path, filename, s3_full_key,)

        return (video, s3_result["success"], s3_result["msg"], rel_path, abs_path, filename, s3_full_key,)
