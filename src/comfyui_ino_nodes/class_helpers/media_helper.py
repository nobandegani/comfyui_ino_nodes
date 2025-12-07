from pathlib import Path

from inopyutils import InoMediaHelper

class InoConvertVideoToMP4:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "input_path": ("STRING", {"multiline": False,"default": "" }),
                "output_path": ("STRING", {"multiline": False, "default": ""}),
            },
            "optional": {
                "change_fps": ("BOOLEAN", {"default": True}),
                "fps": ("INT", {"default": 30, "min": 1, "max": 1000}),
                "change_resolution": ("BOOLEAN", {"default": True}),
                "max_resolution": ("INT", {"default": 2560}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING",)
    RETURN_NAMES = ("success", "msg", "result",)

    FUNCTION = "function"

    CATEGORY = "InoMediaHelper"

    async def function(self, enabled, input_path, output_path, change_fps, fps, change_resolution, max_resolution):
        if not enabled:
            return (False, "Node is disabled", "",)

        convert = await InoMediaHelper.video_convert_ffmpeg(
            input_path=Path(input_path),
            output_path=Path(output_path),
            change_res=change_resolution,
            change_fps=change_fps, 
            max_res=max_resolution,
            max_fps=fps
        )

        return (convert["success"], convert["msg"], convert, )

LOCAL_NODE_CLASS = {
    "InoConvertVideoToMP4": InoConvertVideoToMP4,
}
LOCAL_NODE_NAME = {
    "InoConvertVideoToMP4": "Ino Convert Video To MP4",
}
