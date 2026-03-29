from comfy_api.latest import io

class InoFloatToInt:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_float": ("FLOAT", {"default": 0}),
                "method": ( ["round", "floor", "ceil"], {})
            }
        }

    RETURN_TYPES = ("INT", )
    RETURN_NAMES = ("ReturnINT", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, input_float, method):
        import math
        if method == "round":
            return (round(input_float),)
        elif method == "floor":
            return (math.floor(input_float),)
        elif method == "ceil":
            return (math.ceil(input_float), )

class InoCompareFloat(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="InoCompareFloat",
            display_name="Ino Compare Float",
            category="InoNodes",
            inputs=[
                io.Float.Input("float_a", default=0.0),
                io.Float.Input("float_b", default=0.0),
                io.Combo.Input("compare", options=["=", "<", ">", "<=", ">=", "<>"]),
            ],
            outputs=[
                io.Boolean.Output()
            ]
        )

    @classmethod
    def execute(cls, float_a, float_b, compare) -> io.NodeOutput:
        ops = {
            "=": float_a == float_b,
            "<": float_a < float_b,
            ">": float_a > float_b,
            "<=": float_a <= float_b,
            ">=": float_a >= float_b,
            "<>": float_a != float_b,
        }
        return io.NodeOutput(ops[compare])

class InoFloatEqual:
    """
        check if its equal to the input Float
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "float_a": ("FLOAT", {
                    "default": 0.0,
                    "step": 0.01,
                    "display": "number"
                }),
                "float_b": ("FLOAT", {
                    "default": 0.0,
                    "step": 0.01,
                    "display": "number"
                }),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is equal",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, float_a, float_b):
        return (float_a == float_b,)

LOCAL_NODE_CLASS = {
    "InoFloatToInt": InoFloatToInt,
    "InoCompareFloat": InoCompareFloat,
    "InoFloatEqual": InoFloatEqual,
}
LOCAL_NODE_NAME = {
    "InoFloatToInt": "Ino Float To Int",
    "InoCompareFloat": "Ino Compare Float",
    "InoFloatEqual": "Ino Float Equal",
}
