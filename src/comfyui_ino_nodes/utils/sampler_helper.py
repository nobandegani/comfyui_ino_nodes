import hashlib
from pathlib import Path
import json
from copy import deepcopy
from typing import List, Dict, Tuple

import folder_paths
from comfy_extras.nodes_flux import FluxGuidance


def _as_int(v, default):
    try: return int(v)
    except (TypeError, ValueError): return default

def _as_float(v, default):
    try: return float(v)
    except (TypeError, ValueError): return default

def _get_model_type (model_type: str = "model") -> str:
    """Get model type from config."""
    if model_type == "model" or model_type is None or model_type == "":
        type_final = "models"
    elif model_type == "creator_lora":
        type_final = "creator_loras"
    else:
        type_final = model_type
    return type_final

def _resolve_models_path(config: str = "default", model_type: str = "") -> Path:
    """Resolve models .json path. 'default' => ../configs/models.json (relative to this file)."""

    type_final = _get_model_type(model_type)

    if config == "default":
        base_dir = Path(__file__).resolve().parent.parent  # comfyui_ino_nodes/
        return (base_dir / "configs" / f"{type_final}.json").resolve()
    return Path(config).expanduser().resolve()

def _load_models_list(config: str = "default", model_type: str = "") -> List[Dict]:
    """Load models list with file-mtime cache."""
    path = _resolve_models_path(config, model_type)
    if not path.exists():
        raise FileNotFoundError(f"models.json not found at: {path}")

    cache = _load_models_list.__dict__
    mtime = path.stat().st_mtime

    if cache.get("_path") != str(path) or cache.get("_mtime") != mtime:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        models = data.get("models", [])
        if not isinstance(models, list):
            raise ValueError("Invalid models.json: 'models' must be a list")

        cache["_path"] = str(path)
        cache["_mtime"] = mtime
        cache["_models"] = models

    return cache["_models"]

def get_models(config: str = "default", config_type: str = "model") -> Tuple[List[str], List[Dict]]:
    """
    Return (names, models):
      - names: list of model names (strings)
      - models: list of model dicts
    """
    models = deepcopy(_load_models_list(config, config_type))
    names = [m.get("name", "") for m in models if isinstance(m, dict)]
    return names, models

def get_model_by_name(name: str, models: List[Dict]) -> Dict:
    """Find a model by name (case-insensitive) from a models list."""
    key = (name or "").strip().lower()
    for m in models:
        if isinstance(m, dict) and m.get("name", "").strip().lower() == key:
            return deepcopy(m)
    raise KeyError(f"Model '{name}' not found.")


class InoGetModelConfig:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model": (list(get_models()[0]), {"tooltip": "The name of the LoRA."}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("ModelName", "ModelConfig")

    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    def function(self,
                 enabled,
                 model,
        ):
        if not enabled:
            return (model, "", )
        model_cfg = get_model_by_name(model, get_models()[1])
        return (model, model_cfg, )

