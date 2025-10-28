# wildcard trick is taken from pythongossss's
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

import os
IS_DEBUG  = bool(os.getenv('COMFYUI_INO_DEBUG', 0))

def ino_print_log(prefix:str = "", msg:str="unknown", e = None):
    if IS_DEBUG:
        print(f"{prefix}: {msg} -> {e}")

MODEL_TYPES = (
    "checkpoints", "clip", "clip_vision", "controlnet", "diffusers", "diffusion_models",
    "loras", "sams", "text_encoders", "vae"
)
