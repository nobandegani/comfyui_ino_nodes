import hashlib
from pathlib import Path
from inspect import cleandoc

from inopyutils import file_helper, InoFileHelper


class InoIncrementBatchName:
    """
        Increment Batch Name
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
                    "label": "Seed (0 = random)",
                    "control_after_generate": True,
                }),
                "name": ("STRING", {
                    "multiline": False,
                    "default": "Batch_00001"
                }),
            },
            "optional": {
                "dummy_string": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("string", )

    DESCRIPTION = cleandoc(__doc__)

    FUNCTION = "function"

    CATEGORY = "InoFileHelper"

    async def function(self, enabled, seed, name, dummy_string):
        if not enabled:
            return "Disabled", "Node is disabled", ""

        return InoFileHelper.increment_batch_name(name= name)

class InoZip:
    """
        Zip
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
                    "label": "Seed (0 = random)",
                    "control_after_generate": True,
                }),
                "to_zip": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "path_to_save": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "zip_file_name": ("STRING", {
                    "multiline": False,
                    "default": ""
                })
            },
            "optional": {
                "dummy_string": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING")
    RETURN_NAMES = ("success", "message", "other")

    DESCRIPTION = cleandoc(__doc__)

    FUNCTION = "function"

    CATEGORY = "InoFileHelper"

    async def function(self, enabled, seed, to_zip, path_to_save, zip_file_name, dummy_string):
        if not enabled:
            return "Disabled", "Node is disabled", ""

        res = await InoFileHelper.zip(
            to_zip=to_zip,
            path_to_save=path_to_save,
            zip_file_name=zip_file_name
        )
        return res["success"], res["msg"], res


class InoUnzip:
    """
        Unzip
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
                    "label": "Seed (0 = random)",
                    "control_after_generate": True,
                }),
                "zip_path": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "output_path": ("STRING", {
                    "multiline": False,
                    "default": ""
                })
            },
            "optional": {
                "dummy_string": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING")
    RETURN_NAMES = ("success", "message", "other")

    DESCRIPTION = cleandoc(__doc__)

    FUNCTION = "function"

    CATEGORY = "InoFileHelper"

    async def function(self, enabled, seed, zip_path, output_path, dummy_string):
        if not enabled:
            return "Disabled", "Node is disabled", ""

        res = await InoFileHelper.unzip(
            zip_path=zip_path,
            output_path=output_path
        )
        return res["success"], res["msg"], res

class InoRemoveFile:
    """
        Remove File
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
                    "label": "Seed (0 = random)",
                    "control_after_generate": True,
                }),
                "file_path": ("STRING", {
                    "multiline": False,
                    "default": ""
                })
            },
            "optional": {
                "dummy_string": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING")
    RETURN_NAMES = ("success", "message", "other")

    DESCRIPTION = cleandoc(__doc__)

    FUNCTION = "function"

    CATEGORY = "InoFileHelper"

    async def function(self, enabled, seed, file_path, dummy_string):
        if not enabled:
            return "Disabled", "Node is disabled", ""

        res = await InoFileHelper.remove_file(
            file_path=file_path
        )
        return res["success"], res["msg"], res

class InoRemoveFolder:
    """
        Remove Folder
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
                    "label": "Seed (0 = random)",
                    "control_after_generate": True,
                }),
                "folder_path": ("STRING", {
                    "multiline": False,
                    "default": ""
                })
            },
            "optional": {
                "dummy_string": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING")
    RETURN_NAMES = ("success", "message", "other")

    DESCRIPTION = cleandoc(__doc__)

    FUNCTION = "function"

    CATEGORY = "InoFileHelper"

    async def function(self, enabled, seed, folder_path, dummy_string):
        if not enabled:
            return "Disabled", "Node is disabled", ""

        res = await InoFileHelper.remove_folder(
            folder_path=Path(folder_path)
        )
        return res["success"], res["msg"], res

class InoCopyFiles:
    """
        Ino Copy Files
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "from_path": ("STRING", {"default": ""}),
                "to_path": ("STRING", {"default": ""}),
                "iterate_subfolders": ("BOOLEAN", {"default": True}),
                "rename_files": ("BOOLEAN", {"default": True}),
                "prefix_name": ("STRING", {"default": "file"}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", )
    RETURN_NAMES = ("success", "message", "logs", )

    FUNCTION = "function"

    CATEGORY = "InoFileHelper"

    async def function(self, enabled, from_path, to_path, iterate_subfolders, rename_files, prefix_name):
        if not enabled:
            return ("Disabled", "Node is disabled", "", )

        res = await InoFileHelper.copy_files(
            to_path=Path(to_path),
            from_path=Path(from_path),
            iterate_subfolders=iterate_subfolders,
            rename_files=rename_files,
            prefix_name=prefix_name,
        )
        return (res["success"], res["msg"], res["logs"], )

class InoCountFiles:
    """
        Count File
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "folder_path": ("STRING", {
                    "default": ""
                }),
                "recursive": ("BOOLEAN", {"default": True}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "INT", )
    RETURN_NAMES = ("success", "message", "count", )

    FUNCTION = "function"

    CATEGORY = "InoFileHelper"

    async def function(self, enabled, folder_path, recursive):
        if not enabled:
            return (False, "Node is disabled", "")

        res = await InoFileHelper.count_files(
            path=Path(folder_path),
            recursive=recursive
        )
        return (res["success"], res["msg"], res["count"], )

class InoValidateMediaFiles:
    """
        Validate Media Files
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "input_path": ("STRING", {"default": ""}),
                "include_images": ("BOOLEAN", {"default": True}),
                "include_videos": ("BOOLEAN", {"default": True}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("success", "message", "skipped_images_path", "skipped_images_unsupported_path", "skipped_videos_path", "skipped_videos_unsupported_path", "unsupported_files_path", "logs", )

    FUNCTION = "function"

    CATEGORY = "InoFileHelper"

    async def function(self, enabled, input_path, include_images, include_videos):
        if not enabled:
            return (False, "Node is disabled", "", "", "", "", "", "",)

        res = await InoFileHelper.validate_files(
            input_path=Path(input_path),
            include_image=include_images,
            include_video=include_videos,
        )
        return (True, res.get("msg"), res.get("skipped_images_path"), res.get("skipped_images_unsupported_path"), res.get("skipped_videos_path"), res.get("skipped_videos_unsupported_path"), res.get("unsupported_files_path"), res.get("logs"),)

LOCAL_NODE_CLASS = {
    "InoIncrementBatchName": InoIncrementBatchName,
    "InoZip": InoZip,
    "InoUnzip": InoUnzip,
    "InoRemoveFile": InoRemoveFile,
    "InoRemoveFolder": InoRemoveFolder,
    "InoCopyFiles": InoCopyFiles,
    "InoCountFiles": InoCountFiles,
    "InoValidateMediaFiles": InoValidateMediaFiles,
}
LOCAL_NODE_NAME = {
    "InoIncrementBatchName": "Ino Increment Batch Name",
    "InoZip": "Ino Zip",
    "InoUnzip": "Ino Unzip",
    "InoRemoveFile": "Ino Remove File",
    "InoRemoveFolder": "Ino Remove Folder",
    "InoCopyFiles": "Ino Copy Files",
    "InoCountFiles": "Ino Count Files",
    "InoValidateMediaFiles": "Ino Validate Media Files",
}
