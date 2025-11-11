# wildcard trick is taken from pythongossss's
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

import os
_is_debug = os.getenv('COMFYUI_INO_DEBUG') == "1"
IS_DEBUG  = _is_debug
print(f"COMFYUI_INO_DEBUG: {_is_debug}")

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
    "llm", "Joy_caption", "prompt_generator", "Diffueraser"
    "tts", "unet", "upscale_models", "vae", "vibevoice", "wav2vec2"
)

UNET_WEIGHT_DTYPE=["default", "fp8_e4m3fn", "fp8_e4m3fn_fast", "fp8_e5m2"]

CLIP_TYPE= ["stable_diffusion", "stable_cascade", "sd3", "stable_audio", "mochi", "ltxv", "pixart", "cosmos", "lumina2", "wan", "hidream", "chroma", "ace", "omnigen2", "qwen_image", "hunyuan_image"]
