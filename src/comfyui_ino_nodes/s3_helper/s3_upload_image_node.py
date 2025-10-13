import os
from pathlib import Path

from PIL import Image, ImageOps, ImageSequence
from PIL.PngImagePlugin import PngInfo
import numpy as np
from inopyutils import InoJsonHelper

import folder_paths
from comfy.cli_args import args

from .s3_helper import S3Helper
from ..node_helper import any_typ

class InoS3UploadImage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "execute": (any_typ,),
                "images": ("IMAGE",),
                "s3_config": ("STRING", {"default": ""}),
                "s3_key": ("STRING", {"default": ""}),
                "file_name": ("STRING", {"default": ""})
            },
            "optional": {
                "compress_level": ("INT", {"default": 4, "min": 1, "max": 9}),
            },
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("success", "msg", "result", "s3_image_paths",)
    FUNCTION = "function"
    CATEGORY = "InoS3Helper"

    async def function(self, execute, images, s3_config, s3_key, file_name, compress_level):
        if not execute:
            return (False, "", "", "", )

        validate_s3_config = S3Helper.validate_s3_config(s3_config)
        if not validate_s3_config["success"]:
            return (False, "", "", "", )

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, "", "", "", )

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

        result_str = InoJsonHelper.dict_to_string(results)['data']
        return (True, "Success", result_str, "", )
