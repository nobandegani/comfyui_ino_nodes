import os
import random

import folder_paths
from comfy_api.latest import io, ui, Input, Types


class InoPreviewVideo:
    def __init__(self):
        self.prefix_append = "_temp_" + ''.join(random.choice("abcdefghijklmnopqrstupvxyz") for _ in range(5))

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "video": ("VIDEO",),
            },
            "optional": {
                "format": (("mp4", "webm", "auto"), {"default": "mp4"}),
                "codec": (("h264", "auto"), {"default": "h264"}),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "function"
    CATEGORY = "InoNodes"
    OUTPUT_NODE = True

    def function(self, enabled, video: Input.Video, format="mp4", codec="h264"):
        if not enabled:
            return {"ui": ui.PreviewVideo([]).as_dict()}

        width, height = video.get_dimensions()
        full_output_folder, filename, counter, subfolder, _ = folder_paths.get_save_image_path(
            "ComfyUI" + self.prefix_append, folder_paths.get_temp_directory(), width, height
        )

        file = f"{filename}_{counter:05}_.{Types.VideoContainer.get_extension(format)}"
        video.save_to(
            os.path.join(full_output_folder, file),
            format=Types.VideoContainer(format),
            codec=codec,
        )

        return {"ui": ui.PreviewVideo([ui.SavedResult(file, subfolder, io.FolderType.temp)]).as_dict()}


LOCAL_NODE_CLASS = {"InoPreviewVideo": InoPreviewVideo}
LOCAL_NODE_NAME = {"InoPreviewVideo": "Ino Preview Video"}
