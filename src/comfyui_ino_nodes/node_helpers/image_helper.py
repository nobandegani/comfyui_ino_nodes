import torch
import os

from torchvision.transforms import InterpolationMode
import torchvision.transforms.functional as TorchFunctional
from datetime import datetime, timezone, timedelta

import folder_paths
from comfy_api.latest import ComfyExtension, io

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

    RETURN_TYPES = ("BOOLEAN", "STRING" , "INT", "STRING", )
    RETURN_NAMES = ("Success", "Result", "NumberOfImages", "DateTimeIso", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, images, filename_prefix):
        time_now = datetime.now(timezone.utc).isoformat()

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

        if len(results) == 0:
            return (False, "", 0, )

        return (True, names, len(results), time_now)

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

class InoLoadImagesFromFolder(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoLoadImagesFromFolder",
            display_name="Ino Load Images From Folder",
            category="InoNodes",
            inputs=[
                io.Combo.Input(
                    "parent_folder",
                    options=["input", "output", "temp"]
                ),
                io.String.Input(
                    "folder",
                ),
                io.Int.Input(
                    "load_cap",
                    default=0,
                    min=0,
                    max=10000
                ),
                io.Int.Input(
                    "skip_from_first",
                    default=0,
                    min=0,
                    max=10000
                )
            ],
            outputs=[
                io.Image.Output(
                    display_name="images",
                    is_output_list=True,
                    tooltip="List of loaded images",
                ),
                io.Int.Output(
                    display_name="number of images",
                )
            ],
        )

    @classmethod
    def execute(cls, parent_folder, folder, load_cap, skip_from_first):
        from comfy_extras.nodes_dataset import load_and_process_images
        if parent_folder == "input":
            sub_input_dir = os.path.join(folder_paths.get_input_directory(), folder)
        elif parent_folder == "output":
            sub_input_dir = os.path.join(folder_paths.get_output_directory(), folder)
        else:
            sub_input_dir = os.path.join(folder_paths.get_temp_directory(), folder)

        valid_extensions = [".png", ".jpg", ".jpeg", ".webp"]
        image_files = [
            f
            for f in os.listdir(sub_input_dir)
            if any(f.lower().endswith(ext) for ext in valid_extensions)
        ]

        image_files = sorted(image_files)

        skip_from_first = max(0, int(skip_from_first))
        load_cap = max(0, int(load_cap))

        if skip_from_first:
            image_files = image_files[skip_from_first:]

        if load_cap > 0:
            image_files = image_files[:load_cap]
        
        output_tensor = load_and_process_images(image_files, sub_input_dir)
        return io.NodeOutput(output_tensor, len(output_tensor))

LOCAL_NODE_CLASS = {
    "InoSaveImages": InoSaveImages,
    "InoImageResizeByLongerSideV1": InoImageResizeByLongerSideV1,
    "InoImageResizeByLongerSideAndCropV2": InoImageResizeByLongerSideAndCropV2,
    "InoLoadImagesFromFolder": InoLoadImagesFromFolder,
}
LOCAL_NODE_NAME = {
    "InoSaveImages": "Ino Save Images",
    "InoImageResizeByLongerSideV1": "Ino Image Resize By Longer Side V1",
    "InoImageResizeByLongerSideAndCropV2": "Ino Image Resize By Longer Side And Crop V2",
    "InoLoadImagesFromFolder": "Ino Load Images From Folder",
}
