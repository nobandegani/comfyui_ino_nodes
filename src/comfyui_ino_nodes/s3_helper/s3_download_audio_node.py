import os
import torch
import numpy as np
from PIL import Image, ImageOps, ImageSequence

from pathlib import Path
from datetime import datetime

import folder_paths
import node_helpers

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING

class InoS3DownloadAudio:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "s3_key": ("STRING", {"default": "input/example.wav"}),
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING, "tooltip": "you can leave it empty and pass it with env vars"}),
                "bucket_name": ("STRING", {"default": "default"}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "AUDIO", )
    RETURN_NAMES = ("success", "msg", "result", "audio", )
    FUNCTION = "function"

    async def function(self, enabled, s3_key, s3_config, bucket_name):
        if not enabled:
            return (False, "not enabled", "", None, )

        validate_s3_config = S3Helper.validate_s3_config(s3_config)
        if not validate_s3_config["success"]:
            return (False, validate_s3_config["msg"], "", None, )
        s3_config = validate_s3_config["config"]

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"], "", None, )

        parent_path = folder_paths.get_temp_directory()

        file_name = f'{datetime.now().strftime("%Y%m%d%H%M%S")}{Path(s3_key).suffix}'
        local_save_path: Path = Path(parent_path) / file_name

        s3_instance = S3Helper.get_instance(s3_config)
        downloaded = await s3_instance.download_file(
            s3_key=s3_key,
            local_file_path=str(local_save_path.resolve())
        )
        if not downloaded["success"]:
            return (downloaded["success"], downloaded["msg"], downloaded, None, )

        from comfy_extras.nodes_audio import LoadAudio

        audio_loader = LoadAudio()
        load_audio = audio_loader.load(audio=downloaded["local_file"])

        if load_audio[0]:
            return (True, "Success", downloaded, load_audio[0],)

        return (False, "failed to load the audio", downloaded, load_audio[0],)
