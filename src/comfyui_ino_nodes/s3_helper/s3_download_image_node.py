import os
import torch
import numpy as np
from PIL import Image, ImageOps, ImageSequence

from .s3_client import get_s3_instance, get_save_path
S3_INSTANCE = get_s3_instance()


class InoS3DownloadImage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "s3_key": ("STRING", {"default": "input/example.png"}),
                "save_locally": ("BOOLEAN", {"default": True}),
                "save_path": ("STRING", {"default": "input/example.png"})
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "IMAGE", "MASK", )
    RETURN_NAMES = ("success", "msg", "result", "image", "mask", )
    FUNCTION = "function"

    async def function(self, s3_key, save_locally, save_path):
        rel_path = get_save_path(s3_key, save_path)
        abs_path = rel_path.resolve()
        downloaded = await S3_INSTANCE.download_file(
            s3_key=s3_key,
            local_file_path=str(rel_path)
        )
        if not downloaded["success"]:
            return (downloaded["success"], downloaded["msg"], downloaded, None, None, )

        img = Image.open(rel_path)
        output_images = []
        output_masks = []
        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            if i.mode == 'I':
                i = i.point(lambda i: i * (1 / 255))
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        if not save_locally:
            os.remove(rel_path)

        return (downloaded["success"], downloaded["msg"], downloaded, output_image, output_mask, )
