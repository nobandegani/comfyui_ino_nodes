import json
from copy import deepcopy

from inopyutils import InoJsonHelper

from ..node_helper import any_typ

class InoJson:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "base_json": ("STRING", {"default": "{}"}),
                "field_name": ("STRING", {"default": ""}),
                "field_value": (any_typ,)
            }
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("Json", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, base_json, field_name, field_value):
        json_object = InoJsonHelper.string_to_dict(base_json)
        json_object[field_name] = field_value
        json_string = json.dumps(json_object)
        return (json_string, )

LOCAL_NODE_CLASS = {
    "InoJson": InoJson,
}
LOCAL_NODE_NAME = {
    "InoJson": "Ino Json",
}
