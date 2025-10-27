import hashlib
from pathlib import Path
import json
import asyncio
from copy import deepcopy
from typing import List, Dict, Tuple

from inopyutils import InoJsonHelper

import folder_paths
from comfy_extras.nodes_flux import FluxGuidance

from comfy.samplers import SAMPLER_NAMES, SCHEDULER_NAMES
from .model_helper import InoHuggingFaceDownloadFile, InoCivitaiDownloadFile

from ..node_helper import any_type, ino_print_log

default_bool = ["unset", "true", "false"]
sampler_names = ["unset"] + SAMPLER_NAMES
scheduler_names = ["unset"] + SCHEDULER_NAMES

def _load_models(config: str = "default", model_type: str = "models") -> Dict:
    """Load models"""
    if config == "default":
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        json_path:Path = base_dir / "data" / f"{model_type}.json"
        read_json =InoJsonHelper.read_json_from_file_sync(
            file_path=str(json_path.resolve())
        )
        if not read_json["success"]:
            return read_json
        else:
            json_data = read_json["data"]
    else:
        json_data = InoJsonHelper.string_to_dict(
            json_string=config,
        )
        if not json_data["success"]:
            return json_data
        else:
            json_data = json_data["data"]

    json_data = json_data[model_type]
    names = [m["name"] for m in json_data]
    ids = [m["id"] for m in json_data]

    return {
        "success": True,
        "msg": "success",
        "names": names,
        "ids": ids,
        "fields": json_data,
    }

def get_model_by_field(models: Dict, field_name: str, field_match: str) -> Dict:
    for m in models:
        if m[field_name] == field_match:
            return deepcopy(m)
    return {}

def prepare_lora_config(lora_config: str) -> Dict:
    """Prepare LoRA config"""

    load_json = InoJsonHelper.string_to_dict(
        json_string=lora_config
    )
    if not load_json["success"]:
        return {
            "use_lora": False,
            "lora_config": None
        }

    return {
        "use_lora": True,
        "lora_config": load_json["data"]
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
        return True, lora_loaded[0], lora_loaded[1], f"{config_dict["trigger_word"]}, "
    else:
        return False, model, clip, ""

from comfy_extras.nodes_custom_sampler import Noise_RandomNoise

class InoRandomNoise:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "noise_seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "control_after_generate": True,
                }),
            }
        }

    RETURN_TYPES = ("NOISE", "INT", )
    FUNCTION = "function"
    CATEGORY = "InoSamplerHelper"

    def function(self, noise_seed):
        random_seed = Noise_RandomNoise(noise_seed)
        return (random_seed, noise_seed, )

class InoGetModelConfig:
    """

    """
    @staticmethod
    def load_models():
        load = _load_models()
        if load["success"]:
            names = ["unset"]
            names.extend(load["names"])
            return {"success": load["msg"], "msg": "", "names": names, "ids": load["ids"], "fields": load["fields"]}
        else:
            return None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model_name": (s.load_models()["names"], {"tooltip": "The name of the Model."}),
                "model_id": (s.load_models()["ids"], {"tooltip": "The id of the Model."}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "INT", "STRING", "STRING", )
    RETURN_NAMES = ("Success", "MSG", "Model_ID", "Model_Name", "Model_Config", )

    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    def function(self,
                 enabled,
                 model_name, model_id
        ):
        if not enabled:
            return (False, "not enabled", -1, "", "", )

        models = self.load_models()["fields"]
        if model_name == "unset":
            model_cfg = get_model_by_field(models, "id", model_id)
        else:
            model_cfg = get_model_by_field(models, "name", model_name)

        model_cfg_str = InoJsonHelper.dict_to_string(model_cfg)
        if not model_cfg_str["success"]:
            return (model_cfg_str["success"], model_cfg_str["msg"], -1, "", "", )

        return (True, "Success", model_cfg["id"], model_cfg["name"], model_cfg_str["data"], )

