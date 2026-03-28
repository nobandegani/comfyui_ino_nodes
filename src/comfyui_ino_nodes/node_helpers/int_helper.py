import random
from comfy_api.latest import io

class InoRandomIntInRange:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "int_min": ("INT", {"default": 0, "min": 0, "max": 999999}),
                "int_max": ("INT", {"default": 999999, "min": 0, "max": 999999}),
                "length": ("INT", {"default": 1, "min": 0, "max": 10}),
            }
        }

    RETURN_TYPES = ("INT", "STRING", )
    RETURN_NAMES = ("RandomInt", "FormattedInt", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, enabled, int_min, int_max, length):
        if not enabled:
            return (-1, "")
        random_int = random.randint(int_min, int_max)
        formatted_int = str(random_int).zfill(length)
        return (random_int, formatted_int, )

class InoIntToString:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_int": ("INT", {"default": 0}),
            }
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("ReturnString", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, input_int):
        return (str(input_int), )

class InoIntToFloat:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_int": ("INT", {"default": 0}),
            }
        }

    RETURN_TYPES = ("FLOAT", )
    RETURN_NAMES = ("ReturnFLOAT", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, input_int):
        return (float(input_int), )

class InoIntEqual:
    """
        check if its equal to the input Int
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "int_a": ("INT", {
                    "default": 0,
                    "step": 1,
                    "display": "number"
                }),
                "int_b": ("INT", {
                    "default": 0,
                    "step": 1,
                    "display": "number"
                }),
            },

        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is equal",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, int_a, int_b):
        return (int_a == int_b,)

class InoCompareInt(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="InoCompareInt",
            display_name="Ino Compare Int",
            category="InoNodes",
            inputs=[
                io.Int.Input("int_a", default=0),
                io.Int.Input("int_b", default=0),
                io.Combo.Input("compare", options=["=", "<", ">", "<=", ">=", "<>"]),
            ],
            outputs=[
                io.Boolean.Output()
            ]
        )

    @classmethod
    def execute(cls, int_a, int_b, compare) -> io.NodeOutput:
        ops = {
            "=": int_a == int_b,
            "<": int_a < int_b,
            ">": int_a > int_b,
            "<=": int_a <= int_b,
            ">=": int_a >= int_b,
            "<>": int_a != int_b,
        }
        return io.NodeOutput(ops[compare])

LOCAL_NODE_CLASS = {
    "InoIntEqual": InoIntEqual,
    "InoRandomIntInRange": InoRandomIntInRange,
    "InoIntToString": InoIntToString,
    "InoIntToFloat": InoIntToFloat,
    "InoCompareInt": InoCompareInt,
}
LOCAL_NODE_NAME = {
    "InoIntEqual": "Ino Int Equal",
    "InoRandomIntInRange": "Ino Random Int In Range",
    "InoIntToString": "Ino Int To String",
    "InoIntToFloat": "Ino Int To Float",
    "InoCompareInt": "Ino Compare Int",
}
