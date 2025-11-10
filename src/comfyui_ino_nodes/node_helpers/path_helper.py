import folder_paths

class InoGetComfyPath:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder_type": (["input", "output", "temp"],),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("String",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, folder_type):
        if folder_type == "input":
            final_path = folder_paths.get_input_directory()
        elif folder_type == "output":
            final_path = folder_paths.get_output_directory()
        else:
            final_path = folder_paths.get_temp_directory()
        return (final_path,)


LOCAL_NODE_CLASS = {
    "InoGetComfyPath": InoGetComfyPath,
}
LOCAL_NODE_NAME = {
    "InoGetComfyPath": "Ino Get Comfy Path",
}
