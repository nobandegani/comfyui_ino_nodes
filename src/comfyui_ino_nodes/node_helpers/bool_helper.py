from comfy_api.latest import ComfyExtension, io

class InoBooleanEqual(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="InoBooleanEqual",
            display_name="Ino Boolean Equal",
            category="InoNodes",
            inputs=[
                io.Boolean.Input("input",default=True),
                io.Boolean.Input("compare", default=True),
            ],
            outputs=[
                io.Boolean.Output()
            ]
        )

    @classmethod
    def execute(cls, input, compare) -> io.NodeOutput:
        return io.NodeOutput(input == compare)

class InoNotBoolean(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="InoNotBoolean",
            display_name="Ino Not Boolean",
            category="InoNodes",
            inputs=[
                io.Boolean.Input("boolean", default=True),
            ],
            outputs=[
                io.Boolean.Output()
            ]
        )

    @classmethod
    def execute(cls, boolean: bool) -> io.NodeOutput:
        return io.NodeOutput(not boolean)


class InoBoolToSwitch(io.ComfyNode):
    """
    Convert bool to int, 2 for true, 1 for false. When disabled returns -1.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="InoBoolToSwitch",
            display_name="Ino Bool To Switch",
            category="InoNodes",
            inputs=[
                io.Boolean.Input("enabled", default=True, label_off="OFF", label_on="ON"),
                io.Boolean.Input("input_bool"),
            ],
            outputs=[
                io.Int.Output()
            ]
        )

    @classmethod
    def execute(cls, enabled: bool, input_bool: bool) -> io.NodeOutput:
        if not enabled:
            return io.NodeOutput(-1)
        result = 2 if input_bool else 1
        return io.NodeOutput(result)

class InoConditionBooleanMulti:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 2, "max": 1000, "step": 1}),
                "condition": ( ["AND", "OR"], {}),
                "bool_1": ("BOOLEAN", {"default": True, "forceInput": True}),
            },
            "optional": {
                "bool_2": ("BOOLEAN", {"default": False, "forceInput": True}),
            }
    }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("bool",)
    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, inputcount, condition, **kwargs):
        bool_1 = kwargs["bool_1"]
        bools = []
        for c in range(1, inputcount):
            val = kwargs.get(f"bool_{c + 1}", None)
            if val is None:
                continue
            bools.append(bool(val))

        if bool_1 is not None:
            bools.insert(0, bool(bool_1))

        if not bools:
            return (False,)

        if condition == "AND":
            result = all(bools)
        elif condition == "OR":
            result = any(bools)
        else:
            return (False,)

        return (result,)

LOCAL_NODE_CLASS = {
    "InoBooleanEqual": InoBooleanEqual,
    "InoNotBoolean": InoNotBoolean,
    "InoBoolToSwitch": InoBoolToSwitch,
    "InoConditionBooleanMulti": InoConditionBooleanMulti,
}
LOCAL_NODE_NAME = {
    "InoBooleanEqual": "Ino Boolean Equal",
    "InoNotBoolean": "Ino Not Boolean",
    "InoBoolToSwitch": "Ino Bool To Switch",
    "InoConditionBooleanMulti": "Ino Condition Boolean Multi",
}
