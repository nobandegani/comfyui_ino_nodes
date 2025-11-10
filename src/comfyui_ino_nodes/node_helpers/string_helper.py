import re

class InoStringToggleCase:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "input_string": ("STRING", {
                    "multiline": True,
                    "default": "Test String"
                }),
                "toggle_to": ("BOOLEAN", {"default": True, "label_off": "Lower", "label_on": "Upper"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("String",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, enabled, input_string, toggle_to):
        if not enabled:
            return input_string
        result = str(input_string).upper() if toggle_to else str(input_string).lower()
        return (result,)


class InoStringReplaceSimple:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_string": ("STRING", {"default": "Test {String}"}),
                "replace_string": ("STRING", {"default": "Replaced"}),
            }
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("string", )

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, input_string, replace_string):
        return (re.sub(r"\{[^}]*\}", replace_string, input_string), )

class InoStringStripSimple:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_string": ("STRING", {"default": "Test {String}"}),
                "strip_string": ("STRING", {"default": "'[]{}()-_+="}),
            }
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("string", )

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, input_string, strip_string):
        if input_string is None:
            return ""

        translation_table = str.maketrans("", "", strip_string)
        return (input_string.translate(translation_table), )

LOCAL_NODE_CLASS = {
    "InoStringToggleCase": InoStringToggleCase,
    "InoStringReplaceSimple": InoStringReplaceSimple,
    "InoStringStripSimple": InoStringStripSimple,
}
LOCAL_NODE_NAME = {
    "InoStringToggleCase": "Ino String Toggle Case",
    "InoStringReplaceSimple": "Ino String Replace Simple",
    "InoStringStripSimple": "Ino String Strip Simple",
}
