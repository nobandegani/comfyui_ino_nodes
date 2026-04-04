import os
from pathlib import Path

import folder_paths

from comfy_api.latest import io

from ..node_helper import ino_print_log, MODEL_TYPES, UNET_WEIGHT_DTYPE, CLIP_TYPE
from .download_model_helper import InoHandleDownloadModel


class InoLoadVaeModel(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoLoadVaeModel",
            display_name="Ino Load VAE Model",
            category="InoModelHelper",
            description="Loads a VAE model from a file path.",
            inputs=[
                io.Boolean.Input("enabled", default=True, label_off="OFF", label_on="ON"),
                io.String.Input("model_path", default=""),
            ],
            outputs=[
                io.Boolean.Output(display_name="success"),
                io.String.Output(display_name="message"),
                io.Vae.Output(display_name="vae"),
            ],
        )

    @classmethod
    async def execute(cls, enabled, model_path) -> io.NodeOutput:
        if not enabled:
            ino_print_log("InoLoadVaeModel", "Attempt to run but disabled")
            return io.NodeOutput(False, "not enabled", None)

        try:
            from nodes import VAELoader
            model_loader = VAELoader()
            file_loader = model_loader.load_vae(vae_name=model_path)
            loaded_model = file_loader[0]

            if loaded_model is not None:
                ino_print_log("InoLoadVaeModel", "vae loaded")
                return io.NodeOutput(True, "vae loaded", loaded_model)
            else:
                ino_print_log("InoLoadVaeModel", "vae not loaded")
                return io.NodeOutput(False, "vae not loaded", None)
        except Exception as e:
            ino_print_log("InoLoadVaeModel", "exception", e)
            return io.NodeOutput(False, f"Error: {e}", None)


class InoLoadControlnetModel(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoLoadControlnetModel",
            display_name="Ino Load Controlnet Model",
            category="InoModelHelper",
            description="Loads a ControlNet model from a file path.",
            inputs=[
                io.Boolean.Input("enabled", default=True, label_off="OFF", label_on="ON"),
                io.String.Input("model_path", default=""),
            ],
            outputs=[
                io.Boolean.Output(display_name="success"),
                io.String.Output(display_name="message"),
                io.ControlNet.Output(display_name="control_net"),
            ],
        )

    @classmethod
    async def execute(cls, enabled, model_path) -> io.NodeOutput:
        if not enabled:
            ino_print_log("InoLoadControlnetModel", "Attempt to run but disabled")
            return io.NodeOutput(False, "not enabled", None)

        try:
            from nodes import ControlNetLoader
            model_loader = ControlNetLoader()
            file_loader = model_loader.load_controlnet(control_net_name=model_path)
            loaded_model = file_loader[0]

            if loaded_model is not None:
                ino_print_log("InoLoadControlnetModel", "controlnet loaded")
                return io.NodeOutput(True, "controlnet loaded", loaded_model)
            else:
                ino_print_log("InoLoadControlnetModel", "controlnet not loaded")
                return io.NodeOutput(False, "controlnet not loaded", None)
        except Exception as e:
            ino_print_log("InoLoadControlnetModel", "exception", e)
            return io.NodeOutput(False, f"Error: {e}", None)


class InoLoadClipModel(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoLoadClipModel",
            display_name="Ino Load Clip Model",
            category="InoModelHelper",
            description="Loads a CLIP model from a file path.",
            inputs=[
                io.Boolean.Input("enabled", default=True, label_off="OFF", label_on="ON"),
                io.String.Input("model_path", default=""),
                io.Combo.Input("clip_type", options=CLIP_TYPE, optional=True),
            ],
            outputs=[
                io.Boolean.Output(display_name="success"),
                io.String.Output(display_name="message"),
                io.Clip.Output(display_name="clip"),
            ],
        )

    @classmethod
    async def execute(cls, enabled, model_path, clip_type="stable_diffusion") -> io.NodeOutput:
        if not enabled:
            ino_print_log("InoLoadClipModel", "Attempt to run but disabled")
            return io.NodeOutput(False, "not enabled", None)

        try:
            from nodes import CLIPLoader
            model_loader = CLIPLoader()
            file_loader = model_loader.load_clip(clip_name=model_path, type=clip_type, device="default")
            loaded_model = file_loader[0]

            if loaded_model is not None:
                ino_print_log("InoLoadClipModel", "clip loaded")
                return io.NodeOutput(True, "clip loaded", loaded_model)
            else:
                ino_print_log("InoLoadClipModel", "clip not loaded")
                return io.NodeOutput(False, "clip not loaded", None)
        except Exception as e:
            ino_print_log("InoLoadClipModel", "exception", e)
            return io.NodeOutput(False, f"Error: {e}", None)


