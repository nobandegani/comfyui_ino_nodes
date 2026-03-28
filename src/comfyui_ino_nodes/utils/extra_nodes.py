import asyncio

from comfy_api.latest import ComfyExtension, io
from comfy_api.latest import _io

from ..node_helper import any_type, ino_print_log

#todo add show any

class InoRelay(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        execute_template = io.MatchType.Template("execute")
        relay_template = io.MatchType.Template("relay")
        return io.Schema(
            node_id="InoRelay",
            display_name="Ino Relay",
            category="InoNodes",
            inputs=[
                io.MatchType.Input("execute", template=execute_template, optional=True),
                io.MatchType.Input("relay", template=relay_template, optional=True),
            ],
            outputs=[
                io.MatchType.Output(template=execute_template, display_name="execute"),
                io.MatchType.Output(template=relay_template, display_name="relay"),
            ],
        )

    @classmethod
    def execute(cls, execute=None, relay=None) -> io.NodeOutput:
        if execute is not None:
            return io.NodeOutput(execute, relay)
        return io.NodeOutput(execute, None)

class InoAnyEqual(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        template = io.MatchType.Template("compare")
        return io.Schema(
            node_id="InoAnyEqual",
            display_name="Ino Any Equal",
            category="InoNodes",
            inputs=[
                io.MatchType.Input("input", template=template),
                io.MatchType.Input("compare", template=template),
            ],
            outputs=[
                io.Boolean.Output(display_name="equal"),
            ],
        )

    @classmethod
    def execute(cls, input, compare) -> io.NodeOutput:
        return io.NodeOutput(input == compare)


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

MISSING = object()

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
                io.Int.Input("switch", default=0, min=0),
                io.MatchType.Input("default", template=template, lazy=True),
                *[io.MatchType.Input(f"input_{i}", template=template, optional=True, lazy=True) for i in range(0, 10)],
            ],
            outputs=[
                io.MatchType.Output(template=template, display_name="output"),
            ],
        )

    @classmethod
    def check_lazy_status(cls, switch, default=MISSING, **kwargs):
        # None = connected but lazy, not yet evaluated → need to request
        # MISSING = not connected at all → skip, use fallback
        needed = []
        key = f"input_{switch}"
        selected = kwargs.get(key, MISSING)
        if selected is None:
            needed.append(key)
        elif selected is MISSING:
            # Selected input not connected, need default as fallback
            if default is None:
                needed.append("default")
        return needed if needed else None

    @classmethod
    def execute(cls, switch, default=MISSING, **kwargs) -> io.NodeOutput:
        result = kwargs.get(f"input_{switch}", MISSING)
        if result is not MISSING:
            return io.NodeOutput(result)
        fallback = default if default is not MISSING else None
        return io.NodeOutput(fallback)

LOCAL_NODE_CLASS = {
    "InoRelay": InoRelay,
    "InoAnyEqual": InoAnyEqual,
    "InoDelayAsync": InoDelayAsync,

    "InoPrintLog": InoPrintLog,

    "InoRandomNoise": InoRandomNoise,

    "InoSwitchOnBool": InoSwitchOnBool,
    "InoSwitchOnInt": InoSwitchOnInt
}
LOCAL_NODE_NAME = {
    "InoRelay": "Ino Relay",
    "InoAnyEqual": "Ino Any Equal",
    "InoDelayAsync": "Ino Delay Async",

    "InoPrintLog": "Ino Print Log",

    "InoRandomNoise": "Ino Random Noise",

    "InoSwitchOnBool": "Ino Switch On Bool",
    "InoSwitchOnInt": "Ino Switch On Int"
}
