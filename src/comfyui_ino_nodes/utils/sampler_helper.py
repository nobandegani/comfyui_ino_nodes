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

def _resolve_models_path(config: str = "default", model_type: str = "models") -> Path:
    """Resolve models .json path. 'default' => ../configs/models.json (relative to this file)."""

    if config == "default":
        base_dir = Path(__file__).resolve().parent.parent  # comfyui_ino_nodes/
        return (base_dir / "configs" / f"{model_type}.json").resolve()
    return Path(config).expanduser().resolve()

def _load_models_list(config: str = "default", model_type: str = "models") -> List[Dict]:
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

def get_models(config: str = "default", model_type: str = "models") -> Tuple[List[str], List[Dict]]:
    """
    Return (names, models):
      - names: list of model names (strings)
      - models: list of model dicts
    """
    models = deepcopy(_load_models_list(config, model_type))
    names = [m.get("name", "") for m in models if isinstance(m, dict)]
    return names, models

def get_model_by_name(name: str, models: List[Dict]) -> Dict:
    """Find a model by name (case-insensitive) from a models list."""
    key = (name or "").strip().lower()
    for m in models:
        if isinstance(m, dict) and m.get("name", "").strip().lower() == key:
            return deepcopy(m)
    raise KeyError(f"Model '{name}' not found.")


def prepare_lora_config(lora_config: str) -> Dict:
    """Prepare LoRA config"""

    if not lora_config or lora_config == "" or lora_config == "none":
        return {
            "use_lora": False,
            "lora_config": None
        }

    if isinstance(lora_config, str):
        config_str = lora_config.strip()
        try:
            model_cfg = json.loads(config_str)
        except json.JSONDecodeError as e:
            return {
                "use_lora": False,
                "lora_config": None
            }
    elif isinstance(lora_config, dict):
        model_cfg = lora_config
    else:
        return {
            "use_lora": False,
            "lora_config": None
        }

    return {
        "use_lora": True,
        "lora_config": model_cfg
    }

def load_lora(config_str, model, clip):
    """Load LoRA"""
    from nodes import LoraLoader
    prepared_config = prepare_lora_config(config_str)
    if prepared_config["use_lora"]:
        config_dict = prepared_config["lora_config"]
        lora_loader = LoraLoader()
        lora_loaded = lora_loader.load_lora(
            model=model,
            clip=clip,
            lora_name=config_dict["file"],
            strength_model=config_dict["strength_model"],
            strength_clip=config_dict["strength_clip"]
        )
        return lora_loaded[0], lora_loaded[1]
    else:
        return model, clip

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
                "lora": (list(get_models(config="default", model_type="loras")[0]), {"tooltip": "The name of the LoRA."}),
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
        model_cfg = get_model_by_name(lora, get_models(config="default", model_type="loras")[1])
        return (lora, model_cfg, )

class InoShowModelConfig:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "config": ("STRING", {
                    "multiline": True,
                }),
            }
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "BOOLEAN",
        "BOOLEAN",
        "BOOLEAN",
        "FLOAT",
        "BOOLEAN",
        "STRING",
        "STRING",
        "STRING",
        "BOOLEAN",
        "INT",
        "STRING",
        "STRING",
        "INT",
        "INT",
        "STRING",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "Name",
        "Type",
        "Unet",
        "WeightType",
        "UseDualClip",
        "UseFluxEncoder",
        "UseFluxGuidance",
        "Guidance",
        "UseNegativePrompt",
        "Clip1",
        "Clip2",
        "VAE",
        "UseCFG",
        "CFG",
        "SamplerName",
        "SchedulerName",
        "Steps",
        "Denoise",
        "Tags",
        "Description",
        "LoraCompatible",
    )

    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    def function(self, enabled, config):
        if not enabled:
            return None
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

        return (
            model_cfg["name"],
            model_cfg["type"],
            model_cfg["unet"],
            model_cfg["weight_type"],
            model_cfg["use_dual_clip"],
            model_cfg["use_flux_encoder"],
            model_cfg["use_flux_guidance"],
            model_cfg["guidance"],
            model_cfg["use_negative_prompt"],
            model_cfg["clip1"],
            model_cfg["clip2"],
            model_cfg["vae"],
            model_cfg["use_cfg"],
            model_cfg["cfg"],
            model_cfg["sampler_name"],
            model_cfg["scheduler_name"],
            model_cfg["steps"],
            model_cfg["denoise"],
            model_cfg["tags"],
            model_cfg["description"],
            model_cfg["lora_compatible"],

        )

