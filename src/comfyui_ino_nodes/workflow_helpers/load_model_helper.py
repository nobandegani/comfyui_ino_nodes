from pathlib import Path
from inopyutils import InoJsonHelper, InoHttpHelper, InoFileHelper, ino_ok, ino_err, ino_is_err

import folder_paths

from ..node_helper import ino_print_log, MODEL_TYPES, any_type, UNET_WEIGHT_DTYPE, CLIP_TYPE
from .download_model_helper import InoHandleDownloadModel

#todo add progress bar

class InoLoadVaeModel:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model_path": ("STRING", {"default": ""}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "VAE", )
    RETURN_NAMES = ("Success", "MSG", "VAE",)

    FUNCTION = "function"
    CATEGORY = "InoSamplerHelper"

    async def function(self, enabled, model_path: str,):
        if not enabled:
            ino_print_log("InoHandleLoadModel", "Attempt to run but disabled")
            return (False, "not enabled", None,)

        try:
            loaded_model = None
            from nodes import VAELoader
            model_loader = VAELoader()

            file_loader = model_loader.load_vae(
                vae_name=model_path,
            )
            loaded_model = file_loader[0]

            if loaded_model is not None:
                ino_print_log("InoHandleLoadModel", f"vae loaded")
                return (True, f"vae loaded", loaded_model,  )
            else:
                ino_print_log("InoHandleLoadModel", f"vae not loaded")
                return (False, f"vae not loaded", None,  )
        except Exception as e:
            ino_print_log("InoHandleLoadModel", "exception", e)
            return (False, f"Error: {e}", None, )

class InoLoadControlnetModel:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model_path": ("STRING", {"default": ""}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "CONTROL_NET", )
    RETURN_NAMES = ("Success", "MSG", "CONTROL_NET",)

    FUNCTION = "function"
    CATEGORY = "InoSamplerHelper"

    async def function(self, enabled, model_path: str):
        if not enabled:
            ino_print_log("InoHandleLoadModel", "Attempt to run but disabled")
            return (False, "not enabled", None,)

        try:
            loaded_model = None
            from nodes import ControlNetLoader

            model_loader = ControlNetLoader()
            file_loader = model_loader.load_controlnet(
                control_net_name=model_path
            )
            loaded_model = file_loader[0]

            if loaded_model is not None:
                ino_print_log("InoHandleLoadModel", f"controlnet loaded")
                return (True, f"controlnet loaded", loaded_model,  )
            else:
                ino_print_log("InoHandleLoadModel", f"controlnet not loaded")
                return (False, f"controlnet not loaded", None,  )
        except Exception as e:
            ino_print_log("InoHandleLoadModel", "exception", e)
            return (False, f"Error: {e}", None, )

class InoLoadClipModel:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model_path": ("STRING", {"default": ""}),
            },
            "optional": {
                "clip_type": (CLIP_TYPE, {})
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "CLIP", )
    RETURN_NAMES = ("Success", "MSG", "CLIP",)

    FUNCTION = "function"
    CATEGORY = "InoSamplerHelper"

    async def function(self, enabled, model_path: str, clip_type:str):
        if not enabled:
            ino_print_log("InoHandleLoadModel", "Attempt to run but disabled")
            return (False, "not enabled", None,)

        try:
            loaded_model = None
            from nodes import CLIPLoader
            model_loader = CLIPLoader()

            file_loader = model_loader.load_clip(
                clip_name=model_path,
                type=clip_type,
                device="default"
            )
            loaded_model = file_loader[0]

            if loaded_model is not None:
                ino_print_log("InoHandleLoadModel", f"clip loaded")
                return (True, f"clip loaded", loaded_model,  )
            else:
                ino_print_log("InoHandleLoadModel", f"clip not loaded")
                return (False, f"clip not loaded", None,  )
        except Exception as e:
            ino_print_log("InoHandleLoadModel", "exception", e)
            return (False, f"Error: {e}", None, )

