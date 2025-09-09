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
