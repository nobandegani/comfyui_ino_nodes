import os
import torch
import numpy as np
from PIL import Image, ImageOps, ImageSequence

from pathlib import Path
from datetime import datetime

import folder_paths
import node_helpers

from .s3_helper import S3Helper

class InoS3DownloadImage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "s3_config": ("STRING", {"default": ""}),
                "s3_key": ("STRING", {"default": "input/example.png"}),
            },
            "optional": {
                "bucket_name": ("STRING", {"default": "default"}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "IMAGE", "MASK", )
    RETURN_NAMES = ("success", "msg", "result", "image", "mask", )
    FUNCTION = "function"

    async def function(self, enabled, s3_config, s3_key, bucket_name):
        if not enabled:
            return (False, "", "", None, None, )

        validate_s3_config = S3Helper.validate_s3_config(s3_config)
        if not validate_s3_config["success"]:
            return (False, validate_s3_config["msg"], "", None, None,)

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"], "", None, None,)

        parent_path = folder_paths.get_temp_directory()

        file_name = f'{datetime.now().strftime("%Y%m%d%H%M%S")}{Path(s3_key).suffix}'
        local_save_path: Path = Path(parent_path) / file_name

        s3_instance = S3Helper.get_instance(s3_config)
        downloaded = await s3_instance.download_file(
            s3_key=s3_key,
            local_file_path=str(local_save_path.resolve())
        )
        if not downloaded["success"]:
            return (downloaded["success"], downloaded["msg"], downloaded, None, None, )

        img = node_helpers.pillow(Image.open, downloaded["local_file"])

        output_images = []
        output_masks = []
        w, h = None, None

        excluded_formats = ['MPO']

        for i in ImageSequence.Iterator(img):
            i = node_helpers.pillow(ImageOps.exif_transpose, i)

            if i.mode == 'I':
                i = i.point(lambda i: i * (1 / 255))
            image = i.convert("RGB")

            if len(output_images) == 0:
                w = image.size[0]
                h = image.size[1]

            if image.size[0] != w or image.size[1] != h:
                continue

            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            elif i.mode == 'P' and 'transparency' in i.info:
                mask = np.array(i.convert('RGBA').getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1 and img.format not in excluded_formats:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        return (downloaded["success"], downloaded["msg"], downloaded, output_image, output_mask, )
