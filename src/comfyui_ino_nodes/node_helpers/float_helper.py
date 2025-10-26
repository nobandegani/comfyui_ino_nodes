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

LOCAL_NODE_CLASS = {
    "InoFloatToInt": InoFloatToInt,
}
LOCAL_NODE_NAME = {
    "InoFloatToInt": "Ino Float To Int",
}