class InoGetLoraConfig:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "lora": (list(get_models(config="default", config_type="creator_lora")[0]), {"tooltip": "The name of the LoRA."}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("LoraName", "LoraConfig")

    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    def function(self,
                 enabled,
                 lora,
        ):
        if not enabled:
            return (lora, "", )
        model_cfg = get_model_by_name(lora, get_models(config="default", config_type="creator_lora")[1])
        return (lora, model_cfg, )


class InoLoadSamplerModels:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model_config": ("STRING", {
                    "multiline": True,
                }),
                "lora_1_config": ("STRING", {
                    "multiline": True,
                }),
                "lora_2_config": ("STRING", {
                    "multiline": True,
                }),
                "lora_3_config": ("STRING", {
                    "multiline": True,
                }),
                "lora_4_config": ("STRING", {
                    "multiline": True,
                }),
            },
            "optional": {
                "clip_device": (["default", "cpu"], {"advanced": True}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE", )
    RETURN_NAMES = ("MODEL", "CLIP", "VAE", )

    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    def function(self,
                 enabled,
                 model_config,
                 lora_1_config, lora_2_config, lora_3_config, lora_4_config,
                 clip_device):
        if not enabled:
            return (None, None, None, )

        if isinstance(model_config, str):
            config_str = model_config.strip()
            if not config_str:
                model_cfg = {}
            else:
                try:
                    model_cfg = json.loads(config_str)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON in 'config': {e.msg} at line {e.lineno} col {e.colno}")
        elif isinstance(model_config, dict):
            model_cfg = model_config
        else:
            raise TypeError("`config` must be a JSON string or a dict.")

        from nodes import UNETLoader, CLIPLoader, DualCLIPLoader, VAELoader, LoraLoader

        unet_loader = UNETLoader()
        load_unet = unet_loader.load_unet(
            unet_name=model_cfg["unet"],
            weight_dtype=model_cfg["weight_type"]
        )

        dual_clip = model_cfg["use_dual_clip"]
        if dual_clip:
            clip_loader = DualCLIPLoader()
            load_clip = clip_loader.load_clip(
                clip_name1=model_cfg["clip1"],
                clip_name2=model_cfg["clip2"],
                type=model_cfg["type"],
                device=clip_device,
            )
        else:
            clip_loader = CLIPLoader()
            load_clip = clip_loader.load_clip(
                clip_name=model_cfg["clip1"],
                type=model_cfg["type"],
                device=clip_device,
            )

        vae_loader = VAELoader()
        load_vae = vae_loader.load_vae(
            vae_name=model_cfg["vae"],
        )

        print(f"lora1_name: {lora_1_config}")
        print(f"lora2_name: {lora_2_config}")
        model_loaded = load_unet[0]
        clip_loaded = load_clip[0]

        return ( model_loaded, clip_loaded, load_vae[0], )


class InoGetSamplerConfig:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "step": 1,
                    "label": "Seed (0 = random)"
                }),
                "config": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "label": "Config json"
                }),
                "model": ("MODEL", {}),
                "positive": ("CONDITIONING", {
                    "label": "Positive"
                }),
                "negative": ("CONDITIONING", {
                    "label": "Negative"
                }),
            },
            "optional": {
                "steps": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 100,
                    "step": 1,
                    "label": "(-1 = default)"
                }),
                "cfg": ("FLOAT", {
                    "default": -1,
                    "min": -1,
                    "max": 50,
                    "step": 0.01,
                    "label": "(-1 = default)"
                }),
                "denoise": ("FLOAT", {
                    "default": -1,
                    "min": -1,
                    "max": 50,
                    "step": 0.01,
                    "label": "(-1 = default)"
                }),
                "sampler_name": ("STRING", {
                    "multiline": False,
                    "default": "default"
                }),
                "scheduler_name": ("STRING", {
                    "multiline": False,
                    "default": "default"
                }),
            }
        }

    RETURN_TYPES = ("INT", "NOISE", "GUIDER", "SAMPLER", "SIGMAS", "INT", "FLOAT", "FLOAT", "STRING", "STRING", )
    RETURN_NAMES = ("Seed", "NOISE", "GUIDER", "SAMPLER", "SIGMAS", "Steps", "CFG", "Denoise", "Sampler Name", "Scheduler Name", )
    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        m = hashlib.sha256()
        m.update(seed)
        return m.digest().hex()

    def function(self, enabled, seed,
                 config,
                 model, positive, negative,
                 steps, cfg, denoise, sampler_name, scheduler_name):
        if not enabled:
            return config,

        if isinstance(config, str):
            config_str = config.strip()
            if not config_str:
                model_cfg = {}
            else:
                try:
                    model_cfg = json.loads(config_str)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON in 'config': {e.msg} at line {e.lineno} col {e.colno}")
        elif isinstance(config, dict):
            model_cfg = config
        else:
            raise TypeError("`config` must be a JSON string or a dict.")

        final_steps = steps if steps != -1 else _as_int(model_cfg.get("steps", -1), -1)
        final_cfg = cfg if cfg != -1 else _as_float(model_cfg.get("cfg", -1), -1)
        final_denoise = denoise if denoise != -1 else _as_float(model_cfg.get("denoise", -1), -1)

        final_sampler_name = sampler_name if sampler_name != "default" else model_cfg.get("sampler_name", "none")
        final_scheduler_name = scheduler_name if scheduler_name != "default" else model_cfg.get("scheduler_name", "none")

        use_cfg = bool(model_cfg.get("use_cfg", False))

        from comfy_extras.nodes_custom_sampler import BasicGuider, CFGGuider, RandomNoise, KSamplerSelect, BasicScheduler

        if use_cfg:
            guider = CFGGuider()
            get_guider = guider.get_guider(
                model=model,
                positive=positive,
                negative=negative,
                cfg=final_cfg
            )
        else:
            guider = BasicGuider()
            get_guider = guider.get_guider(
                model=model,
                conditioning=positive,
            )

        random_noise = RandomNoise()
        get_noise = random_noise.get_noise(
            noise_seed=seed,
        )

        sampler_selector = KSamplerSelect()
        get_sampler = sampler_selector.get_sampler(
            sampler_name=final_sampler_name
        )

        scheduler_selector = BasicScheduler()
        get_sigmas = scheduler_selector.get_sigmas(
            model=model,
            scheduler=final_scheduler_name,
            steps=final_steps,
            denoise=final_denoise,
        )

        return (seed,
                get_noise[0], get_guider[0], get_sampler[0], get_sigmas[0],
                final_steps, final_cfg, final_denoise, final_sampler_name, final_scheduler_name,)



