import os
import time

import numpy as np
from PIL import Image, ImageOps

from inspect import cleandoc
from .hepler_upload import upload_file_to_bedrive

class BeDriveSaveImage:
    """
        Save image to Bedrive
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "image": ("IMAGE", {"tooltip": "This is an image"}),
                "file_name": ("STRING", {
                    "multiline": False,
                    "default": "test"
                }),
                "api_token": ("STRING", {
                    "multiline": False,
                    "default": "token"
                }),
                "parent_id": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
                "remove_after": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "status_message")
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "upload"

    # OUTPUT_NODE = True
    # OUTPUT_TOOLTIPS = ("",) # Tooltips for the output node

    CATEGORY = "InoNodes"

    def __init__(self):
        pass


    def upload(self, enabled, image, file_name, api_token, parent_id, remove_after):
        if enabled == False:
            print("save file is disabled")
            return (image, "node is disabled")

        i = 255. * image[0].cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

        output_dir = os.path.join(os.path.dirname(__file__), "../../temp_images")
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, file_name)

        img.save(file_path)

        result = upload_file_to_bedrive(api_token, file_path, parent_id)
        if result.get("success"):
            if remove_after:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"⚠️ Failed to delete file: {e}")

            status = f"✅ Uploaded successfully"
        else:
            status = f"❌ Uploaded failed"

        print(result)
        return (image, status)

    # @classmethod
    # def IS_CHANGED(s, image, string_field, int_field, float_field, print_to_screen):
    #    return ""
