import re
import hashlib
import base64
from pathlib import Path

from comfy_api.latest import io

from ..node_helper import PARENT_FOLDER_OPTIONS, resolve_comfy_path


class InoStringToggleCase(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoStringToggleCase",
            display_name="Ino String Toggle Case",
            category="InoStringHelper",
            description="Converts a string to upper or lower case.",
            inputs=[
                io.Boolean.Input("enabled", default=True, label_off="OFF", label_on="ON"),
                io.String.Input("input_string", default="Test String", multiline=True),
                io.Boolean.Input("toggle_to", default=True, label_off="Lower", label_on="Upper"),
            ],
            outputs=[
                io.String.Output(display_name="string"),
            ],
        )

    @classmethod
    def execute(cls, enabled, input_string, toggle_to) -> io.NodeOutput:
        if not enabled:
            return io.NodeOutput(input_string)
        result = str(input_string).upper() if toggle_to else str(input_string).lower()
        return io.NodeOutput(result)


class InoStringReplacePlaceholder(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoStringReplacePlaceholder",
            display_name="Ino String Replace Placeholder",
            category="InoStringHelper",
            description="Replaces all {placeholder} tokens in a string with the replacement value.",
            inputs=[
                io.String.Input("input_string", default="Test {String}"),
                io.String.Input("replace_string", default="Replaced"),
            ],
            outputs=[
                io.String.Output(display_name="string"),
            ],
        )

    @classmethod
    def execute(cls, input_string, replace_string) -> io.NodeOutput:
        return io.NodeOutput(re.sub(r"\{[^}]*\}", replace_string, input_string))


class InoStringReplace(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoStringReplace",
            display_name="Ino String Replace",
            category="InoStringHelper",
            description="Replaces all occurrences of a substring with another.",
            inputs=[
                io.String.Input("input_string", default="Test string"),
                io.String.Input("replace_from", default="Test"),
                io.String.Input("replace_to", default="Example"),
            ],
            outputs=[
                io.String.Output(display_name="string"),
            ],
        )

    @classmethod
    def execute(cls, input_string, replace_from, replace_to) -> io.NodeOutput:
        return io.NodeOutput(input_string.replace(replace_from, replace_to))


class InoStringStripSimple(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoStringStripSimple",
            display_name="Ino String Strip Simple",
            category="InoStringHelper",
            description="Removes all specified characters from a string.",
            inputs=[
                io.String.Input("input_string", default="Test {String}"),
                io.String.Input("strip_string", default="'[]{}()-_+="),
            ],
            outputs=[
                io.String.Output(display_name="string"),
            ],
        )

    @classmethod
    def execute(cls, input_string, strip_string) -> io.NodeOutput:
        if input_string is None:
            return io.NodeOutput("")
        translation_table = str.maketrans("", "", strip_string)
        return io.NodeOutput(input_string.translate(translation_table))


class InoStringToAlphabeticString(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoStringToAlphabeticString",
            display_name="Ino String To Alphabetic String",
            category="InoStringHelper",
            description="Hashes a string and converts it to a fixed-length alphabetic-only string.",
            inputs=[
                io.String.Input("input_string", default="mjp043n85se4z"),
                io.Int.Input("length", default=8, min=1, max=64),
            ],
            outputs=[
                io.String.Output(display_name="string"),
            ],
        )

    @classmethod
    def execute(cls, input_string, length) -> io.NodeOutput:
        if input_string is None:
            return io.NodeOutput("")

        alphabet = "abcdefghijklmnopqrstuvwxyz"
        digest = hashlib.sha256(input_string.encode()).digest()
        b32 = base64.b32encode(digest).decode().lower().rstrip("=")

        result_chars = []
        for ch in b32:
            if 'a' <= ch <= 'z':
                idx = ord(ch) - ord('a')
            else:
                idx = (ord(ch) - ord('2')) % 26
            result_chars.append(alphabet[idx])
            if len(result_chars) == length:
                break

        return io.NodeOutput("".join(result_chars))


class InoSaveText(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoSaveText",
            display_name="Ino Save Text",
            category="InoStringHelper",
            description="Saves a text string to a file in the specified folder.",
            is_output_node=True,
            inputs=[
                io.Boolean.Input("enabled", default=True, label_off="OFF", label_on="ON"),
                io.String.Input("text", default="", multiline=True),
                io.Combo.Input("parent_folder", options=PARENT_FOLDER_OPTIONS),
                io.String.Input("folder", default=""),
                io.String.Input("filename", default="output.txt"),
            ],
            outputs=[
                io.Boolean.Output(display_name="success"),
                io.String.Output(display_name="message"),
                io.String.Output(display_name="rel_path"),
                io.String.Output(display_name="abs_path"),
            ],
        )

    @classmethod
    def execute(cls, enabled, text, parent_folder, folder, filename) -> io.NodeOutput:
        rel_path, abs_path = resolve_comfy_path(parent_folder, folder, filename)

        if not enabled:
            return io.NodeOutput(False, "not enabled", rel_path, abs_path)
        try:
            Path(abs_path).parent.mkdir(parents=True, exist_ok=True)
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(text)
            return io.NodeOutput(True, "saved", rel_path, abs_path)
        except Exception as e:
            return io.NodeOutput(False, str(e), rel_path, abs_path)


LOCAL_NODE_CLASS = {
    "InoStringToggleCase": InoStringToggleCase,
    "InoStringReplacePlaceholder": InoStringReplacePlaceholder,
    "InoStringReplace": InoStringReplace,
    "InoStringStripSimple": InoStringStripSimple,
    "InoStringToAlphabeticString": InoStringToAlphabeticString,
    "InoSaveText": InoSaveText,
}
LOCAL_NODE_NAME = {
    "InoStringToggleCase": "Ino String Toggle Case",
    "InoStringReplacePlaceholder": "Ino String Replace Placeholder",
    "InoStringReplace": "Ino String Replace",
    "InoStringStripSimple": "Ino String Strip Simple",
    "InoStringToAlphabeticString": "Ino String To Alphabetic String",
    "InoSaveText": "Ino Save Text",
}
