import hashlib
from pathlib import Path
from inspect import cleandoc

from inopyutils import file_helper, InoFileHelper

from ..node_helper import PARENT_FOLDER_OPTIONS, resolve_comfy_path


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
            return ("",)

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
                "source_parent_folder": (PARENT_FOLDER_OPTIONS,),
                "source_folder": ("STRING", {"default": ""}),
                "parent_folder": (PARENT_FOLDER_OPTIONS,),
                "folder": ("STRING", {"default": ""}),
                "filename": ("STRING", {"default": "archive.zip"}),
            },
            "optional": {
                "dummy_string": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("success", "message", "rel_path", "abs_path")

    DESCRIPTION = cleandoc(__doc__)

    FUNCTION = "function"
    OUTPUT_NODE = True

    CATEGORY = "InoFileHelper"

    async def function(self, enabled, seed, source_parent_folder, source_folder, parent_folder, folder, filename, dummy_string=None):
        if not enabled:
            return (False, "Node is disabled", "", "")

        _, source_abs = resolve_comfy_path(source_parent_folder, source_folder)
        rel_path, abs_path = resolve_comfy_path(parent_folder, folder, filename)

        Path(abs_path).parent.mkdir(parents=True, exist_ok=True)

        res = await InoFileHelper.zip(
            to_zip=source_abs,
            path_to_save=str(Path(abs_path).parent),
            zip_file_name=Path(abs_path).name
        )
        return (res["success"], res["msg"], rel_path, abs_path)


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
                "source_parent_folder": (PARENT_FOLDER_OPTIONS,),
                "source_folder": ("STRING", {"default": ""}),
                "source_filename": ("STRING", {"default": "archive.zip"}),
                "parent_folder": (PARENT_FOLDER_OPTIONS,),
                "folder": ("STRING", {"default": ""}),
            },
            "optional": {
                "dummy_string": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("success", "message", "rel_path", "abs_path")

    DESCRIPTION = cleandoc(__doc__)

    FUNCTION = "function"
    OUTPUT_NODE = True

    CATEGORY = "InoFileHelper"

    async def function(self, enabled, seed, source_parent_folder, source_folder, source_filename, parent_folder, folder, dummy_string=None):
        if not enabled:
            return (False, "Node is disabled", "", "")

        _, zip_abs = resolve_comfy_path(source_parent_folder, source_folder, source_filename)
        rel_path, abs_path = resolve_comfy_path(parent_folder, folder)

        res = await InoFileHelper.unzip(
            zip_path=zip_abs,
            output_path=abs_path
        )
        return (res["success"], res["msg"], rel_path, abs_path)

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
                "parent_folder": (PARENT_FOLDER_OPTIONS,),
                "folder": ("STRING", {"default": ""}),
                "filename": ("STRING", {"default": ""}),
            },
            "optional": {
                "dummy_string": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("success", "message", "rel_path", "abs_path")

    DESCRIPTION = cleandoc(__doc__)

    FUNCTION = "function"
    OUTPUT_NODE = True

    CATEGORY = "InoFileHelper"

    async def function(self, enabled, seed, parent_folder, folder, filename, dummy_string=None):
        if not enabled:
            return (False, "Node is disabled", "", "")

        rel_path, abs_path = resolve_comfy_path(parent_folder, folder, filename)

        res = await InoFileHelper.remove_file(
            file_path=abs_path
        )
        return (res["success"], res["msg"], rel_path, abs_path)

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
                "parent_folder": (PARENT_FOLDER_OPTIONS,),
                "folder": ("STRING", {"default": ""}),
            },
            "optional": {
                "dummy_string": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("success", "message", "rel_path", "abs_path")

    DESCRIPTION = cleandoc(__doc__)

    FUNCTION = "function"
    OUTPUT_NODE = True

    CATEGORY = "InoFileHelper"

    async def function(self, enabled, seed, parent_folder, folder, dummy_string=None):
        if not enabled:
            return (False, "Node is disabled", "", "")

        rel_path, abs_path = resolve_comfy_path(parent_folder, folder)

        res = await InoFileHelper.remove_folder(
            folder_path=Path(abs_path)
        )
        return (res["success"], res["msg"], rel_path, abs_path)

class InoCopyFiles:
    """
        Ino Copy Files
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "from_parent_folder": (PARENT_FOLDER_OPTIONS,),
                "from_folder": ("STRING", {"default": ""}),
                "to_parent_folder": (PARENT_FOLDER_OPTIONS,),
                "to_folder": ("STRING", {"default": ""}),
                "iterate_subfolders": ("BOOLEAN", {"default": True}),
                "rename_files": ("BOOLEAN", {"default": True}),
                "prefix_name": ("STRING", {"default": "file"}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("success", "message", "rel_path", "abs_path", "logs", )

    FUNCTION = "function"
    OUTPUT_NODE = True

    CATEGORY = "InoFileHelper"

    async def function(self, enabled, from_parent_folder, from_folder, to_parent_folder, to_folder, iterate_subfolders, rename_files, prefix_name):
        if not enabled:
            return (False, "Node is disabled", "", "", "")

        _, from_abs = resolve_comfy_path(from_parent_folder, from_folder)
        rel_path, abs_path = resolve_comfy_path(to_parent_folder, to_folder)

        res = await InoFileHelper.copy_files(
            to_path=Path(abs_path),
            from_path=Path(from_abs),
            iterate_subfolders=iterate_subfolders,
            rename_files=rename_files,
            prefix_name=prefix_name,
        )
        return (res["success"], res["msg"], rel_path, abs_path, res["logs"], )

class InoCountFiles:
    """
        Count File
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "parent_folder": (PARENT_FOLDER_OPTIONS,),
                "folder": ("STRING", {"default": ""}),
                "recursive": ("BOOLEAN", {"default": True}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "INT", )
    RETURN_NAMES = ("success", "message", "rel_path", "abs_path", "count", )

    FUNCTION = "function"

    CATEGORY = "InoFileHelper"

    async def function(self, enabled, parent_folder, folder, recursive):
        if not enabled:
            return (False, "Node is disabled", "", "", 0)

        rel_path, abs_path = resolve_comfy_path(parent_folder, folder)

        res = await InoFileHelper.count_files(
            path=Path(abs_path),
            recursive=recursive
        )
        return (res["success"], res["msg"], rel_path, abs_path, res["count"], )

class InoValidateMediaFiles:
    """
        Validate Media Files
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "parent_folder": (PARENT_FOLDER_OPTIONS,),
                "folder": ("STRING", {"default": ""}),
                "include_images": ("BOOLEAN", {"default": True}),
                "include_videos": ("BOOLEAN", {"default": True}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("success", "message", "rel_path", "abs_path", "skipped_images_path", "skipped_images_unsupported_path", "skipped_videos_path", "skipped_videos_unsupported_path", "unsupported_files_path", "logs", "output_path", )

    FUNCTION = "function"

    CATEGORY = "InoFileHelper"

    async def function(self, enabled, parent_folder, folder, include_images, include_videos):
        if not enabled:
            return (False, "Node is disabled", "", "", "", "", "", "", "", "", "")

        rel_path, abs_path = resolve_comfy_path(parent_folder, folder)

        res = await InoFileHelper.validate_files(
            input_path=Path(abs_path),
            include_image=include_images,
            include_video=include_videos,
        )
        return (True, res.get("msg"), rel_path, abs_path, res.get("skipped_images_path"), res.get("skipped_images_unsupported_path"), res.get("skipped_videos_path"), res.get("skipped_videos_unsupported_path"), res.get("unsupported_files_path"), res.get("logs"), abs_path,)

class InoRemoveDuplicateFiles:
    """
        Remove Duplicate Files
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "parent_folder": (PARENT_FOLDER_OPTIONS,),
                "folder": ("STRING", {"default": ""}),
                "recursive": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "chunk_size": ("INT", {"default": 32, "min": 8, "max": 1024, "step": 8,}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING", "INT", )
    RETURN_NAMES = ("success", "message", "rel_path", "abs_path", "removed_list", "removed_count", )

    FUNCTION = "function"
    OUTPUT_NODE = True

    CATEGORY = "InoFileHelper"

    async def function(self, enabled, parent_folder, folder, recursive, chunk_size=32):
        if not enabled:
            return (False, "Node is disabled", "", "", "", 0)

        rel_path, abs_path = resolve_comfy_path(parent_folder, folder)

        res = await InoFileHelper.remove_duplicate_files(
            input_path=Path(abs_path),
            recursive=recursive,
            chunk_size=chunk_size
        )
        return (res["success"], res["msg"], rel_path, abs_path, res["removed"], res["removed_count"], )

LOCAL_NODE_CLASS = {
    "InoIncrementBatchName": InoIncrementBatchName,
    "InoZip": InoZip,
    "InoUnzip": InoUnzip,
    "InoRemoveFile": InoRemoveFile,
    "InoRemoveFolder": InoRemoveFolder,
    "InoCopyFiles": InoCopyFiles,
    "InoCountFiles": InoCountFiles,
    "InoValidateMediaFiles": InoValidateMediaFiles,
    "InoRemoveDuplicateFiles": InoRemoveDuplicateFiles,
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
    "InoRemoveDuplicateFiles": "Ino Remove Duplicate Files",
}
