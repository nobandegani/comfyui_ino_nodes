from inspect import cleandoc

import os

class InoParseFilePath:
    """
        return path, name, extension from full file path
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {
                    "multiline": False,
                    "default": "C:/Local/Programs/5774150451195922272.jpg"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("path", "file name", "extension")
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass


    def function(self, file_path):
        # Normalize the path
        file_path = os.path.normpath(file_path)

        # Split path and file name
        dir_path = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)

        # Split file name and extension
        name, ext = os.path.splitext(base_name)
        ext = ext.lstrip(".")  # Remove leading dot

        return (dir_path, name, ext)



class InoNotBoolean:
    """
        reverse boolean
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "BOOLEAN": ("BOOLEAN")
            }
        }

    RETURN_TYPES = ("BOOLEAN")
    RETURN_NAMES = ("BOOLEAN", )
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass


    def function(self, BOOLEAN):
        return (not BOOLEAN)


class InoCountFiles:
    """
        count files in folder
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {
                    "multiline": False,
                    "default": "test"
                }),
                "file_pattern": ("STRING", {
                    "multiline": False,
                    "default": "*.*"
                }),
            }
        }

    RETURN_TYPES = ("INT")
    RETURN_NAMES = ("file count", )
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass


    def function(self, file_path, file_pattern):
        return (6)
