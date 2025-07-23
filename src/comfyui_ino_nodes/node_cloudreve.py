import torch
import numpy as np
from PIL import Image

from inspect import cleandoc


class Cloudreve_Get_Captcha:
    """
        Cloudreve Get Captcha
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "server_address": ("STRING", {
                    "multiline": False,
                    "default": "token"
                })
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "IMAGE")
    RETURN_NAMES = ("status", "ticket", "image")
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "function"

    # OUTPUT_NODE = True
    # OUTPUT_TOOLTIPS = ("",) # Tooltips for the output node

    CATEGORY = "InoNodes"

    def __init__(self):
        pass


    def function(self, enabled, server_address):
        if not enabled:
            img_tensor = torch.zeros((1, 512, 512, 3), dtype=torch.float32)
            return "Disabled", "", img_tensor

    # @classmethod
    # def IS_CHANGED(s, image, string_field, int_field, float_field, print_to_screen):
    #    return ""
