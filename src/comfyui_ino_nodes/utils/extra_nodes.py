import asyncio

from comfy_api.latest import ComfyExtension, io
from comfy_api.latest import _io

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
                "execute": (any_type, {"default": None, }),
                "relay": (any_type, {"default": None, }),
            },
        }

    RETURN_TYPES = (any_type, any_type, )
    RETURN_NAMES = ("execute", "relay" )
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass

    async def function(self, execute = None, relay = None):
        if execute is not None:
            return (execute, relay,)

        return (execute, None,)

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

class InoSwitchOnBool(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        template = io.MatchType.Template("switch")
        return io.Schema(
            node_id="InoSwitchOnBool",
            display_name="Ino Switch On Bool",
            category="logic",
            is_experimental=True,
            inputs=[
                io.Boolean.Input("switch"),
                io.MatchType.Input("on_false", template=template, lazy=True),
                io.MatchType.Input("on_true", template=template, lazy=True),
            ],
            outputs=[
                io.MatchType.Output(template=template, display_name="output"),
            ],
        )

    @classmethod
    def check_lazy_status(cls, switch, on_false=None, on_true=None):
        if switch and on_true is None:
            return ["on_true"]
        if not switch and on_false is None:
            return ["on_false"]

    @classmethod
    def execute(cls, switch, on_true, on_false) -> io.NodeOutput:
        return io.NodeOutput(on_true if switch else on_false)

class InoSwitchOnInt(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        template = io.MatchType.Template("switch")
        return io.Schema(
            node_id="InoSwitchOnInt",
            display_name="Ino Switch On Int",
            category="InoNodes",
            is_experimental=True,
            inputs=[
                io.Int.Input("switch", default=0, min=-1),
                io.MatchType.Input("on_below_0", template=template, lazy=True),
                io.MatchType.Input("on_above_9", template=template, lazy=True),
                *[io.MatchType.Input(f"input_{i}", template=template, lazy=True) for i in range(10)],
            ],
            outputs=[
                io.MatchType.Output(template=template, display_name="output"),
            ],
        )

    @classmethod
    def check_lazy_status(cls, switch, on_below_0=None, on_above_9=None, **kwargs):
        if switch < 0 and on_below_0 is None:
            return ["on_below_0"]
        if switch > 9 and on_above_9 is None:
            return ["on_above_9"]
        if 0 <= switch <= 9:
            key = f"input_{switch}"
            if kwargs.get(key) is None:
                return [key]

    @classmethod
    def execute(cls, switch, on_below_0=None, on_above_9=None, **kwargs) -> io.NodeOutput:
        if switch < 0:
            return io.NodeOutput(on_below_0)
        if switch > 9:
            return io.NodeOutput(on_above_9)
        return io.NodeOutput(kwargs.get(f"input_{switch}"))

LOCAL_NODE_CLASS = {
    "InoRelay": InoRelay,
    "InoAnyEqual": InoAnyEqual,
    "InoAnyBoolSwitch": InoAnyBoolSwitch,
    "InoDelayAsync": InoDelayAsync,

    "InoPrintLog": InoPrintLog,

    "InoRandomNoise": InoRandomNoise,

    "InoSwitchOnBool": InoSwitchOnBool,
    "InoSwitchOnInt": InoSwitchOnInt
}
LOCAL_NODE_NAME = {
    "InoRelay": "Ino Relay",
    "InoAnyEqual": "Ino Any Equal",
    "InoAnyBoolSwitch": "Ino Any Bool Switch",
    "InoDelayAsync": "Ino Delay Async",

    "InoPrintLog": "Ino Print Log",

    "InoRandomNoise": "Ino Random Noise",

    "InoSwitchOnBool": "Ino Switch On Bool",
    "InoSwitchOnInt": "Ino Switch On Int"
}
