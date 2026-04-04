import folder_paths
import comfy.utils
import comfy.sd


class InoLoadMultipleLora:

    def __init__(self):
        self.loaded_loras = [None] * 5

    @classmethod
    def INPUT_TYPES(s):
        lora_list = folder_paths.get_filename_list("loras")
        inputs = {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
            },
            "optional": {},
        }
        for i in range(5):
            inputs["optional"][f"lora_{i}_enable"] = ("BOOLEAN", {"default": False, "label_off": "OFF", "label_on": "ON"})
            inputs["optional"][f"lora_{i}_name"] = (lora_list,)
            inputs["optional"][f"lora_{i}_strength_model"] = ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01})
            inputs["optional"][f"lora_{i}_strength_clip"] = ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01})
        return inputs

    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "INT")
    RETURN_NAMES = ("model", "clip", "lora_names", "total_loaded")
    OUTPUT_IS_LIST = (False, False, True, False)
    FUNCTION = "load_loras"
    CATEGORY = "InoNodes"

    def load_loras(self, model, clip, **kwargs):
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
            if self.loaded_loras[i] is not None:
                if self.loaded_loras[i][0] == lora_path:
                    lora = self.loaded_loras[i][1]
                else:
                    self.loaded_loras[i] = None

            if lora is None:
                lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
                self.loaded_loras[i] = (lora_path, lora)

            model, clip = comfy.sd.load_lora_for_models(model, clip, lora, strength_model, strength_clip)
            loaded_names.append(lora_name)

        return (model, clip, loaded_names if loaded_names else [""], len(loaded_names))


LOCAL_NODE_CLASS = {
    "InoLoadMultipleLora": InoLoadMultipleLora,
}
LOCAL_NODE_NAME = {
    "InoLoadMultipleLora": "Ino Load Multiple Lora",
}
