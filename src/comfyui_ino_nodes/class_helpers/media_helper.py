from pathlib import Path

from inopyutils import InoMediaHelper

from ..node_helper import PARENT_FOLDER_OPTIONS, resolve_comfy_path

class InoConvertVideoToMP4:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "input_parent_folder": (PARENT_FOLDER_OPTIONS,),
                "input_folder": ("STRING", {"default": ""}),
                "output_parent_folder": (PARENT_FOLDER_OPTIONS,),
                "output_folder": ("STRING", {"default": ""}),
            },
            "optional": {
                "change_fps": ("BOOLEAN", {"default": True}),
                "fps": ("INT", {"default": 30, "min": 1, "max": 1000}),
                "change_resolution": ("BOOLEAN", {"default": True}),
                "max_resolution": ("INT", {"default": 2560}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("success", "message", "rel_path", "abs_path",)

    FUNCTION = "function"
    OUTPUT_NODE = True

    CATEGORY = "InoMediaHelper"

    async def function(self, enabled, input_parent_folder, input_folder, output_parent_folder, output_folder, change_fps=True, fps=30, change_resolution=True, max_resolution=2560):
        if not enabled:
            return (False, "Node is disabled", "", "",)

        _, input_abs = resolve_comfy_path(input_parent_folder, input_folder)
        rel_path, abs_path = resolve_comfy_path(output_parent_folder, output_folder)

        convert = await InoMediaHelper.video_convert_ffmpeg(
            input_path=Path(input_abs),
            output_path=Path(abs_path),
            change_res=change_resolution,
            change_fps=change_fps,
            max_res=max_resolution,
            max_fps=fps
        )

        return (convert["success"], convert["msg"], rel_path, abs_path, )

LOCAL_NODE_CLASS = {
    "InoConvertVideoToMP4": InoConvertVideoToMP4,
}
LOCAL_NODE_NAME = {
    "InoConvertVideoToMP4": "Ino Convert Video To MP4",
}