class InoLoadDiffusionModel:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model_path": ("STRING", {"default": ""}),
            },
            "optional": {
                "unet_weight_dtype": (UNET_WEIGHT_DTYPE, {}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "MODEL", )
    RETURN_NAMES = ("Success", "MSG", "MODEL",)

    FUNCTION = "function"
    CATEGORY = "InoSamplerHelper"

    async def function(self, enabled, model_path: str, unet_weight_dtype:str):
        if not enabled:
            ino_print_log("InoHandleLoadModel", "Attempt to run but disabled")
            return (False, "not enabled", None,)

        try:
            loaded_model = None
            from nodes import UNETLoader

            model_loader = UNETLoader()
            file_loader = model_loader.load_unet(
                unet_name=model_path,
                weight_dtype=unet_weight_dtype
            )
            loaded_model = file_loader[0]

            if loaded_model is not None:
                ino_print_log("InoHandleLoadModel", f"diffusion loaded")
                return (True, f"diffusion loaded", loaded_model,  )
            else:
                ino_print_log("InoHandleLoadModel", f"diffusion not loaded")
                return (False, f"diffusion not loaded", None,  )
        except Exception as e:
            ino_print_log("InoHandleLoadModel", "exception", e)
            return (False, f"Error: {e}", None, )

class InoLoadLoraClipModel:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model_path": ("STRING", {"default": ""}),
                "model": ("MODEL", {}),
                "clip": ("CLIP", {}),
            },
            "optional": {
                "strength_model": ("FLOAT", {"default": 1, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "MODEL", "CLIP", )
    RETURN_NAMES = ("Success", "MSG", "MODEL", "CLIP", )

    FUNCTION = "function"
    CATEGORY = "InoSamplerHelper"

    async def function(self, enabled, model_path: str, model, clip, strength_model, strength_clip):
        if not enabled:
            ino_print_log("InoHandleLoadModel", "Attempt to run but disabled")
            return (False, "not enabled", None,)

        try:
            loaded_model = None
            loaded_clip = None
            from nodes import LoraLoader

            model_loader = LoraLoader()
            file_loader = model_loader.load_lora(
                model=model,
                clip=clip,
                lora_name=model_path,
                strength_model=strength_model,
                strength_clip=strength_clip
            )
            loaded_model = file_loader[0]
            loaded_clip = file_loader[1]

            if loaded_model is not None and loaded_clip is not None:
                ino_print_log("InoHandleLoadModel", f"lora loaded")
                return (True, f"lora loaded", loaded_model,  loaded_clip)
            else:
                ino_print_log("InoHandleLoadModel", f"lora not loaded")
                return (False, f"lora not loaded", None,  )
        except Exception as e:
            ino_print_log("InoHandleLoadModel", "exception", e)
            return (False, f"Error: {e}", None, )

class InoLoadLoraModel:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model_path": ("STRING", {"default": ""}),
                "model": ("MODEL", {}),
            },
            "optional": {
                "strength_model": ("FLOAT", {"default": 1, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "MODEL", "CLIP", )
    RETURN_NAMES = ("Success", "MSG", "MODEL", "CLIP", )

    FUNCTION = "function"
    CATEGORY = "InoSamplerHelper"

    async def function(self, enabled, model_path: str, model, strength_model):
        if not enabled:
            ino_print_log("InoHandleLoadModel", "Attempt to run but disabled")
            return (False, "not enabled", None,)

        try:
            loaded_model = None
            from nodes import LoraLoaderModelOnly

            model_loader = LoraLoaderModelOnly()
            file_loader = model_loader.load_lora_model_only(
                model=model,
                lora_name=model_path,
                strength_model=strength_model,
            )
            loaded_model = file_loader[0]

            if loaded_model is not None:
                ino_print_log("InoHandleLoadModel", f"lora loaded")
                return (True, f"lora loaded", loaded_model,)
            else:
                ino_print_log("InoHandleLoadModel", f"lora not loaded")
                return (False, f"lora not loaded", None,  )
        except Exception as e:
            ino_print_log("InoHandleLoadModel", "exception", e)
            return (False, f"Error: {e}", None, )

class InoHandleLoadModel:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model_type": (MODEL_TYPES, {}),
                "model_path": ("STRING", {"default": ""}),
            },
            "optional": {
                "unet_weight_dtype": (UNET_WEIGHT_DTYPE, {}),
                "clip_type": (CLIP_TYPE, {})
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", any_type, )
    RETURN_NAMES = ("Success", "MSG", "Model",)

    FUNCTION = "function"
    CATEGORY = "InoSamplerHelper"

    async def function(self, enabled, model_type:str, model_path: str, unet_weight_dtype, clip_type):
        if not enabled:
            ino_print_log("InoHandleLoadModel", "Attempt to run but disabled")
            return (False, "not enabled", None,)

        try:
            loaded_model = None
            supported = False

            if not supported:
                ino_print_log("InoHandleLoadModel", f"loading {model_type} not supported")
                return (False, f"loading {model_type} models not supported yet", None, )

            if loaded_model is not None:
                ino_print_log("InoHandleLoadModel", f"{model_type} loaded")
                return (True, f"{model_type} loaded", loaded_model,  )
            else:
                ino_print_log("InoHandleLoadModel", f"{model_type} not loaded")
                return (False, f"{model_type} not loaded", None,  )
        except Exception as e:
            ino_print_log("InoHandleLoadModel", "exception", e)
            return (False, f"Error: {e}", None, )

class InoHandleDownloadAndLoadModel:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "config": ("STRING", {"default": "{}"}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING", any_type,)
    RETURN_NAMES = ("success", "msg", "model_type", "abs_path", "rel_path", "loaded_model",)

    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    async def function(self, enabled, config: str):
        if not enabled:
            ino_print_log("InoHandleDownloadAndLoadModel", "Attempt to run but disabled")
            return (False, "not enabled", "", "", "", None,)

        download_handler = InoHandleDownloadModel()
        download_result = await download_handler.function(enabled=True, config=config)

        if not download_result[0]:
            ino_print_log("InoHandleDownloadAndLoadModel", "download failed", download_result[1])
            return (False, download_result[1], "", "", "", None,)

        model_type = download_result[2]
        abs_path = download_result[3]
        rel_path = download_result[4]

        model_load_handler = InoHandleLoadModel()
        model_loader = await model_load_handler.function(enabled=True, model_type=model_type, model_path=rel_path)
        if not model_loader[0]:
            ino_print_log("InoHandleDownloadAndLoadModel", "load failed", model_loader[1])
            return (False, model_loader[1], model_type, abs_path, rel_path, None, )

        ino_print_log("InoHandleDownloadAndLoadModel", f"{model_type} downloaded and loaded")
        return (True, f"{model_type} loaded", model_type, abs_path, rel_path, model_loader[2])

class InoGetModelPathAsString:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_type": (MODEL_TYPES, {}),
            }
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("string", )

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, model_type,):
        model_path = Path(folder_paths.get_input_directory()).parent / "models" / model_type
        return (str(model_path.resolve()), )


LOCAL_NODE_CLASS = {
    "InoLoadVaeModel": InoLoadVaeModel,
    "InoLoadControlnetModel": InoLoadControlnetModel,
    "InoLoadClipModel": InoLoadClipModel,
    "InoLoadDiffusionModel": InoLoadDiffusionModel,
    "InoLoadLoraClipModel": InoLoadLoraClipModel,
    "InoLoadLoraModel": InoLoadLoraModel,

    "InoHandleLoadModel": InoHandleLoadModel,
    "InoHandleDownloadAndLoadModel": InoHandleDownloadAndLoadModel,

    "InoGetModelPathAsString": InoGetModelPathAsString
}
LOCAL_NODE_NAME = {
    "InoLoadVaeModel": "Ino Load VAE Model",
    "InoLoadControlnetModel": "Ino Load Controlnet Model",
    "InoLoadClipModel": "Ino Load Clip Model",
    "InoLoadDiffusionModel": "Ino Load Diffusion Model",
    "InoLoadLoraClipModel": "Ino Load Lora Clip Model",
    "InoLoadLoraModel": "Ino Load Lora Model",

    "InoHandleLoadModel": "Ino Handle Load Model",
    "InoHandleDownloadAndLoadModel": "Ino Handle Download And Load Model",

    "InoGetModelPathAsString": "Ino Get Model Path As String"
}
