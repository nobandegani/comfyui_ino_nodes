import random
import json
import torch
from torchvision.transforms import InterpolationMode
import torchvision.transforms.functional as TorchFunctional
import hashlib
from datetime import datetime, timezone
from ..node_helper import any_typ

#---------------------------------InoNotBoolean
class InoNotBoolean:
    """
        reverse boolean
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "boolean": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", )
    RETURN_NAMES = ("boolean", )

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, boolean):
        return (not boolean, )


# ---------------------------------InoIntEqual
class InoIntEqual:
    """
        check if its equal to the input Int
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "int_a": ("INT", {
                    "default": 0,
                    "step": 1,
                    "display": "number"
                }),
                "int_b": ("INT", {
                    "default": 0,
                    "step": 1,
                    "display": "number"
                }),
            },

        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is equal",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, int_a, int_b):
        return (int_a == int_b,)


class InoStringToggleCase:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "input_string": ("STRING", {
                    "multiline": True,
                    "default": "Test String"
                }),
                "toggle_to": ("BOOLEAN", {"default": True, "label_off": "Lower", "label_on": "Upper"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("String",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, enabled, input_string, toggle_to):
        if not enabled:
            return input_string
        result = str(input_string).upper() if toggle_to else str(input_string).lower()
        return (result,)

class InoBoolToSwitch:
    """
        Convert bool to int, 2 for true, 1 for false
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "input_bool": ("BOOLEAN", {})
            }
        }

    RETURN_TYPES = ("INT", )
    RETURN_NAMES = ("INT", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, enabled, input_bool):
        if not enabled:
            return -1

        if input_bool:
            result = 2
        else:
            result = 1

        return (result, )

class InoStringToCombo:
    """
        Convert string to combo value
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "input_string": ("STRING", {
                    "multiline": False,
                    "default": "default"
                }),
            }
        }

    RETURN_TYPES = ("COMBO", )
    RETURN_NAMES = ("COMBO", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, enabled, input_string):
        if not enabled or not input_string:
            return (input_string, )

        return (input_string, )

