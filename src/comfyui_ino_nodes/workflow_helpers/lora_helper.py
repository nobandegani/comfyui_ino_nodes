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

        return (model, clip, loaded_names, len(loaded_names))


class InoCalculateLoraConfig:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "dataset_count": ("INT", {
                    "default": 6,
                    "step": 1,
                    "display": "number"
                }),
            },
            "optional": {
                "max_batch_size": ("INT", {
                    "default": 6,
                    "step": 1,
                    "display": "number"
                }),
                "target_epochs": ("INT", {
                    "default": 25,
                    "step": 1,
                    "display": "number"
                }),
                "max_lora_parts": ("INT", {
                    "default": 6,
                    "step": 1,
                    "display": "number"
                }),
            },
        }

    RETURN_TYPES = ("INT",
                    "INT",
                    "INT",
                    "INT",
                    "INT",
                    "INT",
                    "FLOAT",
                    "FLOAT",
                    "FLOAT",
                    "INT",
                    "STRING",
                    "BOOLEAN",
                    "INT",
                    "FLOAT",
                    "BOOLEAN",
                    "INT")
    RETURN_NAMES = ("DIM(Linear rank)",
                    "Alpha(Linear alpha)",
                    "Steps",
                    "Save every",
                    "Batch size",
                    "Gradient accumulation",
                    "Learning rate",
                    "Weight decay",
                    "EMA decay",
                    "DOP loss multiplier",
                    "Noise Scheduler",
                    "EMA", "LoRA Weight",
                    "Caption dropout rate",
                    "Cache latents",
                    "Sample Every")

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass


    def function(self, enabled, dataset_count, max_batch_size, target_epochs, max_lora_parts):
        if not enabled:
            return 0, 0, 0, 0, 0

        batch_size = min(max_batch_size, max(1, dataset_count // 10))
        grad_accum = max(1, 12 // batch_size)

        steps = int(dataset_count * target_epochs / batch_size)

        ema = False

        dim = 32
        alpha = dim // 2

        if dataset_count <= 40:
            lr = 0.00005
        elif dataset_count <= 100:
            lr = 0.0001
        else:
            lr = 0.00015

        save_every = steps / max_lora_parts
        sample_every = steps / 10
        return int(dim), int(alpha), int(steps), int(save_every), int(batch_size), int(grad_accum), float(lr), float(0.0001), float(0.99), int(1), "DDPM", ema, int(1), float(0.05), True, int(sample_every)

LOCAL_NODE_CLASS = {
    "InoCalculateLoraConfig": InoCalculateLoraConfig,
    "InoLoadMultipleLora": InoLoadMultipleLora,
}
LOCAL_NODE_NAME = {
    "InoCalculateLoraConfig": "Ino Calculate Lora Config",
    "InoLoadMultipleLora": "Ino Load Multiple Lora",
}
