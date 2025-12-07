from inopyutils import InoMediaHelper

class InoConvertVideo:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "input_path": ("STRING", {"multiline": False,"default": "" }),
                "output_path": ("STRING", {"multiline": False, "default": ""}),
                "change_fps": ("BOOLEAN", {"default": True}),
                "fps": ("INT", {"default": 30, "min": 1, "max": 1000}),
                "change_resolution": ("BOOLEAN", {"default": True}),
                "max_resolution": ("INT", {"default": 2560}),
            },
            "optional": {
                "dummy_string": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING",)
    RETURN_NAMES = ("success", "msg", "result",)

    FUNCTION = "function"

    CATEGORY = "InoMediaHelper"

    async def function(self, enabled, input_path, output_path, change_fps, fps, change_resolution, max_resolution):
        if not enabled:
            return (False, "Node is disabled", "",)

        convert = await InoMediaHelper.video_convert_ffmpeg(input_path, output_path, change_resolution, change_fps, max_resolution, fps)

        return (convert["success"], convert["msg"], convert, )

LOCAL_NODE_CLASS = {
    "InoConvertVideo": InoConvertVideo,
}
LOCAL_NODE_NAME = {
    "InoConvertVideo": "Ino Convert Video",
}
