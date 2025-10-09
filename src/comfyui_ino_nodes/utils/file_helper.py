import hashlib
from inspect import cleandoc

from inopyutils import file_helper, InoFileHelper


class IncrementBatchName:
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
                    "label": "Seed (0 = random)"
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

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        m = hashlib.sha256()
        m.update(seed)
        return m.digest().hex()

    async def function(self, enabled, seed, name, dummy_string):
        if not enabled:
            return "Disabled", "Node is disabled", ""

        return InoFileHelper.increment_batch_name(name= name)

class Zip:
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
                    "label": "Seed (0 = random)"
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

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        m = hashlib.sha256()
        m.update(seed)
        return m.digest().hex()

    async def function(self, enabled, seed, to_zip, path_to_save, zip_file_name, dummy_string):
        if not enabled:
            return "Disabled", "Node is disabled", ""

        res = await InoFileHelper.zip(
            to_zip=to_zip,
            path_to_save=path_to_save,
            zip_file_name=zip_file_name
        )
        return res["success"], res["msg"], res


class Unzip:
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
                    "label": "Seed (0 = random)"
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

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        m = hashlib.sha256()
        m.update(seed)
        return m.digest().hex()

    async def function(self, enabled, seed, zip_path, output_path, dummy_string):
        if not enabled:
            return "Disabled", "Node is disabled", ""

        res = await InoFileHelper.unzip(
            zip_path=zip_path,
            output_path=output_path
        )
        return res["success"], res["msg"], res

class RemoveFile:
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
                    "label": "Seed (0 = random)"
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

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        m = hashlib.sha256()
        m.update(seed)
        return m.digest().hex()

    async def function(self, enabled, seed, file_path, dummy_string):
        if not enabled:
            return "Disabled", "Node is disabled", ""

        res = await InoFileHelper.remove_file(
            file_path=file_path
        )
        return res["success"], res["msg"], res

class RemoveFolder:
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
                    "label": "Seed (0 = random)"
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

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        m = hashlib.sha256()
        m.update(seed)
        return m.digest().hex()

    async def function(self, enabled, seed, folder_path, dummy_string):
        if not enabled:
            return "Disabled", "Node is disabled", ""

        res = await InoFileHelper.remove_folder(
            folder_path=folder_path
        )
        return res["success"], res["msg"], res

LOCAL_NODE_CLASS = {
    "IncrementBatchName": IncrementBatchName,
    "Zip": Zip,
    "Unzip": Unzip,
    "RemoveFile": RemoveFile,
    "RemoveFolder": RemoveFolder,
}
LOCAL_NODE_NAME = {
    "IncrementBatchName": "Increment Batch Name",
    "Zip": "Zip",
    "Unzip": "Unzip",
    "RemoveFile": "Remove File",
    "RemoveFolder": "Remove Folder",
}
