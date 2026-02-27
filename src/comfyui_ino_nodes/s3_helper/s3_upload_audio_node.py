import os
from pathlib import Path
from datetime import datetime

from PIL import Image, ImageOps, ImageSequence
from PIL.PngImagePlugin import PngInfo
import numpy as np
from inopyutils import ino_ok, ino_err, ino_is_err

import folder_paths
from comfy.cli_args import args

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import any_type

class InoS3UploadAudio:
    # todo add bool, to save file as input file name, or after saving it in temp, to include the _00001
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "execute": (any_type,),
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "audio": ("AUDIO",),
                "s3_key": ("STRING", {"default": ""}),
                "file_name": ("STRING", {"default": ""})
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING, "tooltip": "you can leave it empty and pass it with env vars"}),
                "date_time_as_name": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("AUDIO", "BOOLEAN", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("audio", "success", "msg", "result", "file_name", "s3_audio_path",)
    FUNCTION = "function"
    CATEGORY = "InoS3Helper"

    async def function(self, execute, enabled, audio, s3_key, file_name, s3_config, date_time_as_name):
        if not enabled:
            return (audio, False, "", "", "", "",)

        if not execute:
            return (audio, False, "", "", "", "",)

        if isinstance(file_name, list):
            if len(file_name) == 1:
                file_name = str(file_name[0])
            else:
                return (audio, False, "file name is list", "", "", "",)

        elif isinstance(file_name, str):
            pass
        else:
            return (audio, False, "file name not string", "", "", "",)

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (audio, False, validate_s3_key["msg"], "", "", "",)

        if date_time_as_name:
            file_name = datetime.now().strftime("%Y%m%d%H%M%S%f")

        save_as = "mp3"
        file = f"{file_name}.{save_as}"

        from comfy_extras.nodes_audio import SaveAudioMP3

        audio_saver = SaveAudioMP3()
        save_audio = audio_saver.execute(
            audio=audio,
            filename_prefix=file_name,
            format="mp3",
            quality="128k"
        )

        if not isinstance(save_audio, dict):
            return (audio, False, "Audio saved, but failed to get filename", "", "", "",)

        if len(save_audio["ui"]["audio"]) != 1:
            return (audio, False, "Audio saved, but there is more than one file", "", "", "",)

        file_name = save_audio["ui"]["audio"][0]["filename"]

        parent_path = folder_paths.get_output_directory()
        full_path:Path = Path(parent_path) / file_name

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return (audio, False, s3_instance["msg"], "", "", "",)
        s3_instance = s3_instance["instance"]

        s3_full_key = f"{s3_key.rstrip('/')}/{file_name}"
        s3_result = await s3_instance.upload_file(
            s3_key=s3_full_key,
            local_file_path=full_path,
            # bucket_name=bucket_name,
        )
        if not s3_result["success"]:
            return (audio, False, s3_result["msg"], "", "", "",)

        #os.remove(full_path)

        return (audio, True, "Success", s3_result, file, s3_full_key, )