class InoDateTimeAsString:
    """
        Date Time As String
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "step": 1,
                    "label": "Seed (0 = random)"
                }),
                "include_year": ("BOOLEAN", {"default": True, "label_off": "Exclude", "label_on": "Include"}),
                "include_month": ("BOOLEAN", {"default": True, "label_off": "Exclude", "label_on": "Include"}),
                "include_day": ("BOOLEAN", {"default": True, "label_off": "Exclude", "label_on": "Include"}),
                "include_hour": ("BOOLEAN", {"default": True, "label_off": "Exclude", "label_on": "Include"}),
                "include_minute": ("BOOLEAN", {"default": True, "label_off": "Exclude", "label_on": "Include"}),
                "include_second": ("BOOLEAN", {"default": True, "label_off": "Exclude", "label_on": "Include"}),
                "date_sep": ("STRING", {
                    "multiline": False,
                    "default": "-"
                }),
                "datetime_sep": ("STRING", {
                    "multiline": False,
                    "default": "-"
                }),
                "time_sep": ("STRING", {
                    "multiline": False,
                    "default": "-"
                }),
            },
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("output_date_time", )
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        m = hashlib.sha256()
        m.update(seed)
        return m.digest().hex()

    def function(
        self, seed,
        include_year, include_month, include_day,
        include_hour, include_minute, include_second,
        date_sep="-", datetime_sep=" ", time_sep=":"
    ):
        now = datetime.now()

        date_parts = []
        time_parts = []

        if include_year:
            date_parts.append(str(now.year))
        if include_month:
            date_parts.append(f"{now.month:02d}")
        if include_day:
            date_parts.append(f"{now.day:02d}")

        if include_hour:
            time_parts.append(f"{now.hour:02d}")
        if include_minute:
            time_parts.append(f"{now.minute:02d}")
        if include_second:
            time_parts.append(f"{now.second:02d}")

        date_str = date_sep.join(date_parts) if date_parts else ""
        time_str = time_sep.join(time_parts) if time_parts else ""

        if date_str and time_str:
            return (f"{date_str}{datetime_sep}{time_str}", )
        elif date_str:
            return (date_str, )
        elif time_str:
            return (time_str, )
        else:
            return ("", )

class InoRandomIntInRange:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "int_min": ("INT", {"default": 0, "min": 0, "max": 999999}),
                "int_max": ("INT", {"default": 999999, "min": 0, "max": 999999}),
                "length": ("INT", {"default": 1, "min": 0, "max": 10}),
            }
        }

    RETURN_TYPES = ("INT", "INT", )
    RETURN_NAMES = ("RandomInt", "FormattedInt", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, enabled, int_min, int_max, length):
        if not enabled:
            return (-1, )
        random_int = random.randint(int_min, int_max)
        formatted_int = str(random_int).zfill(length)
        return (random_int, formatted_int, )

class InoIntToString:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_int": ("INT", {"default": 0}),
            }
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("ReturnString", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, input_int):
        return (str(input_int), )

class InoIntToFloat:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_int": ("INT", {"default": 0}),
            }
        }

    RETURN_TYPES = ("FLOAT", )
    RETURN_NAMES = ("ReturnFLOAT", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, input_int):
        return (float(input_int), )

class InoFloatToInt:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_float": ("FLOAT", {"default": 0}),
                "method": ( ["round", "floor", "ceil"], {})
            }
        }

    RETURN_TYPES = ("INT", )
    RETURN_NAMES = ("ReturnINT", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, input_float, method):
        import math
        if method == "round":
            return (round(input_float),)
        elif method == "floor":
            return (math.floor(input_float),)
        elif method == "ceil":
            return (math.ceil(input_float), )

class InoSaveImages:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", {"tooltip": "The images to save."}),
                "filename_prefix": ("STRING", {"default": "ComfyUI", "tooltip": "The prefix for the file to save. This may include formatting information such as %date:yyyy-MM-dd% or %Empty Latent Image.width% to include values from nodes."})
            }
        }

    RETURN_TYPES = ("STRING" , "INT", )
    RETURN_NAMES = ("Result", "NumberOfImages", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, images, filename_prefix):
        from nodes import SaveImage
        save_image = SaveImage()
        save_image_res = save_image.save_images(
            images=images,
            filename_prefix=filename_prefix
        )
        results = save_image_res["ui"]["images"]

        names = []
        for result in results:
            names.append(result["filename"])

        return (names, len(results), )

class InoImageResizeByLongerSideV1:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "size": ("INT", {"default": 512, "min": 0, "step": 1, "max": 99999}),
                "interpolation_mode": (
                    ["bicubic", "bilinear", "nearest", "nearest exact"],
                ),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Result",)

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(
        self,
        image: torch.Tensor,
        size: int,
        interpolation_mode: str,
    ):
        assert isinstance(image, torch.Tensor)
        assert isinstance(size, int)
        assert isinstance(interpolation_mode, str)

        interpolation_mode = interpolation_mode.upper().replace(" ", "_")
        interpolation_mode = getattr(InterpolationMode, interpolation_mode)

        _, h, w, _ = image.shape

        if h >= w:
            new_h = size
            new_w = round(w * new_h / h)
        else:  # h < w
            new_w = size
            new_h = round(h * new_w / w)

        image = image.permute(0, 3, 1, 2)
        image = TorchFunctional.resize(
            image,
            (new_h, new_w),
            interpolation=interpolation_mode,
            antialias=True,
        )
        image = image.permute(0, 2, 3, 1)

        return (image,)

import nodes
MAX_RESOLUTION = nodes.MAX_RESOLUTION

class InoImageResizeByLongerSideAndCropV2:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "target_width": ("INT", {
                    "default": 512,
                    "min": 1,
                    "max": MAX_RESOLUTION,
                    "step": 1
                }),
                "target_height": ("INT", {
                    "default": 512,
                    "min": 1,
                    "max": MAX_RESOLUTION,
                    "step": 1
                }),
                "padding_color": (["white", "black"],),
                "interpolation": (["area", "bicubic", "nearest-exact", "bilinear", "lanczos"],),
                "crop": ("BOOLEAN", {"default": True}),
                "position": (["top-left", "top-center", "center", "bottom-center", "bottom-right"],),
                "x": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
                "y": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Result",)

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, image, target_width: int, target_height: int, padding_color, interpolation, crop, position, x, y):
        from comfy_extras.nodes_images import GetImageSize, ImageCrop, ResizeAndPadImage
        get_image_size = GetImageSize()
        image_size = get_image_size.get_size(image)
        source_width = int(image_size[0])
        source_height = int(image_size[1])

        source_is_width_larger:bool = source_width > source_height
        target_is_width_larger:bool = target_width > target_height

        if source_is_width_larger == True and target_is_width_larger == True:
            resize_width:int = target_width
            resize_height:int = round((target_width / source_width) * source_height)
        else:
            resize_height:int = target_height
            resize_width:int = round((target_height / source_height) * source_width)

        resizer = ResizeAndPadImage()
        resized_image = resizer.resize_and_pad(image, resize_width, resize_height, padding_color, interpolation)

        if not crop:
            return (resized_image[0],)

        cropper = ImageCrop()
        # Compute crop origin based on position. If position is set, it overrides manual x/y.
        canvas = resized_image[0]
        # canvas shape: (batch, height, width, channels)
        canvas_h = int(canvas.shape[1])
        canvas_w = int(canvas.shape[2])

        def clamp(val, lo, hi):
            return max(lo, min(val, hi))

        # Defaults to manual x/y, but overridden by position mapping below
        crop_x = int(x)
        crop_y = int(y)

        # Horizontal positions
        left_x = 0
        center_x = max(0, (canvas_w - int(target_width)) // 2)
        right_x = max(0, canvas_w - int(target_width))
        # Vertical positions
        top_y = 0
        center_y = max(0, (canvas_h - int(target_height)) // 2)
        bottom_y = max(0, canvas_h - int(target_height))

        if position == "top-left":
            crop_x, crop_y = left_x, top_y
        elif position == "top-center":
            crop_x, crop_y = center_x, top_y
        elif position == "center":
            crop_x, crop_y = center_x, center_y
        elif position == "bottom-center":
            crop_x, crop_y = center_x, bottom_y
        elif position == "bottom-right":
            crop_x, crop_y = right_x, bottom_y

        # Ensure crop origin stays within canvas
        crop_x = clamp(crop_x, 0, max(0, canvas_w - 1))
        crop_y = clamp(crop_y, 0, max(0, canvas_h - 1))

        cropped_image = cropper.crop(canvas, int(target_width), int(target_height), int(crop_x), int(crop_y))

        return (cropped_image[0],)

class InoConditionBooleanMulti:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 2, "max": 1000, "step": 1}),
                "condition": ( ["AND", "OR"], {}),
                "bool_1": ("BOOLEAN", {"default": True, "forceInput": True}),
            },
            "optional": {
                "bool_2": ("BOOLEAN", {"default": False, "forceInput": True}),
            }
    }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("bool",)
    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, inputcount, condition, **kwargs):
        bool_1 = kwargs["bool_1"]
        bools = []
        for c in range(1, inputcount):
            val = kwargs.get(f"bool_{c + 1}", None)
            if val is None:
                continue
            bools.append(bool(val))

        if bool_1 is not None:
            bools.insert(0, bool(bool_1))

        if not bools:
            return (False,)

        if condition == "AND":
            result = all(bools)
        elif condition == "OR":
            result = any(bools)
        else:
            return (False,)

        return (result,)


LOCAL_NODE_CLASS = {
    "InoNotBoolean": InoNotBoolean,
    "InoIntEqual": InoIntEqual,
    "InoStringToggleCase": InoStringToggleCase,
    "InoBoolToSwitch": InoBoolToSwitch,
    "InoStringToCombo": InoStringToCombo,
    "InoDateTimeAsString": InoDateTimeAsString,
    "InoRandomIntInRange": InoRandomIntInRange,
    "InoIntToString": InoIntToString,
    "InoIntToFloat": InoIntToFloat,
    "InoFloatToInt": InoFloatToInt,
    "InoSaveImages": InoSaveImages,
    "InoImageResizeByLongerSideV1": InoImageResizeByLongerSideV1,
    "InoImageResizeByLongerSideAndCropV2": InoImageResizeByLongerSideAndCropV2,
    "InoConditionBooleanMulti": InoConditionBooleanMulti,
}
LOCAL_NODE_NAME = {
    "InoNotBoolean": "Ino Not Boolean",
    "InoIntEqual": "Ino Int Equal",
    "InoStringToggleCase": "Ino String Toggle Case",
    "InoBoolToSwitch": "Ino Bool To Switch",
    "InoStringToCombo": "Ino String To Combo",
    "InoDateTimeAsString": "Ino DateTime As String",
    "InoRandomIntInRange": "Ino Random Int In Range",
    "InoIntToString": "Ino Int To String",
    "InoIntToFloat": "Ino Int To Float",
    "InoFloatToInt": "Ino Float To Int",
    "InoSaveImages": "Ino Save Images",
    "InoImageResizeByLongerSideV1": "Ino Image Resize By Longer Side V1",
    "InoImageResizeByLongerSideAndCropV2": "Ino Image Resize By Longer Side And Crop V2",
    "InoConditionBooleanMulti": "Ino Condition Boolean Multi",
}
