from inspect import cleandoc

import os
import re
import random
import hashlib

from pathlib import Path

#---------------------------------InoParseFilePath
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


#---------------------------------InoCountFiles
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


#---------------------------------InoImageBranch
class InoBranchImage:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "boolean": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "input_image": ("IMAGE", ),
            },
        }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("output_image", )
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass


    def function(self, boolean, input_image=None):
        if boolean:
            return (input_image, )
        else:
            return (input_image, )


class InoGetFolderBatchID:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "step": 1,
                    "label": "Seed (0 = random)"
                }),
                "batch_type": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "creator_name": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "get_last_one": ("BOOLEAN", {
                    "default": True
                }),
            },
            "optional": {
                "parent_path": ("STRING", {
                    "multiline": False,
                    "default": "ComfyUI/output/Assets"
                }),
            }
        }

    RETURN_TYPES = ("INT", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("Batch ID", "Batch ID String", "Batch ID Path Rel", "Batch ID Path Abs")
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        m = hashlib.sha256()
        m.update(seed)
        return m.digest().hex()

    def function(self, enabled, seed, batch_type, creator_name, get_last_one, parent_path):
        if not enabled:
            return 0, "", ""
        seed_number = random.seed(seed)

        input_path = Path(parent_path) / creator_name / batch_type
        input_path = input_path.resolve()
        input_path.mkdir(parents=True, exist_ok=True)

        batch_id_folders = [
            folder.name for folder in input_path.iterdir()
            if folder.is_dir() and re.match(r'Batch_\d{3}', folder.name)
        ]

        if batch_id_folders:
            last_batch_num = max(int(re.search(r'\d{3}', name).group()) for name in batch_id_folders)
            if get_last_one:
                final_batch_num = last_batch_num
            else:
                final_batch_num = last_batch_num + 1
        else:
            final_batch_num = 1

        final_batch_str = f"Batch_{final_batch_num:03}"
        final_batch_abs_path = (input_path / final_batch_str).resolve()

        final_batch_rel_path = final_batch_abs_path.relative_to(Path(Path(parent_path).parent).resolve())

        return final_batch_num, final_batch_str, str(final_batch_rel_path), str(final_batch_abs_path)


LOCAL_NODE_CLASS = {
    "InoParseFilePath": InoParseFilePath,
    "InoCountFiles": InoCountFiles,
    "InoBranchImage": InoBranchImage,
    "InoGetFolderBatchID": InoGetFolderBatchID,
}
LOCAL_NODE_NAME = {
    "InoParseFilePath": "Ino Parse File Path",
    "InoCountFiles": "Ino Count Files",
    "InoBranchImage": "Ino Branch Image",
    "InoGetFolderBatchID": "Ino Get Folder Batch ID",
}
