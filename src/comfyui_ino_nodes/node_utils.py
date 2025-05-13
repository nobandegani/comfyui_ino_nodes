from inspect import cleandoc

import os
import fnmatch

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

    RETURN_TYPES = ("STRING", "STRING", "STRING", )
    RETURN_NAMES = ("path", "file name", "extension", )
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

        return (dir_path, name, ext, )



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
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass


    def function(self, boolean):
        return (not boolean, )


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

    RETURN_TYPES = ("INT", )
    RETURN_NAMES = ("file count", )
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass


    def function(self, file_path, file_pattern):
        # Normalize and verify
        file_path = os.path.normpath(file_path)
        if not os.path.isdir(file_path):
            return (-1,)

        all_files = os.listdir(file_path)
        pattern = file_pattern.lower()

        # Step 1: split the pattern
        if '.' in pattern:
            name_part, ext_part = pattern.split('.', 1)
            ext_part = ext_part.lower()
        else:
            name_part = pattern
            ext_part = None

        # Step 2: match filename by inclusion
        if name_part == "*":
            name_matches = all_files
        else:
            name_matches = [f for f in all_files if name_part in f.lower()]

        # Step 3: match extension (if any)
        if ext_part != "*":
            final_matches = [f for f in name_matches if f.lower().endswith(f".{ext_part}")]
        else:
            final_matches = name_matches

        return (len(final_matches),)
