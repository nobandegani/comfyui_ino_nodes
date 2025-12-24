import re
import hashlib
import base64

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

class InoStringReplaceSimple2:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_string": ("STRING", {"default": "Test string"}),
                "replace_from": ("STRING", {"default": "Test"}),
                "replace_to": ("STRING", {"default": "Example"}),
            }
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("string", )

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, input_string, replace_from, replace_to):
        result = input_string.replace(replace_from, replace_to)
        return (result, )

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

class InoStringToAlphabeticString:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_string": ("STRING", {"default": "mjp043n85se4z"}),
                "length": ("INT", {"default": 8}),
            }
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("string", )

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, input_string, length):
        if input_string is None:
            return ""

        alphabet = "abcdefghijklmnopqrstuvwxyz"
        digest = hashlib.sha256(input_string.encode()).digest()
        b32 = base64.b32encode(digest).decode().lower().rstrip("=")

        result_chars = []
        for ch in b32:
            if 'a' <= ch <= 'z':
                idx = ord(ch) - ord('a')
            else:  # '2'..'7'
                idx = (ord(ch) - ord('2')) % 26
            result_chars.append(alphabet[idx])
            if len(result_chars) == length:
                break

        alphbetic_string = "".join(result_chars)

        return (alphbetic_string, )

LOCAL_NODE_CLASS = {
    "InoStringToggleCase": InoStringToggleCase,
    "InoStringReplaceSimple": InoStringReplaceSimple,
    "InoStringReplaceSimple2": InoStringReplaceSimple2,
    "InoStringStripSimple": InoStringStripSimple,
    "InoStringToAlphabeticString": InoStringToAlphabeticString,
}
LOCAL_NODE_NAME = {
    "InoStringToggleCase": "Ino String Toggle Case",
    "InoStringReplaceSimple": "Ino String Replace Simple",
    "InoStringReplaceSimple2": "Ino String Replace Simple2",
    "InoStringStripSimple": "Ino String Strip Simple",
    "InoStringToAlphabeticString": "Ino String To Alphabetic String",
}