class InoLoadDiffusionModel(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoLoadDiffusionModel",
            display_name="Ino Load Diffusion Model",
            category="InoModelHelper",
            description="Loads a diffusion/UNET model from a file path.",
            inputs=[
                io.Boolean.Input("enabled", default=True, label_off="OFF", label_on="ON"),
                io.String.Input("model_path", default=""),
                io.Combo.Input("unet_weight_dtype", options=UNET_WEIGHT_DTYPE, optional=True),
            ],
            outputs=[
                io.Boolean.Output(display_name="success"),
                io.String.Output(display_name="message"),
                io.Model.Output(display_name="model"),
            ],
        )

    @classmethod
    async def execute(cls, enabled, model_path, unet_weight_dtype="default") -> io.NodeOutput:
        if not enabled:
            ino_print_log("InoLoadDiffusionModel", "Attempt to run but disabled")
            return io.NodeOutput(False, "not enabled", None)

        try:
            from nodes import UNETLoader
            model_loader = UNETLoader()
            file_loader = model_loader.load_unet(unet_name=model_path, weight_dtype=unet_weight_dtype)
            loaded_model = file_loader[0]

            if loaded_model is not None:
                ino_print_log("InoLoadDiffusionModel", "diffusion loaded")
                return io.NodeOutput(True, "diffusion loaded", loaded_model)
            else:
                ino_print_log("InoLoadDiffusionModel", "diffusion not loaded")
                return io.NodeOutput(False, "diffusion not loaded", None)
        except Exception as e:
            ino_print_log("InoLoadDiffusionModel", "exception", e)
            return io.NodeOutput(False, f"Error: {e}", None)


class InoLoadLoraClipModel(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoLoadLoraClipModel",
            display_name="Ino Load Lora Clip Model",
            category="InoModelHelper",
            description="Loads a LoRA and applies it to both model and CLIP.",
            inputs=[
                io.Boolean.Input("enabled", default=True, label_off="OFF", label_on="ON"),
                io.String.Input("model_path", default=""),
                io.Model.Input("model"),
                io.Clip.Input("clip"),
                io.Float.Input("strength_model", default=1.0, step=0.01, optional=True),
                io.Float.Input("strength_clip", default=1.0, step=0.01, optional=True),
            ],
            outputs=[
                io.Boolean.Output(display_name="success"),
                io.String.Output(display_name="message"),
                io.String.Output(display_name="name"),
                io.String.Output(display_name="trigger_word"),
                io.Model.Output(display_name="model"),
                io.Clip.Output(display_name="clip"),
            ],
        )

    @classmethod
    async def execute(cls, enabled, model_path, model, clip, strength_model=1.0, strength_clip=1.0) -> io.NodeOutput:
        if not enabled:
            ino_print_log("InoLoadLoraClipModel", "Attempt to run but disabled")
            return io.NodeOutput(False, "not enabled", "", "", None, None)

        try:
            lora_name = os.path.splitext(os.path.basename(model_path))[0]
            lora_trigger = lora_name.split("_", 1)[0]

            from nodes import LoraLoader
            model_loader = LoraLoader()
            file_loader = model_loader.load_lora(
                model=model, clip=clip, lora_name=model_path,
                strength_model=strength_model, strength_clip=strength_clip
            )
            loaded_model = file_loader[0]
            loaded_clip = file_loader[1]

            if loaded_model is not None and loaded_clip is not None:
                ino_print_log("InoLoadLoraClipModel", "lora loaded")
                return io.NodeOutput(True, "lora loaded", lora_name, lora_trigger, loaded_model, loaded_clip)
            else:
                ino_print_log("InoLoadLoraClipModel", "lora not loaded")
                return io.NodeOutput(False, "lora not loaded", "", "", None, None)
        except Exception as e:
            ino_print_log("InoLoadLoraClipModel", "exception", e)
            return io.NodeOutput(False, f"Error: {e}", "", "", None, None)


class InoLoadLoraModel(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoLoadLoraModel",
            display_name="Ino Load Lora Model",
            category="InoModelHelper",
            description="Loads a LoRA and applies it to the model only.",
            inputs=[
                io.Boolean.Input("enabled", default=True, label_off="OFF", label_on="ON"),
                io.String.Input("model_path", default=""),
                io.Model.Input("model"),
                io.Float.Input("strength_model", default=1.0, step=0.01, optional=True),
            ],
            outputs=[
                io.Boolean.Output(display_name="success"),
                io.String.Output(display_name="message"),
                io.String.Output(display_name="name"),
                io.String.Output(display_name="trigger_word"),
                io.Model.Output(display_name="model"),
            ],
        )

    @classmethod
    async def execute(cls, enabled, model_path, model, strength_model=1.0) -> io.NodeOutput:
        if not enabled:
            ino_print_log("InoLoadLoraModel", "Attempt to run but disabled")
            return io.NodeOutput(False, "not enabled", "", "", None)

        try:
            lora_name = os.path.splitext(os.path.basename(model_path))[0]
            lora_trigger = lora_name.split("_", 1)[0]

            from nodes import LoraLoaderModelOnly
            model_loader = LoraLoaderModelOnly()
            file_loader = model_loader.load_lora_model_only(
                model=model, lora_name=model_path, strength_model=strength_model
            )
            loaded_model = file_loader[0]

            if loaded_model is not None:
                ino_print_log("InoLoadLoraModel", "lora loaded")
                return io.NodeOutput(True, "lora loaded", lora_name, lora_trigger, loaded_model)
            else:
                ino_print_log("InoLoadLoraModel", "lora not loaded")
                return io.NodeOutput(False, "lora not loaded", "", "", None)
        except Exception as e:
            ino_print_log("InoLoadLoraModel", "exception", e)
            return io.NodeOutput(False, f"Error: {e}", "", "", None)


