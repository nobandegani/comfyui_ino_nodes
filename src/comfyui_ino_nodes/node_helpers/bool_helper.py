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

class InoConditionBoolean(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="InoConditionBoolean",
            display_name="Ino Condition Boolean",
            category="InoNodes",
            inputs=[
                io.Combo.Input("condition", options=["AND", "OR"]),
                io.Boolean.Input("bool_1", default=True),
                io.Boolean.Input("bool_2", default=True),
            ],
            outputs=[
                io.Boolean.Output()
            ]
        )

    @classmethod
    def execute(cls, condition, bool_1, bool_2) -> io.NodeOutput:
        if condition == "AND":
            result = bool_1 and bool_2
        else:
            result = bool_1 or bool_2
        return io.NodeOutput(result)

LOCAL_NODE_CLASS = {
    "InoBooleanEqual": InoBooleanEqual,
    "InoNotBoolean": InoNotBoolean,
    "InoBoolToSwitch": InoBoolToSwitch,
    "InoConditionBoolean": InoConditionBoolean
}
LOCAL_NODE_NAME = {
    "InoBooleanEqual": "Ino Boolean Equal",
    "InoNotBoolean": "Ino Not Boolean",
    "InoBoolToSwitch": "Ino Bool To Switch",
    "InoConditionBoolean": "Ino Condition Boolean",
}
