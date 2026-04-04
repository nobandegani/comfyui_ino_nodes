from pathlib import Path

from comfy_api.latest import io

from ..node_helper import PARENT_FOLDER_OPTIONS, resolve_comfy_path


class InoGetComfyPath(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoGetComfyPath",
            display_name="Ino Get Comfy Path",
            category="InoPathHelper",
            description="Returns the absolute path to a ComfyUI directory (input, output, or temp).",
            inputs=[
                io.Combo.Input("folder_type", options=PARENT_FOLDER_OPTIONS),
            ],
            outputs=[
                io.String.Output(display_name="path"),
            ],
        )

    @classmethod
    def execute(cls, folder_type) -> io.NodeOutput:
        _, abs_path = resolve_comfy_path(folder_type)
        return io.NodeOutput(abs_path)


class InoGetLoraPathNameTriggerWord(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoGetLoraPathNameTriggerWord",
            display_name="Ino Get Lora Path Name Trigger Word",
            category="InoPathHelper",
            description="Extracts the LoRA ID, name, and trigger word from a file path.",
            inputs=[
                io.String.Input("lora_path"),
            ],
            outputs=[
                io.String.Output(display_name="lora_id"),
                io.String.Output(display_name="lora_name"),
                io.String.Output(display_name="lora_trigger_word"),
            ],
        )

    @classmethod
    def execute(cls, lora_path) -> io.NodeOutput:
        lora_path = Path(lora_path)
        lora_id = lora_path.parent.name
        lora_name = lora_path.stem
        trigger_word = lora_name.split('_')[0]
        return io.NodeOutput(lora_id, lora_name, trigger_word)


LOCAL_NODE_CLASS = {
    "InoGetComfyPath": InoGetComfyPath,
    "InoGetLoraPathNameTriggerWord": InoGetLoraPathNameTriggerWord,
}
LOCAL_NODE_NAME = {
    "InoGetComfyPath": "Ino Get Comfy Path",
    "InoGetLoraPathNameTriggerWord": "Ino Get Lora Path Name Trigger Word",
}
