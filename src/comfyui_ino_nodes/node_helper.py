# wildcard trick is taken from pythongossss's
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

import os
_is_debug = os.getenv('COMFYUI_INO_DEBUG', 0) == 1
IS_DEBUG  = _is_debug

def ino_print_log(prefix:str = "", msg:str="unknown", e = None):
    if IS_DEBUG:
        message = ""
        if prefix:
            message += f"[{prefix}]: "
        message += f"{msg}"
        if e:
            message += f" ->{e}"
        print(message)

MODEL_TYPES = (
    "audio_encoders", "checkpoints", "clip", "clip_vision", "controlnet", "diffusers", "diffusion_models",
    "embeddings", "face_restore", "loras", "sams", "style_models","text_encoders", "transformers",
    "tts", "unet", "upscale_models", "vae", "vibevoice", "wav2vec2"
)
