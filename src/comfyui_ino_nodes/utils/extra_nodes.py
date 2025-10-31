import asyncio

from ..node_helper import any_type, ino_print_log

#todo add show any

class InoRelay:
    """
        Date Time As String
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "execute": (any_type, {}),
                "relay": (any_type, {}),
            },
        }

    RETURN_TYPES = (any_type, any_type, )
    RETURN_NAMES = ("execute", "relay" )
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass

    def function(self, execute, relay):
        return (execute, relay, )

class InoAnyEqual:
    """
        reverse boolean
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input": (any_type, {}),
                "compare": (any_type, {}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("equal",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, input, compare):
        return (input == compare,)

class InoAnyBoolSwitch:
    """
        reverse boolean
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_false": (any_type, {}),
                "input_true": (any_type, {}),
                "condition": ("BOOLEAN", {"default": True, "label_off": "False", "label_on": "True"}),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("output",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, input_false, input_true, condition):
        if condition:
            return (input_true,)
        else:
            return (input_false,)

class InoDelayAsync:
    """
        reverse boolean
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "relay": (any_type, {}),
                "delay": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 10000.0, "step": 0.1,}),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("output",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    async def function(self, enabled, relay, delay):
        if not enabled:
            return (relay,)

        await asyncio.sleep(delay)
        return (relay,)

class InoPrintLog:
    """
        reverse boolean
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "relay": (any_type, {}),
                "log_message": ("STRING", {"default": "Log message", "multiline": True}),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("output",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    async def function(self, enabled, relay, log_message):
        if not enabled:
            return (relay,)

        ino_print_log("", log_message)
        return (relay,)

from comfy_extras.nodes_custom_sampler import Noise_RandomNoise

class InoRandomNoise:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "noise_seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "control_after_generate": True,
                }),
                "precision": ("BOOLEAN", {"default": True, "label_off": "32-bit", "label_on": "64-bit"}),
            }
        }

    RETURN_TYPES = ("NOISE", "INT", )
    FUNCTION = "function"
    CATEGORY = "InoSamplerHelper"

    def function(self, noise_seed, precision:bool):
        if precision:
            final_seed = noise_seed & 0xFFFFFFFFFFFFFFFF
        else:
            final_seed = noise_seed & 0xFFFFFFFF

        random_seed = Noise_RandomNoise(final_seed)

        return (random_seed, final_seed, )

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

LOCAL_NODE_CLASS = {
    "InoRelay": InoRelay,
    "InoAnyEqual": InoAnyEqual,
    "InoAnyBoolSwitch": InoAnyBoolSwitch,
    "InoDelayAsync": InoDelayAsync,

    "InoPrintLog": InoPrintLog,

    "InoRandomNoise": InoRandomNoise,

    "InoCastAnyToString": InoCastAnyToString,
    "InoCastAnyToInt": InoCastAnyToInt,
}
LOCAL_NODE_NAME = {
    "InoRelay": "Ino Relay",
    "InoAnyEqual": "Ino Any Equal",
    "InoAnyBoolSwitch": "Ino Any Bool Switch",
    "InoDelayAsync": "Ino Delay Async",

    "InoPrintLog": "Ino Print Log",

    "InoRandomNoise": "Ino Random Noise",

    "InoCastAnyToString": "Ino Cast Any To String",
    "InoCastAnyToInt": "Ino Cast Any To Int",
}
