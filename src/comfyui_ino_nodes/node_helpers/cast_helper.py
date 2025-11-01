import asyncio

from ..node_helper import any_type, ino_print_log

class InoCastAnyToString:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_any": (any_type, {}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "function"
    CATEGORY = "InoExtraNodes"

    def function(self, input_any):
        return (str(input_any), )

class InoCastAnyToInt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_any": (any_type, {}),
            }
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "function"
    CATEGORY = "InoExtraNodes"

    def function(self, input_any):
        return (int(input_any), )

class InoCastAnyToModel:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_any": (any_type, {}),
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "function"
    CATEGORY = "InoExtraNodes"

    def function(self, input_any):
        return (input_any, )

class InoCastAnyToClip:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_any": (any_type, {}),
            }
        }

    RETURN_TYPES = ("CLIP",)
    FUNCTION = "function"
    CATEGORY = "InoExtraNodes"

    def function(self, input_any):
        return (input_any, )

class InoCastAnyToVae:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_any": (any_type, {}),
            }
        }

    RETURN_TYPES = ("VAE",)
    FUNCTION = "function"
    CATEGORY = "InoExtraNodes"

    def function(self, input_any):
        return (input_any, )

class InoCastAnyToControlnet:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_any": (any_type, {}),
            }
        }

    RETURN_TYPES = ("CONTROL_NET",)
    FUNCTION = "function"
    CATEGORY = "InoExtraNodes"

    def function(self, input_any):
        return (input_any, )

LOCAL_NODE_CLASS = {
    "InoCastAnyToString": InoCastAnyToString,
    "InoCastAnyToInt": InoCastAnyToInt,

    "InoCastAnyToModel": InoCastAnyToModel,
    "InoCastAnyToClip": InoCastAnyToClip,
    "InoCastAnyToVae": InoCastAnyToVae,
    "InoCastAnyToControlnet": InoCastAnyToControlnet,
}
LOCAL_NODE_NAME = {
    "InoCastAnyToString": "Ino Cast Any To String",
    "InoCastAnyToInt": "Ino Cast Any To Int",

    "InoCastAnyToModel": "Ino Cast Any To Model",
    "InoCastAnyToClip": "Ino Cast Any To Clip",
    "InoCastAnyToVae": "Ino Cast Any To Vae",
    "InoCastAnyToControlnet": "Ino Cast Any To Controlnet",
}
