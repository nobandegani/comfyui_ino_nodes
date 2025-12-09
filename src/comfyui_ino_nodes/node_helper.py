from pathlib import Path
import os
import csv

# wildcard trick is taken from pythongossss's
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

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
    "audio_encoders",
    "checkpoints",
    "clip",
    "clip_vision",
    "controlnet",
    "detection",
    "DiffuEraser",
    "diffusers",
    "diffusion_models",
    "embeddings",
    "face_restore",
    "Joy_caption",
    "llm",
    "loras",
    "prompt_generator",
    "sam",
    "sam2",
    "sams",
    "style_models",
    "text_encoders",
    "transformers",
    "tts",
    "ultralytics",
    "unet",
    "upscale_models",
    "vae",
    "vibevoice",
    "wav2vec2",
)

UNET_WEIGHT_DTYPE= ["default", "fp8_e4m3fn", "fp8_e4m3fn_fast", "fp8_e5m2"]

CLIP_TYPE= ["stable_diffusion", "stable_cascade", "sd3", "stable_audio", "mochi", "ltxv", "pixart", "cosmos", "lumina2", "wan", "hidream", "chroma", "ace", "omnigen2", "qwen_image", "hunyuan_image", "flux2", "ovis"]

def _load_csv_as_dict(is_config: bool, model_type: str) -> list:
    base_dir = Path(__file__).resolve().parent.parent.parent
    middle_dir = "configs" if is_config else "files"
    csv_path: Path = base_dir / "data" / middle_dir / f"{model_type}.csv"

    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        return []

    with open(str(csv_path.resolve()), mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def get_list_from_csv(is_config: bool, model_type: str, return_only_names):
    csv_data = _load_csv_as_dict(is_config, model_type)
    data = []

    if return_only_names:
        for row in csv_data:
            data.append(row["name"])
    else:
        data = csv_data

    return data

def get_model_from_csv(is_config: bool, model_type: str, model_name:str):
    csv_data = _load_csv_as_dict(is_config, model_type)
    data = {}
    for row in csv_data:
        if row["name"] == model_name:
            data = row
    return data
