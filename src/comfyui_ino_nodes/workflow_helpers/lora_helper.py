import folder_paths
import comfy.utils
import comfy.sd

from comfy_api.latest import io


class InoLoadMultipleLora(io.ComfyNode):
    _loaded_loras = [None] * 5

    @classmethod
    def define_schema(cls):
        lora_list = folder_paths.get_filename_list("loras")
        inputs = [
            io.Model.Input("model"),
            io.Clip.Input("clip"),
        ]
        for i in range(5):
            inputs.append(io.Boolean.Input(f"lora_{i}_enable", default=False, label_off="OFF", label_on="ON", optional=True))
            inputs.append(io.Combo.Input(f"lora_{i}_name", options=lora_list, optional=True))
            inputs.append(io.Float.Input(f"lora_{i}_strength_model", default=1.0, min=-100.0, max=100.0, step=0.01, optional=True))
            inputs.append(io.Float.Input(f"lora_{i}_strength_clip", default=1.0, min=-100.0, max=100.0, step=0.01, optional=True))

        return io.Schema(
            node_id="InoLoadMultipleLora",
            display_name="Ino Load Multiple Lora",
            category="InoModelHelper",
            description="Loads up to 5 LoRAs and applies them sequentially to model and CLIP.",
            inputs=inputs,
            outputs=[
                io.Model.Output(display_name="model"),
                io.Clip.Output(display_name="clip"),
                io.String.Output(display_name="lora_names", is_output_list=True),
                io.Int.Output(display_name="total_loaded"),
            ],
        )

    @classmethod
    def execute(cls, model, clip, **kwargs) -> io.NodeOutput:
        loaded_names = []
        for i in range(5):
            enable = kwargs.get(f"lora_{i}_enable", False)
            if not enable:
                continue

            lora_name = kwargs.get(f"lora_{i}_name")
            strength_model = kwargs.get(f"lora_{i}_strength_model", 1.0)
            strength_clip = kwargs.get(f"lora_{i}_strength_clip", 1.0)

            if lora_name is None or (strength_model == 0 and strength_clip == 0):
                continue

            lora_path = folder_paths.get_full_path_or_raise("loras", lora_name)
            lora = None
            if cls._loaded_loras[i] is not None:
                if cls._loaded_loras[i][0] == lora_path:
                    lora = cls._loaded_loras[i][1]
                else:
                    cls._loaded_loras[i] = None

            if lora is None:
                lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
                cls._loaded_loras[i] = (lora_path, lora)

            model, clip = comfy.sd.load_lora_for_models(model, clip, lora, strength_model, strength_clip)
            loaded_names.append(lora_name)

        return io.NodeOutput(model, clip, loaded_names if loaded_names else [""], len(loaded_names))


LOCAL_NODE_CLASS = {
    "InoLoadMultipleLora": InoLoadMultipleLora,
}
LOCAL_NODE_NAME = {
    "InoLoadMultipleLora": "Ino Load Multiple Lora",
}
