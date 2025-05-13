import os
import time

import numpy as np
from PIL import Image, ImageOps

from inspect import cleandoc
from .hepler_upload import upload_file_to_bedrive

class BeDriveSaveFile:
    """
        Save file to Bedrive
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "file_path": ("STRING", {
                    "multiline": False,
                    "default": "/stest/test.png"
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

    RETURN_TYPES = ()
    #RETURN_NAMES = ("image_output_name",)
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "upload"

    OUTPUT_NODE = True
    # OUTPUT_TOOLTIPS = ("",) # Tooltips for the output node

    CATEGORY = "InoNodes"

    def __init__(self):
        pass

    def upload(self, enabled, file_path, api_token, parent_id, remove_after):
        if enabled == False:
            print("save file is disabled")
            return ()

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
        return ()

    # @classmethod
    # def IS_CHANGED(s, image, string_field, int_field, float_field, print_to_screen):
    #    return ""