class InoHandleLoadModel(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoHandleLoadModel",
            display_name="Ino Handle Load Model",
            category="InoModelHelper",
            description="Generic model loader by type. Currently not fully implemented.",
            inputs=[
                io.Boolean.Input("enabled", default=True, label_off="OFF", label_on="ON"),
                io.Combo.Input("model_type", options=list(MODEL_TYPES)),
                io.String.Input("model_path", default=""),
                io.Combo.Input("unet_weight_dtype", options=UNET_WEIGHT_DTYPE, optional=True),
                io.Combo.Input("clip_type", options=CLIP_TYPE, optional=True),
            ],
            outputs=[
                io.Boolean.Output(display_name="success"),
                io.String.Output(display_name="message"),
                io.AnyType.Output(display_name="model"),
            ],
        )

    @classmethod
    async def execute(cls, enabled, model_type, model_path, unet_weight_dtype="default", clip_type="stable_diffusion") -> io.NodeOutput:
        if not enabled:
            ino_print_log("InoHandleLoadModel", "Attempt to run but disabled")
            return io.NodeOutput(False, "not enabled", None)

        try:
            ino_print_log("InoHandleLoadModel", f"loading {model_type} not supported")
            return io.NodeOutput(False, f"loading {model_type} models not supported yet", None)
        except Exception as e:
            ino_print_log("InoHandleLoadModel", "exception", e)
            return io.NodeOutput(False, f"Error: {e}", None)


class InoHandleDownloadAndLoadModel(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoHandleDownloadAndLoadModel",
            display_name="Ino Handle Download And Load Model",
            category="InoModelHelper",
            description="Downloads and loads a model in a single operation.",
            inputs=[
                io.Boolean.Input("enabled", default=True, label_off="OFF", label_on="ON"),
                io.String.Input("config", default="{}"),
            ],
            outputs=[
                io.Boolean.Output(display_name="success"),
                io.String.Output(display_name="msg"),
                io.String.Output(display_name="model_type"),
                io.String.Output(display_name="abs_path"),
                io.String.Output(display_name="rel_path"),
                io.AnyType.Output(display_name="loaded_model"),
            ],
        )

    @classmethod
    async def execute(cls, enabled, config) -> io.NodeOutput:
        if not enabled:
            ino_print_log("InoHandleDownloadAndLoadModel", "Attempt to run but disabled")
            return io.NodeOutput(False, "not enabled", "", "", "", None)

        download_result = await InoHandleDownloadModel.execute(enabled=True, config=config)

        if not download_result.args[0]:
            ino_print_log("InoHandleDownloadAndLoadModel", "download failed", download_result.args[1])
            return io.NodeOutput(False, download_result.args[1], "", "", "", None)

        model_type = download_result.args[2]
        abs_path = download_result.args[3]
        rel_path = download_result.args[4]

        model_loader = await InoHandleLoadModel.execute(enabled=True, model_type=model_type, model_path=rel_path)
        if not model_loader.args[0]:
            ino_print_log("InoHandleDownloadAndLoadModel", "load failed", model_loader.args[1])
            return io.NodeOutput(False, model_loader.args[1], model_type, abs_path, rel_path, None)

        ino_print_log("InoHandleDownloadAndLoadModel", f"{model_type} downloaded and loaded")
        return io.NodeOutput(True, f"{model_type} loaded", model_type, abs_path, rel_path, model_loader.args[2])


class InoGetModelPathAsString(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoGetModelPathAsString",
            display_name="Ino Get Model Path As String",
            category="InoModelHelper",
            description="Returns the absolute path to a model directory for a given type.",
            inputs=[
                io.Combo.Input("model_type", options=list(MODEL_TYPES)),
            ],
            outputs=[
                io.String.Output(display_name="path"),
            ],
        )

    @classmethod
    def execute(cls, model_type) -> io.NodeOutput:
        model_path = Path(folder_paths.get_input_directory()).parent / "models" / model_type
        return io.NodeOutput(str(model_path.resolve()))


LOCAL_NODE_CLASS = {
    "InoLoadVaeModel": InoLoadVaeModel,
    "InoLoadControlnetModel": InoLoadControlnetModel,
    "InoLoadClipModel": InoLoadClipModel,
    "InoLoadDiffusionModel": InoLoadDiffusionModel,
    "InoLoadLoraClipModel": InoLoadLoraClipModel,
    "InoLoadLoraModel": InoLoadLoraModel,

    "InoHandleLoadModel": InoHandleLoadModel,
    "InoHandleDownloadAndLoadModel": InoHandleDownloadAndLoadModel,

    "InoGetModelPathAsString": InoGetModelPathAsString,
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

    "InoGetModelPathAsString": "Ino Get Model Path As String",
}
