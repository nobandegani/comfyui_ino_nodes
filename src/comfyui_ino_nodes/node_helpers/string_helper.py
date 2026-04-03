import os
import re
import hashlib
import base64
from pathlib import Path

import folder_paths

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
            return (input_string,)
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
            return ("",)

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
            return ("",)

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

class InoSaveText:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "text": ("STRING", {"multiline": True, "default": ""}),
                "parent_folder": (["input", "output", "temp"],),
                "folder": ("STRING", {"default": ""}),
                "file_name": ("STRING", {"default": "output.txt"}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING",)
    RETURN_NAMES = ("success", "message", "file_path",)

    FUNCTION = "function"

    OUTPUT_NODE = True

    CATEGORY = "InoNodes"

    def function(self, enabled, text, parent_folder, folder, file_name):
        if parent_folder == "input":
            base_dir = folder_paths.get_input_directory()
        elif parent_folder == "output":
            base_dir = folder_paths.get_output_directory()
        else:
            base_dir = folder_paths.get_temp_directory()

        save_dir = Path(base_dir) / folder
        file_path = str((save_dir / file_name).resolve())

        if not enabled:
            return (False, "not enabled", file_path,)
        try:
            save_dir.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
            return (True, "saved", file_path,)
        except Exception as e:
            return (False, str(e), file_path,)


LOCAL_NODE_CLASS = {
    "InoStringToggleCase": InoStringToggleCase,
    "InoStringReplaceSimple": InoStringReplaceSimple,
    "InoStringReplaceSimple2": InoStringReplaceSimple2,
    "InoStringStripSimple": InoStringStripSimple,
    "InoStringToAlphabeticString": InoStringToAlphabeticString,
    "InoSaveText": InoSaveText,
}
LOCAL_NODE_NAME = {
    "InoStringToggleCase": "Ino String Toggle Case",
    "InoStringReplaceSimple": "Ino String Replace Simple",
    "InoStringReplaceSimple2": "Ino String Replace Simple2",
    "InoStringStripSimple": "Ino String Strip Simple",
    "InoStringToAlphabeticString": "Ino String To Alphabetic String",
    "InoSaveText": "Ino Save Text",
}
