import os
from pathlib import Path
from datetime import datetime

from PIL import Image, ImageOps, ImageSequence
from PIL.PngImagePlugin import PngInfo
import numpy as np
from inopyutils import InoJsonHelper

import folder_paths
from comfy.cli_args import args

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import any_type

class InoS3UploadImage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "execute": (any_type,),
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "images": ("IMAGE",),
                "s3_key": ("STRING", {"default": ""}),
                "file_name": ("STRING", {"default": ""})
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING, "tooltip": "you can leave it empty and pass it with env vars"}),
                "compress_level": ("INT", {"default": 4, "min": 1, "max": 9}),
                "date_time_as_name": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("IMAGE", "BOOLEAN", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("images", "success", "msg", "result", "file_names", "s3_image_paths",)
    FUNCTION = "function"
    CATEGORY = "InoS3Helper"

    async def function(self, execute, enabled, images, s3_key, file_name, s3_config, compress_level, date_time_as_name):
        if not enabled:
            return (images, False, "", "", "", "",)

        if not execute:
            return (images, False, "", "", "", "",)

        validate_s3_config = S3Helper.validate_s3_config(s3_config)
        if not validate_s3_config["success"]:
            return (images, False, validate_s3_config["msg"], "", "", "",)
        s3_config = validate_s3_config["config"]

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (images, False, validate_s3_key["msg"], "", "", )

        if date_time_as_name:
            file_name = datetime.now().strftime("%Y%m%d%H%M%S")

        parent_path = folder_paths.get_temp_directory()

        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(file_name, parent_path, images[0].shape[1], images[0].shape[0])
        results:dict = {}
        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()

            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            full_path = os.path.join(full_output_folder, file)
            img.save(full_path, pnginfo=metadata, compress_level=compress_level)
            results[batch_number] = {
                "filename": file,
                "full_path": full_path,
            }
            counter += 1

        s3_instance = S3Helper.get_instance(s3_config)

        for index in results:
            s3_full_key = s3_key + "/" + results[index]["filename"]
            s3_result = await s3_instance.upload_file(
                s3_key=s3_full_key,
                local_file_path=results[index]["full_path"],
                # bucket_name=bucket_name,
            )
            if s3_result["success"]:
                os.remove(results[index]["full_path"])
                results[index]["s3_success"] = s3_result["success"]
                results[index]["s3_msg"] = s3_result["msg"]
                results[index]["s3_key"] = s3_full_key

        result_str = InoJsonHelper.dict_to_string(results)['data']

        final_success = True
        final_message = ""
        for index in results:
            if not results[index]["s3_success"]:
                final_success = False
                final_message = results[index]["s3_msg"]
                break

        if not final_success:
            return (images, final_success, final_message, result_str, "", )

        s3_paths = []
        file_names = []
        for index in results:
            s3_paths.append(results[index]["s3_key"])
            file_names.append(results[index]["filename"])

        return (images, True, "Success", result_str, file_names, s3_paths, )
