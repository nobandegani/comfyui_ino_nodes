import json
from copy import deepcopy
from pathlib import Path

import folder_paths

from inopyutils import InoJsonHelper

from ..node_helper import any_type, ino_print_log


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
        try:
            json_object = InoJsonHelper.string_to_dict(base_json)
            if not json_object["success"]:
                ino_print_log("InoJsonSetField", json_object["msg"])
                return (False, json_object["msg"], "", )
            json_object = json_object["data"]

            json_object[field_name] = field_value
            json_string = InoJsonHelper.dict_to_string(json_object)
            if not json_string["success"]:
                ino_print_log("InoJsonSetField", json_string["msg"])
                return (False, json_string["msg"], "", )

            base_json = json_string["data"]
            ino_print_log("InoJsonSetField", "Success")
            return (True, "Success", base_json, )
        except Exception as e:
            ino_print_log("InoJsonSetField", "",str(e))
            return (False, f"failed: {e}", "",)

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
        try:
            json_object = InoJsonHelper.string_to_dict(base_json)
            if not json_object["success"]:
                ino_print_log("InoJsonGetField", json_object["msg"])
                return (False, json_object["msg"], "", )
            json_object = json_object["data"]

            ino_print_log("InoJsonGetField", "Success")
            return (True, "Success", json_object[field_name], )
        except Exception as e:
            ino_print_log("InoJsonGetField", "",str(e))
            return (False, f"failed: {e}", "",)

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
        try:
            output_path = folder_paths.get_output_directory()
            save_path :Path = Path(output_path) / Path(local_path)
            save_json = await InoJsonHelper.save_string_as_json_async(
                json_string=json_string,
                file_path=str(save_path.resolve())
            )

            if not save_json["success"]:
                ino_print_log("InoSaveJson", save_json["msg"])
                return (False, save_json["msg"],)

            ino_print_log("InoSaveJson", "Success")
            return (True, save_json["msg"], )
        except Exception as e:
            ino_print_log("InoSaveJson", "",str(e))
            return (False, f"failed: {e}", "",)

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