class InoGetLoraConfig:
    """

    """

    @staticmethod
    def load_models():
        load = _load_models("default", "loras")
        if load["success"]:
            names = ["unset"]
            names.extend(load["names"])
            return {"success": load["msg"], "msg": "", "names": names, "ids": load["ids"], "fields": load["fields"]}
        else:
            return None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "lora_name": (s.load_models()["names"], {"tooltip": "The name of the Model."}),
                "lora_id": (s.load_models()["ids"], {"tooltip": "The id of the Model."}),
            },
            "optional": {
                "strength_model": ("FLOAT", {"default": -1, "min": -1, "max": 1, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": -1, "min": -1, "max": 1, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("INT", "STRING", "STRING",)
    RETURN_NAMES = ("LoraID", "LoraName", "LoraConfig",)

    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    def function(self, enabled, lora_name, lora_id, strength_model, strength_clip ):
        if not enabled:
            return (-1, "", "", )

        models = self.load_models()["fields"]
        if lora_name == "unset":
            lora_cfg = get_model_by_field(models, "id", lora_id)
        else:
            lora_cfg = get_model_by_field(models, "name", lora_name)

        if strength_model != -1:
            lora_cfg["strength_model"] = strength_model

        if strength_clip != -1:
            lora_cfg["strength_clip"] = strength_clip

        lora_cfg_str = InoJsonHelper.dict_to_string(lora_cfg)
        if not lora_cfg_str["success"]:
            return (-1, "", "",)

        return (lora_cfg["id"], lora_cfg["name"], lora_cfg_str["data"], )

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

        load_json = InoJsonHelper.string_to_dict(config)
        if not load_json["success"]:
            return None
        model_cfg = load_json["data"]

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

class InoUpdateModelConfig:
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
            },
            "optional": {
                "use_dual_clip": (default_bool, ),
                "use_flux_encoder": (default_bool, ),
                "use_flux_guidance": (default_bool, ),
                "guidance": ("FLOAT", {"default": -1.0, "min": -1.0, "max": 100.0}),
                "use_negative_prompt": (default_bool, ),
                "use_cfg": (default_bool, ),
                "cfg": ("FLOAT", {"default": -1.0, "min": -1.0, "max": 100.0}),
                "sampler_name": (sampler_names, ),
                "scheduler_name": (scheduler_names, ),
                "steps": ("INT", {"default": -1, "min": -1, "max": 100}),
                "denoise": ("FLOAT", {"default": -1.0, "min": -1.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("OldConfig", "NewConfig", )

    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    def function(
        self, enabled, config,
        use_dual_clip = "unset", use_flux_encoder = "unset", use_flux_guidance = "unset",
        guidance  = -1.0,
        use_negative_prompt = "unset", use_cfg = "unset",
        cfg = -1.0,
        sampler_name = "unset", scheduler_name = "unset",
        steps = -1, denoise = -1.0
    ):
        if not enabled:
            return None

        load_json = InoJsonHelper.string_to_dict(config)
        if not load_json["success"]:
            return None
        model_cfg = load_json["data"]

        if use_dual_clip != "unset":
            model_cfg["use_dual_clip"] = use_dual_clip

        if use_flux_encoder != "unset":
            model_cfg["use_flux_encoder"] = use_flux_encoder

        if use_flux_guidance != "unset":
            model_cfg["use_flux_guidance"] = use_flux_guidance

        if guidance != -1:
            model_cfg["guidance"] = guidance

        if use_negative_prompt != "unset":
            model_cfg["use_negative_prompt"] = use_negative_prompt

        if use_cfg != "unset":
            model_cfg["use_cfg"] = use_cfg

        if cfg != -1:
            model_cfg["cfg"] = cfg

        if sampler_name != "unset":
            model_cfg["sampler_name"] = sampler_name

        if scheduler_name != "unset":
            model_cfg["scheduler_name"] = scheduler_name

        if steps != -1:
            model_cfg["steps"] = steps

        if denoise != -1:
            model_cfg["denoise"] = denoise

        model_cfg_str = InoJsonHelper.dict_to_string(model_cfg)
        if not model_cfg_str["success"]:
            return (-1, "", "",)

        return (config, model_cfg_str["data"], )

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
        load_json = InoJsonHelper.string_to_dict(config)
        if not load_json["success"]:
            return None
        model_cfg = load_json["data"]

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
                "execute": (any_type,),
                "model_config": ("STRING", {}),
                "lora_1_config": ("STRING", {}),
                "lora_2_config": ("STRING", {}),
                "lora_3_config": ("STRING", {}),
                "lora_4_config": ("STRING", {}),
            },
            "optional": {
                "clip_device": (["default", "cpu"], {"advanced": True}),
                "use_dual_clip": (default_bool,),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "MODEL", "CLIP", "VAE", "BOOLEAN", "STRING", )
    RETURN_NAMES = ("Success", "MSG", "MODEL", "CLIP", "VAE", "LoraApplied", "TriggerWords", )

    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    async def function(
        self, enabled, execute,
        model_config,
        lora_1_config, lora_2_config, lora_3_config, lora_4_config,
        clip_device,
        use_dual_clip,
    ):
        if not enabled:
            ino_print_log("InoLoadSamplerModels", "not enabled")
            return (False, "not enabled", None, None, None, None, None, )

        if execute is None:
            ino_print_log("InoLoadSamplerModels", "execute is None")
            return (False, "not enabled", None, None, None, None, None, )

        if not execute:
            ino_print_log("InoLoadSamplerModels", "execute is False")
            return (False, "not enabled", None, None, None, None, None, )

        try:
            load_json = InoJsonHelper.string_to_dict(model_config)
            if not load_json["success"]:
                ino_print_log("InoLoadSamplerModels", "load_json failed")
                return (load_json["success"], load_json["msg"], None, None, None, None, None,)

            model_cfg = load_json["data"]

            unet_config = model_cfg["unet"]
            unet_file_loader = {}
            clip1_config = model_cfg["clip1"]
            clip1_file_loader = {}
            clip2_config = model_cfg["clip2"]
            clip2_file_loader = {}
            vae_config = model_cfg["vae"]
            vae_file_loader = {}

            hf_loader= InoHuggingFaceDownloadFile()
            civitai_loader = InoCivitaiDownloadFile()

            if unet_config["host"] == "hf":
                unet_file_loader = await hf_loader.function(
                    enabled=True,
                    dict_as_input=unet_config
                )
                if not unet_file_loader[0]:
                    ino_print_log("InoLoadSamplerModels", "unet_file_loader hf failed")
                    return (False, unet_file_loader[1], None, None, None, None, None,)
            elif unet_config["host"] == "civitai":
                unet_file_loader = await civitai_loader.function(
                    enabled=True,
                    dict_as_input=unet_config
                )
                if not unet_file_loader[0]:
                    ino_print_log("InoLoadSamplerModels", "unet_file_loader civitai failed")
                    return (False, unet_file_loader[1], None, None, None, None, None,)

            if clip1_config["host"] == "hf":
                clip1_file_loader = await hf_loader.function(
                    enabled=True,
                    dict_as_input=clip1_config
                )
                if not clip1_file_loader[0]:
                    ino_print_log("InoLoadSamplerModels", "clip1_file_loader hf failed")
                    return (False, clip1_file_loader[1], None, None, None, None, None,)
            else:
                ino_print_log("InoLoadSamplerModels", "clip1_file_loader not hf")
                return (False, "Downloading other than HF not supported for clip1", None, None, None, None, None,)

            if clip2_config["host"] == "hf":
                clip2_file_loader = await hf_loader.function(
                    enabled=True,
                    dict_as_input=clip2_config
                )
                if not clip2_file_loader[0]:
                    ino_print_log("InoLoadSamplerModels", "clip2_file_loader hf failed")
                    return (False, clip2_file_loader[1], None, None, None, None, None,)
            else:
                ino_print_log("InoLoadSamplerModels", "clip2_file_loader not hf")
                return (False, "Downloading other than HF not supported for clip2", None, None, None, None, None,)

            if vae_config["host"] == "hf":
                vae_file_loader = await hf_loader.function(
                    enabled=True,
                    dict_as_input=vae_config
                )
                if not vae_file_loader[0]:
                    ino_print_log("InoLoadSamplerModels", "vae_file_loader hf failed")
                    return (False, vae_file_loader[1], None, None, None, None, None,)
            else:
                ino_print_log("InoLoadSamplerModels", "vae_file_loader not hf")
                return (False, "Downloading other than HF not supported for vae", None, None, None, None, None,)

            from nodes import UNETLoader, CLIPLoader, DualCLIPLoader, VAELoader

            unet_loader = UNETLoader()
            load_unet = unet_loader.load_unet(
                unet_name=unet_file_loader[4],
                weight_dtype=model_cfg["weight_type"]
            )

            dual_clip = model_cfg["use_dual_clip"]
            if dual_clip:
                clip_loader = DualCLIPLoader()
                load_clip = clip_loader.load_clip(
                    clip_name1=clip1_file_loader[4],
                    clip_name2=clip2_file_loader[4],
                    type=model_cfg["type"],
                    device=clip_device,
                )
            else:
                clip_loader = CLIPLoader()
                load_clip = clip_loader.load_clip(
                    clip_name=clip1_file_loader[4],
                    type=model_cfg["type"],
                    device=clip_device,
                )

            vae_loader = VAELoader()
            load_vae = vae_loader.load_vae(
                vae_name=vae_file_loader[4],
            )

            model_loaded = load_unet[0]
            clip_loaded = load_clip[0]
            trigger_words = ""

            lora_loaded = False

            lora_1_loaded = load_lora(lora_1_config, model_loaded, clip_loaded)
            model_loaded = lora_1_loaded[1]
            clip_loaded = lora_1_loaded[2]
            trigger_words = trigger_words + lora_1_loaded[3]
            if lora_1_loaded[0]:
                lora_loaded = True

            lora_2_loaded = load_lora(lora_2_config, model_loaded, clip_loaded)
            model_loaded = lora_2_loaded[1]
            clip_loaded = lora_2_loaded[2]
            trigger_words = trigger_words + lora_2_loaded[3]
            if lora_2_loaded[0]:
                lora_loaded = True

            lora_3_loaded = load_lora(lora_3_config, model_loaded, clip_loaded)
            model_loaded = lora_3_loaded[1]
            clip_loaded = lora_3_loaded[2]
            trigger_words = trigger_words + lora_3_loaded[3]
            if lora_3_loaded[0]:
                lora_loaded = True

            lora_4_loaded = load_lora(lora_4_config, model_loaded, clip_loaded)
            model_loaded = lora_4_loaded[1]
            clip_loaded = lora_4_loaded[2]
            trigger_words = trigger_words + lora_4_loaded[3]
            if lora_4_loaded[0]:
                lora_loaded = True

            ino_print_log("InoLoadSamplerModels", "Success")
            return ( True, "Success", model_loaded, clip_loaded, load_vae[0], lora_loaded, trigger_words, )
        except Exception as e:
            ino_print_log("InoLoadSamplerModels", str(e))
            return (False, str(e), None, None, None, None, None,)

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
            "optional": {
                "use_cfg": (default_bool, ),
                "cfg": ("FLOAT", {"default": -1.0, "min": -1.0, "max": 100.0}),
                "sampler_name": (sampler_names, ),
                "scheduler_name": (scheduler_names, ),
                "steps": ("INT", {"default": -1, "min": -1, "max": 100}),
                "denoise": ("FLOAT", {"default": -1.0, "min": -1.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("GUIDER", "SAMPLER", "SIGMAS", "STRING", "STRING", )
    RETURN_NAMES = ("GUIDER", "SAMPLER", "SIGMAS", "OldConfig", "NewConfig", )
    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    def function(self, enabled,
                 config,
                 model, positive, negative,
                 use_cfg, cfg, sampler_name, scheduler_name, steps, denoise
        ):
        if not enabled:
            return (None, None, None, None, None, None,)

        update_config = InoUpdateModelConfig()
        updated_config = update_config.function(
            enabled=True,
            config=config,
            use_cfg=use_cfg,
            cfg=cfg,
            sampler_name=sampler_name,
            scheduler_name=scheduler_name,
            steps=steps,
            denoise=denoise
        )

        load_json = InoJsonHelper.string_to_dict(updated_config[1])
        if not load_json["success"]:
            return (None, None, None, None, None, None,)

        model_cfg = load_json["data"]

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

        model_cfg_str = InoJsonHelper.dict_to_string(model_cfg)
        if not model_cfg_str["success"]:
            return (-1, "", "",)

        return (get_guider[0], get_sampler[0], get_sigmas[0], config, model_cfg_str["data"], )

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
                "use_flux_encoder": (default_bool,),
                "use_flux_guidance": (default_bool,),
                "guidance": ("FLOAT", {"default": -1.0, "min": -1.0, "max": 100.0}),
                "use_negative_prompt": (default_bool,)
            }
        }

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING", "STRING", "STRING", )
    RETURN_NAMES = ("POSITIVE", "NEGATIVE", "OldConfig", "NewConfig", )
    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    def function(
        self, enabled,
        config,
        clip, positive1, positive2, negative,
        use_flux_encoder, use_flux_guidance, guidance, use_negative_prompt
    ):
        if not enabled:
            return (None, None, None, None, )

        update_config = InoUpdateModelConfig()
        updated_config = update_config.function(
            enabled=True,
            config=config,
            use_flux_encoder=use_flux_encoder,
            use_flux_guidance=use_flux_guidance,
            guidance=guidance,
            use_negative_prompt=use_negative_prompt
        )

        load_json = InoJsonHelper.string_to_dict(updated_config[1])
        if not load_json["success"]:
            return (None, None, None, None, None, None,)

        model_cfg = load_json["data"]

        final_guidance = float(model_cfg.get("guidance", -1))

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

        model_cfg_str = InoJsonHelper.dict_to_string(model_cfg)
        if not model_cfg_str["success"]:
            return (-1, "", "",)

        return (positive_condition[0], negative_condition[0], config, model_cfg_str["data"], )

class InoGetModelDownloadConfig:
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
        "BOOLEAN",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "Success",
        "Unet",
        "Clip1",
        "Clip2",
        "Vae",
    )

    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    def function(self, enabled, config):
        if not enabled:
            return (False, "", "", "", "", )

        load_json = InoJsonHelper.string_to_dict(config)
        if not load_json["success"]:
            return (False, "", "", "", "", )

        model_cfg = load_json["data"]

        unet_config = InoJsonHelper.dict_to_string(model_cfg["unet"])["data"]
        clip1_config = InoJsonHelper.dict_to_string(model_cfg["clip1"])["data"]
        clip2_config = InoJsonHelper.dict_to_string(model_cfg["clip2"])["data"]
        vae_config = InoJsonHelper.dict_to_string(model_cfg["vae"])["data"]

        return (
            True,
            unet_config,
            clip1_config,
            clip2_config,
            vae_config,
        )


LOCAL_NODE_CLASS = {
    "InoRandomNoise": InoRandomNoise,
    "InoGetModelConfig": InoGetModelConfig,
    "InoShowModelConfig": InoShowModelConfig,
    "InoUpdateModelConfig": InoUpdateModelConfig,
    "InoGetLoraConfig": InoGetLoraConfig,
    "InoShowLoraConfig": InoShowLoraConfig,
    "InoLoadSamplerModels": InoLoadSamplerModels,
    "InoGetConditioning": InoGetConditioning,
    "InoGetSamplerConfig": InoGetSamplerConfig,
    "InoGetModelDownloadConfig": InoGetModelDownloadConfig,
}
LOCAL_NODE_NAME = {
    "InoRandomNoise": "Ino Random Noise",
    "InoGetModelConfig": "Ino Get Model Config",
    "InoShowModelConfig": "Ino Show Model Config",
    "InoUpdateModelConfig": "Ino Update Model Config",
    "InoGetLoraConfig": "Ino Get Lora Config",
    "InoShowLoraConfig": "Ino Show Lora Config",
    "InoLoadSamplerModels": "Ino Load Sampler Models",
    "InoGetConditioning": "Ino Get Conditioning",
    "InoGetSamplerConfig": "Ino Get Sampler Config",
    "InoGetModelDownloadConfig": "Ino Get Model Download Config",
}

