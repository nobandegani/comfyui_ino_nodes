from pathlib import Path
from inopyutils import InoJsonHelper, InoHttpHelper, InoFileHelper, ino_ok, ino_err, ino_is_err

import folder_paths

from ..node_helper import ino_print_log, MODEL_TYPES, any_type, UNET_WEIGHT_DTYPE, CLIP_TYPE
from .download_model_helper import InoHandleDownloadModel

#todo add progress bar

class InoVaeLoadModel:
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

class InoControlnetLoadModel:
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
            supported = True
            if model_type == "controlnet":
                from nodes import ControlNetLoader

                model_loader = ControlNetLoader()
                file_loader = model_loader.load_controlnet(
                    control_net_name=model_path
                )
                loaded_model = file_loader[0]
            elif model_type == "diffusion_models":
                from nodes import UNETLoader

                model_loader = UNETLoader()
                file_loader = model_loader.load_unet(
                    unet_name=model_path,
                    weight_dtype=unet_weight_dtype
                )
                loaded_model = file_loader[0]
            elif model_type == "text_encoders":
                from nodes import CLIPLoader
                model_loader = CLIPLoader()

                file_loader = model_loader.load_clip(
                    clip_name=model_path,
                    type=clip_type,
                    device="default"
                )
                loaded_model = file_loader[0]
            elif model_type == "vae":
                from nodes import VAELoader
                model_loader = VAELoader()

                file_loader = model_loader.load_vae(
                    vae_name=model_path,
                )
                loaded_model = file_loader[0]
            else:
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
    "InoHandleLoadModel": InoHandleLoadModel,
    "InoHandleDownloadAndLoadModel": InoHandleDownloadAndLoadModel,
    "InoGetModelPathAsString": InoGetModelPathAsString
}
LOCAL_NODE_NAME = {
    "InoHandleLoadModel": "Ino Handle Load Model",
    "InoHandleDownloadAndLoadModel": "Ino Handle Download And Load Model",

    "InoGetModelPathAsString": "Ino Get Model Path As String"
}