class InoShowLoraConfig:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "config": ("STRING", {
                    "multiline": True,
                }),
            }
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "FLOAT",
        "FLOAT",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "Name",
        "BaseModel",
        "Type",
        "TriggerWord",
        "TriggerWords",
        "File",
        "WeightType",
        "ModelStrength",
        "ClipStrength",
        "Description",
        "Tags",
    )

    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    def function(self, enabled, config):
        if not enabled:
            return None
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

        return (
            model_cfg["name"],
            model_cfg["base_model"],
            model_cfg["type"],
            model_cfg["trigger_word"],
            model_cfg["trigger_words"],
            model_cfg["file"],
            model_cfg["weight_type"],
            model_cfg["strength_model"],
            model_cfg["strength_clip"],
            model_cfg["description"],
            model_cfg["tags"],
        )

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

        from nodes import UNETLoader, CLIPLoader, DualCLIPLoader, VAELoader

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

        model_loaded = load_unet[0]
        clip_loaded = load_clip[0]

        lora_1_loaded = load_lora(lora_1_config, model_loaded, clip_loaded)
        model_loaded = lora_1_loaded[0]
        clip_loaded = lora_1_loaded[1]

        lora_2_loaded = load_lora(lora_2_config, model_loaded, clip_loaded)
        model_loaded = lora_2_loaded[0]
        clip_loaded = lora_2_loaded[1]

        lora_3_loaded = load_lora(lora_3_config, model_loaded, clip_loaded)
        model_loaded = lora_3_loaded[0]
        clip_loaded = lora_3_loaded[1]

        lora_4_loaded = load_lora(lora_4_config, model_loaded, clip_loaded)
        model_loaded = lora_4_loaded[0]
        clip_loaded = lora_4_loaded[1]

        return ( model_loaded, clip_loaded, load_vae[0], )


class InoGetSamplerConfig:
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
                "model": ("MODEL", {}),
                "positive": ("CONDITIONING", {
                    "label": "Positive"
                }),
                "negative": ("CONDITIONING", {
                    "label": "Negative"
                }),
            },
        }

    RETURN_TYPES = ("GUIDER", "SAMPLER", "SIGMAS", )
    RETURN_NAMES = ("GUIDER", "SAMPLER", "SIGMAS", )
    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    def function(self, enabled,
                 config,
                 model, positive, negative,
        ):
        if not enabled:
            return None, None, None,

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

        use_cfg = bool(model_cfg.get("use_cfg", False))

        from comfy_extras.nodes_custom_sampler import BasicGuider, CFGGuider, KSamplerSelect, BasicScheduler

        if use_cfg:
            guider = CFGGuider()
            get_guider = guider.get_guider(
                model=model,
                positive=positive,
                negative=negative,
                cfg=model_cfg.get("cfg", -1)
            )
        else:
            guider = BasicGuider()
            get_guider = guider.get_guider(
                model=model,
                conditioning=positive,
            )

        sampler_selector = KSamplerSelect()
        get_sampler = sampler_selector.get_sampler(
            sampler_name=model_cfg.get("sampler_name", "none")
        )

        scheduler_selector = BasicScheduler()
        get_sigmas = scheduler_selector.get_sigmas(
            model=model,
            scheduler=model_cfg.get("scheduler_name", "none"),
            steps=model_cfg.get("steps", -1),
            denoise=model_cfg.get("denoise", -1),
        )

        return (get_guider[0], get_sampler[0], get_sigmas[0], )



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
        }

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING", )
    RETURN_NAMES = ("POSITIVE", "NEGATIVE", )
    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    def function(self, enabled,
                 config,
                 clip, positive1, positive2, negative):
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

        final_guidance = _as_float(model_cfg.get("guidance", -1), -1)

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

        return (positive_condition[0], negative_condition[0], )
