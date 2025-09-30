import os
import json
import tempfile
from pathlib import Path
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from comfy.cli_args import args

from .s3_client import get_s3_instance
S3_INSTANCE = get_s3_instance()

class InoS3UploadImage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "s3_key": ("STRING", {"default": ""}),
                "file_name": ("STRING", {"default": ""})
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("success", "msg", "result", "s3_image_paths",)
    FUNCTION = "function"
    CATEGORY = "InoS3Helper"

    async def function(self, images, s3_key, file_name):
        results = list()
        s3_image_paths = list()

        counter = 0
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()

            file = f"{file_name}_{counter:05}.png"
            temp_file: Path = Path("input/temp_file.png")
            try:
                img.save(temp_file, pnginfo=metadata)

                s3_path:str = f"{s3_key}/{file}"

                uploaded = await S3_INSTANCE.upload_file(
                    s3_key=str(s3_path),
                    local_file_path=str(temp_file)
                )
                if not uploaded["success"]:
                    return (uploaded["success"], uploaded["msg"], results, s3_image_paths,)

                s3_image_paths.append(s3_path)

                results.append(uploaded)
                counter += 1
            finally:
                if temp_file.exists():
                    os.remove(temp_file)

        return (True, "sucess", results, s3_image_paths, )