class InoGetConditioning:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "config": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "label": "Config json"
                }),
                "clip": ("CLIP", {}),
                "positive1": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "label": "positive or flux clip l"
                }),
                "positive2": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "label": "flux t5xxl"
                }),
                "negative": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "label": "Negative"
                }),
            },
            "optional": {
                "guidance": ("FLOAT", {
                    "default": -1,
                    "min": -1,
                    "max": 50,
                    "step": 0.01,
                    "label": "(-1 = default)"
                }),
            }
        }

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING", "FLOAT", )
    RETURN_NAMES = ("POSITIVE", "NEGATIVE", "Guidance", )
    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    def function(self, enabled,
                 config,
                 clip, positive1, positive2, negative,
                 guidance):
        if not enabled:
            return config,

        if isinstance(config, str):
            config_str = config.strip()
            if not config_str:
                model_cfg = {}
            else:
                try:
                    model_cfg = json.loads(config_str)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON in 'config': {e.msg} at line {e.lineno} col {e.colno}")
        elif isinstance(config, dict):
            model_cfg = config
        else:
            raise TypeError("`config` must be a JSON string or a dict.")

        final_guidance = guidance if guidance != -1 else _as_float(model_cfg.get("guidance", -1), -1)

        use_negative_prompt = bool(model_cfg.get("use_negative_prompt", False))
        use_flux_clip_encoder = bool(model_cfg.get("use_flux_encoder", False))
        use_flux_guidance = bool(model_cfg.get("use_flux_guidance", False))

        from nodes import CLIPTextEncode, ConditioningZeroOut
        from comfy_extras.nodes_flux import CLIPTextEncodeFlux, FluxGuidance

        if use_flux_clip_encoder:
            positive_clip_encoder = CLIPTextEncodeFlux()
            positive_condition = positive_clip_encoder.encode(
                clip=clip,
                clip_l=positive1,
                t5xxl=positive2,
                guidance=final_guidance
            )
        else:
            positive_clip_encoder = CLIPTextEncode()
            positive_condition = positive_clip_encoder.encode(
                clip=clip,
                text=positive1,
            )

        if not use_flux_clip_encoder and use_flux_guidance:
            flux_guidance = FluxGuidance()
            positive_condition = flux_guidance.append(
                conditioning=positive_condition[0],
                guidance=final_guidance,
            )

        if use_negative_prompt:
            negative_clip_encoder = CLIPTextEncode()
            negative_condition = negative_clip_encoder.encode(
                clip=clip,
                text=negative,
            )
        else:
            negative_clip_encoder = ConditioningZeroOut()
            negative_condition = negative_clip_encoder.zero_out(
                conditioning=positive_condition[0]
            )

        return (positive_condition[0], negative_condition[0],
                final_guidance, )
