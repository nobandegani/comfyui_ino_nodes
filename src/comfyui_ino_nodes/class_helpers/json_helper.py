import json
from copy import deepcopy
from pathlib import Path

import folder_paths

from inopyutils import InoJsonHelper

from ..node_helper import any_type

class InoJsonSetField:
    """
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "base_json": ("STRING", {"default": "{}"}),
                "field_name": ("STRING", {"default": ""}),
                "field_value": (any_type,)
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", )
    RETURN_NAMES = ("Success", "MSG", "Json", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, base_json, field_name, field_value):
        json_object = InoJsonHelper.string_to_dict(base_json)
        if not json_object["success"]:
            return (False, json_object["msg"], "", )
        json_object = json_object["data"]

        json_object[field_name] = field_value
        json_string = InoJsonHelper.dict_to_string(json_object)
        if not json_string["success"]:
            return (False, json_string["msg"], "", )

        base_json = json_string["data"]
        return (True, "Success", base_json, )

class InoJsonGetField:
    """
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "base_json": ("STRING", {"default": "{}"}),
                "field_name": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", any_type, )
    RETURN_NAMES = ("Success", "MSG", "Field_Value", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, base_json, field_name):
        json_object = InoJsonHelper.string_to_dict(base_json)
        if not json_object["success"]:
            return (False, json_object["msg"], "", )
        json_object = json_object["data"]

        return (True, "Success", json_object[field_name], )

class InoSaveJson:
    """
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "json_string": ("STRING", {"default": "{}"}),
                "local_path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", )
    RETURN_NAMES = ("Success", "MSG",  )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    async def function(self, json_string, local_path):
        output_path = folder_paths.get_output_directory()
        save_path :Path = Path(output_path) / Path(local_path)
        save_json = await InoJsonHelper.save_string_as_json_async(
            json_string=json_string,
            file_path=str(save_path.resolve())
        )
        return (save_json["success"], save_json["msg"], )

LOCAL_NODE_CLASS = {
    "InoJsonSetField": InoJsonSetField,
    "InoJsonGetField": InoJsonGetField,
    "InoSaveJson": InoSaveJson,
}
LOCAL_NODE_NAME = {
    "InoJsonSetField": "Ino Json Set Field",
    "InoJsonGetField": "Ino Json Get Field",
    "InoSaveJson": "Ino Save Json",
}
