import os
from pathlib import Path
from datetime import datetime

from PIL import Image, ImageOps, ImageSequence
from PIL.PngImagePlugin import PngInfo
import numpy as np
from inopyutils import InoJsonHelper, InoFileHelper

import folder_paths
from comfy.cli_args import args

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import any_type

class InoS3UploadAudio:
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

    RETURN_TYPES = ("STRING", "BOOLEAN", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("STRING", "success", "msg", "result", "file_name", "s3_audio_path",)
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

        validate_s3_config = S3Helper.validate_s3_config(s3_config)
        if not validate_s3_config["success"]:
            return (audio, False, validate_s3_config["msg"], "", "", "",)
        s3_config = validate_s3_config["config"]

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (audio, False, validate_s3_key["msg"], "", "", "",)

        if date_time_as_name:
            file_name = datetime.now().strftime("%Y%m%d%H%M%S")

        parent_path = folder_paths.get_temp_directory()

        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(file_name, parent_path, 0, 0)

        filename_with_batch_num = filename.replace("%batch_num%", "0")
        save_as = "mp3"
        file = f"{filename_with_batch_num}_{counter:05}_.{save_as}"
        full_path = os.path.join(full_output_folder, file)

        from comfy_extras.nodes_audio import SaveAudioMP3

        audio_saver = SaveAudioMP3()
        save_audio = audio_saver.save_mp3(
            audio=audio,
            filename_prefix=filename_prefix,
        )
        print(full_path)
        print(save_audio)

        return (audio, False, "", "", "", "",)

        if not save_file["success"]:
            return (audio, False, save_file["msg"], "", "", "", )

        s3_instance = S3Helper.get_instance(s3_config)

        s3_full_key = s3_key + "/" + file
        s3_result = await s3_instance.upload_file(
            s3_key=s3_full_key,
            local_file_path=full_path,
            # bucket_name=bucket_name,
        )
        if not s3_result["success"]:
            return (audio, False, s3_result["msg"], "", "", "",)

        os.remove(full_path)

        return (audio, True, "Success", s3_result, file, s3_full_key, )
